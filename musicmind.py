#!/usr/bin/env python3
"""
MusicMind - Audio Flamingo 3 Skill for OpenClaw
Music understanding, party vibes, and audio intelligence
"""

import os
import sys
import json
import requests
import argparse
from pathlib import Path
from typing import Optional

# Modal deployment endpoint
MODAL_ENDPOINT = os.getenv("MUSICMIND_ENDPOINT", "https://themindexpansionnetwork--audio-flamingo-music-fastapi-app.modal.run")


class MusicMind:
    """
    🎵 MusicMind - AI Music Understanding
    
    Powered by Audio Flamingo 3 - understands music, speech, and sounds
    Perfect for parties, events, content creation, and music discovery
    """
    
    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint or MODAL_ENDPOINT
        self.session = requests.Session()
    
    def analyze(self, audio_path: str, prompt: Optional[str] = None) -> dict:
        """
        Analyze music and get insights
        
        Args:
            audio_path: Path to audio file (mp3, wav, flac)
            prompt: Custom analysis prompt (optional)
        
        Returns:
            Analysis results with genre, mood, tempo, recommendations
        """
        with open(audio_path, 'rb') as f:
            files = {'file': f}
            data = {'prompt': prompt} if prompt else {}
            
            response = self.session.post(
                f"{self.endpoint}/analyze",
                files=files,
                data=data,
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
    
    def party_vibe(self, audio_path: str) -> dict:
        """
        Check if a track is good for a party
        
        Returns party rating (1-10) and verdict like:
        "🔥 BANGER - Drop this at peak time!" or "😴 Skip - Too chill"
        """
        with open(audio_path, 'rb') as f:
            files = {'file': f}
            
            response = self.session.post(
                f"{self.endpoint}/party-vibe",
                files=files,
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
    
    def transcribe(self, audio_path: str) -> dict:
        """Transcribe lyrics from a song"""
        with open(audio_path, 'rb') as f:
            files = {'file': f}
            
            response = self.session.post(
                f"{self.endpoint}/transcribe",
                files=files,
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
    
    def caption(self, audio_path: str) -> dict:
        """Generate social media caption for a track"""
        with open(audio_path, 'rb') as f:
            files = {'file': f}
            
            response = self.session.post(
                f"{self.endpoint}/caption",
                files=files,
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
    
    def health_check(self) -> dict:
        """Check if the service is healthy"""
        response = self.session.get(f"{self.endpoint}/health", timeout=10)
        response.raise_for_status()
        return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="🎵 MusicMind - AI Music Understanding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  musicmind analyze song.mp3
  musicmind party-vibe track.wav
  musicmind transcribe vocals.mp3
  musicmind caption beat.mp3
  musicmind health
        """
    )
    
    parser.add_argument(
        'command',
        choices=['analyze', 'party-vibe', 'transcribe', 'caption', 'health'],
        help='Command to run'
    )
    
    parser.add_argument(
        'audio_file',
        nargs='?',
        help='Path to audio file (required for all commands except health)'
    )
    
    parser.add_argument(
        '--prompt', '-p',
        help='Custom prompt for analyze command'
    )
    
    parser.add_argument(
        '--endpoint',
        default=os.getenv('MUSICMIND_ENDPOINT', MODAL_ENDPOINT),
        help='Custom Modal endpoint URL'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output raw JSON'
    )
    
    args = parser.parse_args()
    
    # Initialize client
    mind = MusicMind(endpoint=args.endpoint)
    
    # Health check
    if args.command == 'health':
        try:
            result = mind.health_check()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ {result['model']} is healthy")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            sys.exit(1)
        return
    
    # Audio file required for other commands
    if not args.audio_file:
        print("❌ Error: audio_file required for this command")
        sys.exit(1)
    
    if not Path(args.audio_file).exists():
        print(f"❌ Error: File not found: {args.audio_file}")
        sys.exit(1)
    
    try:
        if args.command == 'analyze':
            result = mind.analyze(args.audio_file, args.prompt)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("🎵 MUSIC ANALYSIS")
                print("=" * 50)
                print(result['analysis'])
                print(f"\n📊 Tempo: {result['tempo_bpm']:.1f} BPM")
                print(f"⏱️  Duration: {result['duration_seconds']:.1f}s")
        
        elif args.command == 'party-vibe':
            result = mind.party_vibe(args.audio_file)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("🎉 PARTY VIBE CHECK")
                print("=" * 50)
                print(result['analysis'])
                print(f"\n📊 Tempo: {result['tempo_bpm']:.1f} BPM")
        
        elif args.command == 'transcribe':
            result = mind.transcribe(args.audio_file)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("🎤 LYRICS TRANSCRIPTION")
                print("=" * 50)
                print(result['lyrics'])
        
        elif args.command == 'caption':
            result = mind.caption(args.audio_file)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("📱 SOCIAL MEDIA CAPTION")
                print("=" * 50)
                print(result['analysis'])
    
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
