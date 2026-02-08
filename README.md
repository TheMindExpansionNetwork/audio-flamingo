# 🎵 MusicMind - Audio Flamingo 3 for OpenClaw

> **AI Music Understanding for Parties, Events, and Creative Projects**

This is a fork of [NVIDIA's Audio Flamingo 3](https://github.com/NVIDIA/audio-flamingo) adapted for the MindBots ecosystem. It provides music analysis, party vibe checking, lyrics transcription, and social media caption generation.

## 🚀 Quick Start

```bash
# Deploy on Modal (serverless A100)
cd modal_deploy
modal deploy modal_app.py

# Use the CLI
python3 musicmind.py analyze song.mp3
python3 musicmind.py party-vibe track.wav
python3 musicmind.py transcribe vocals.mp3
```

## ✨ Features

- **🎵 Music Analysis** - Genre, mood, tempo, instrumentation, recommendations
- **🎉 Party Vibe Check** - Rate tracks 1-10 for dancefloor suitability
- **🎤 Lyrics Transcription** - Extract lyrics from any song
- **📱 Social Captions** - Generate catchy captions for music posts
- **⚡ Serverless** - Deploys on Modal, scales to zero, pay-per-use

## 🛠️ Usage

### CLI

```bash
# Analyze a track
python3 musicmind.py analyze song.mp3

# Check if it's a banger for your party
python3 musicmind.py party-vibe drop.wav
# Output: "🔥 BANGER - Drop this at peak time!"

# Transcribe lyrics
python3 musicmind.py transcribe song.mp3

# Generate Instagram caption
python3 musicmind.py caption beat.mp3
# Output: "Late night studio vibes 🌙🔊"
```

### Python

```python
from musicmind import MusicMind

mind = MusicMind()

# Full analysis
result = mind.analyze("song.mp3")
print(result['analysis'])
print(f"Tempo: {result['tempo_bpm']:.1f} BPM")

# Party check
vibe = mind.party_vibe("track.wav")
print(vibe['analysis'])
```

## 📡 API Endpoints

Once deployed:

| Endpoint | Description |
|----------|-------------|
| `POST /analyze` | Full music analysis |
| `POST /party-vibe` | Party suitability |
| `POST /transcribe` | Lyrics extraction |
| `POST /caption` | Social media captions |
| `GET /health` | Health check |

## 💰 Cost

Deployed on Modal with A100 GPUs:
- **Cold starts:** ~30 seconds
- **Active:** ~$2/hour while processing
- **Idle:** $0 (scales to zero)
- **Typical usage:** $5-40/month depending on volume

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Client    │────▶│  Modal App   │────▶│  Audio Flamingo │
│  (CLI/API)  │◀────│  (FastAPI)   │◀────│       3         │
└─────────────┘     └──────────────┘     │   (A100 GPU)    │
                                          └─────────────────┘
```

## 🔄 Sync with Upstream

```bash
./update-from-upstream.sh
```

## 📄 License

NVIDIA OneWay Noncommercial License (same as original)

## 🙏 Credits

- Original: [NVIDIA Audio Flamingo 3](https://github.com/NVIDIA/audio-flamingo)
- Model: [Hugging Face](https://huggingface.co/nvidia/audio-flamingo-3-hf)
- Paper: [arXiv](https://arxiv.org/abs/2501.XXX)

---

**Part of the MindBots ecosystem** 🏛️🔥
