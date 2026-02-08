"""
Audio Flamingo 3 - Modal Serverless Deployment
Music Understanding AI - Persistent Model Caching
"""

import modal

# Modal image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "torch>=2.0.0",
        "transformers>=4.48.0",
        "accelerate>=0.25.0",
        "huggingface-hub>=0.19.0",
        "soundfile>=0.12.1",
        "librosa>=0.10.1",
        "numpy>=1.24.0",
        "fastapi>=0.104.0",
        "python-multipart>=0.0.6",
    )
    .env({
        "HF_HUB_ENABLE_HF_TRANSFER": "1",
        "HF_HOME": "/cache/hf",  # Store HF cache on volume
        "TRANSFORMERS_CACHE": "/cache/transformers",
    })
)

# Modal app
app = modal.App("audio-flamingo-music", image=image)

# Volume for caching models (persisted across runs)
cache_vol = modal.Volume.from_name("audio-flamingo-cache", create_if_missing=True)


@app.cls(
    gpu="A100",
    container_idle_timeout=300,
    timeout=1800,  # 30 min timeout for initial model download
    volumes={"/cache": cache_vol},
)
class AudioFlamingoMusic:
    """Audio Flamingo 3 for music understanding"""
    
    @modal.enter()
    def load_model(self):
        """Load model - downloads once, cached forever"""
        from transformers import (
            AudioFlamingo3ForConditionalGeneration,
            AutoProcessor,
        )
        import torch
        import os
        
        model_id = "nvidia/audio-flamingo-3-hf"
        
        print("🎵 Loading Audio Flamingo 3...")
        print(f"📦 Cache location: /cache")
        
        # Check if already cached
        cache_size = self._get_dir_size("/cache")
        print(f"💾 Current cache size: {cache_size / 1e9:.2f} GB")
        
        self.processor = AutoProcessor.from_pretrained(
            model_id,
            cache_dir="/cache/transformers",
            local_files_only=False,
        )
        
        self.model = AudioFlamingo3ForConditionalGeneration.from_pretrained(
            model_id,
            cache_dir="/cache/transformers",
            device_map="auto",
            torch_dtype=torch.float16,
            local_files_only=False,
        )
        
        # Save to volume after download
        cache_vol.commit()
        
        new_size = self._get_dir_size("/cache")
        print(f"✅ Model loaded! Cache size: {new_size / 1e9:.2f} GB")
    
    def _get_dir_size(self, path):
        """Get directory size in bytes"""
        import os
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
        return total
    
    @modal.method()
    def analyze_music(self, audio_path: str, prompt: str = None) -> dict:
        """Analyze music and provide insights"""
        import librosa
        
        if prompt is None:
            prompt = """Analyze this music and provide:
            1. Genre and style
            2. Mood and energy level (1-10)
            3. Best use case (party, chill, workout, etc.)
            4. Similar artists/tracks
            5. Production notes (tempo, key, instrumentation)
            """
        
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "audio", "path": audio_path},
                ],
            }
        ]
        
        inputs = self.processor.apply_chat_template(
            conversation,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
        ).to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )
        
        response = self.processor.batch_decode(
            outputs[:, inputs.input_ids.shape[1]:],
            skip_special_tokens=True,
        )[0]
        
        # Get audio features
        try:
            y, sr = librosa.load(audio_path, sr=None, duration=30)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            duration = len(y) / sr
        except:
            tempo = 0
            duration = 0
        
        return {
            "analysis": response,
            "tempo_bpm": float(tempo) if tempo else 0,
            "duration_seconds": duration,
        }
    
    @modal.method()
    def party_vibe_check(self, audio_path: str) -> dict:
        """Check if track is good for a party"""
        prompt = """Rate this track for a party (1-10) and explain why.
        Consider: energy, danceability, crowd appeal, drop quality.
        Give a one-line verdict like "🔥 BANGER - Drop this at peak time!" or "😴 Skip - Too chill"
        """
        
        result = self.analyze_music(audio_path, prompt)
        result["vibe_check"] = True
        return result
    
    @modal.method()
    def transcribe_lyrics(self, audio_path: str) -> dict:
        """Transcribe lyrics from music"""
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Transcribe all lyrics from this song accurately."},
                    {"type": "audio", "path": audio_path},
                ],
            }
        ]
        
        inputs = self.processor.apply_chat_template(
            conversation,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
        ).to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=1024,
        )
        
        response = self.processor.batch_decode(
            outputs[:, inputs.input_ids.shape[1]:],
            skip_special_tokens=True,
        )[0]
        
        return {"lyrics": response}
    
    @modal.method()
    def generate_caption(self, audio_path: str) -> dict:
        """Generate social media caption"""
        prompt = """Create a catchy social media caption for this track.
        Make it fun, include emojis, and capture the vibe.
        Examples: "This drop hits different 🚀", "Late night drives only 🌙"
        """
        
        return self.analyze_music(audio_path, prompt)


# FastAPI web endpoint
@app.function(volumes={"/cache": cache_vol})
@modal.asgi_app()
def fastapi_app():
    """FastAPI app for HTTP requests"""
    from fastapi import FastAPI, File, UploadFile, Form
    from fastapi.responses import JSONResponse
    import tempfile
    import os
    
    web_app = FastAPI(title="Audio Flamingo Music API")
    handler = AudioFlamingoMusic()
    
    @web_app.post("/analyze")
    async def analyze(file: UploadFile = File(...), prompt: str = Form(None)):
        """Analyze uploaded audio file"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            result = handler.analyze_music.remote(tmp_path, prompt)
            return JSONResponse(result)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            os.unlink(tmp_path)
    
    @web_app.post("/party-vibe")
    async def party_vibe(file: UploadFile = File(...)):
        """Check party vibe of a track"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            result = handler.party_vibe_check.remote(tmp_path)
            return JSONResponse(result)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            os.unlink(tmp_path)
    
    @web_app.post("/transcribe")
    async def transcribe(file: UploadFile = File(...)):
        """Transcribe lyrics from audio"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            result = handler.transcribe_lyrics.remote(tmp_path)
            return JSONResponse(result)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            os.unlink(tmp_path)
    
    @web_app.post("/caption")
    async def caption(file: UploadFile = File(...)):
        """Generate social media caption"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            result = handler.generate_caption.remote(tmp_path)
            return JSONResponse(result)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            os.unlink(tmp_path)
    
    @web_app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "model": "audio-flamingo-3",
            "cached": True,
        }
    
    return web_app


# CLI entry point
@app.local_entrypoint()
def main():
    """Test the model locally"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: modal run modal_app.py -- <audio_file> [command]")
        print("Commands: analyze, party-vibe, transcribe, caption")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "analyze"
    
    handler = AudioFlamingoMusic()
    
    if command == "analyze":
        result = handler.analyze_music.remote(audio_file)
        print(f"🎵 Analysis:\n{result['analysis']}")
        print(f"\n📊 Tempo: {result['tempo_bpm']:.1f} BPM")
    
    elif command == "party-vibe":
        result = handler.party_vibe_check.remote(audio_file)
        print(f"🎉 Party Vibe Check:\n{result['analysis']}")
    
    elif command == "transcribe":
        result = handler.transcribe_lyrics.remote(audio_file)
        print(f"🎤 Lyrics:\n{result['lyrics']}")
    
    elif command == "caption":
        result = handler.generate_caption.remote(audio_file)
        print(f"📱 Caption:\n{result['analysis']}")
