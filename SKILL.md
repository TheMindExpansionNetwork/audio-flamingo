---
name: musicmind
description: AI music understanding powered by Audio Flamingo 3. Analyze tracks, check party vibes, transcribe lyrics, and generate social media captions.
homepage: https://github.com/TheMindExpansionNetwork/audio-flamingo
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": { "bins": ["python3"] },
        "install": ["pip install requests"],
      },
  }
---

# 🎵 MusicMind

AI music understanding powered by NVIDIA's Audio Flamingo 3. Analyze tracks, check party vibes, transcribe lyrics, and generate social media captions.

## Overview

MusicMind brings state-of-the-art audio intelligence to your projects:

- **Music Analysis** - Genre, mood, tempo, instrumentation
- **Party Vibe Check** - Rate tracks for events (1-10)
- **Lyrics Transcription** - Extract lyrics from any song
- **Social Captions** - Generate catchy captions for posts
- **Multi-modal** - Understands speech, music, and sounds

Powered by **Audio Flamingo 3** (7B parameters) - the most capable open audio-language model.

## Quick Start

### 1. Deploy on Modal (one-time setup)

```bash
cd /home/ubuntu/clawd/skills/audio-flamingo/modal_deploy
modal deploy modal_app.py
```

This deploys a serverless A100 endpoint that:
- Scales to zero when not in use (saves money)
- Auto-scales under load
- Costs ~$2/hour only when active

### 2. Use the CLI

```bash
cd /home/ubuntu/clawd/skills/audio-flamingo

# Analyze a track
python3 musicmind.py analyze song.mp3

# Check party vibes
python3 musicmind.py party-vibe track.wav

# Transcribe lyrics
python3 musicmind.py transcribe vocals.mp3

# Generate social caption
python3 musicmind.py caption beat.mp3

# Health check
python3 musicmind.py health
```

### 3. Use in Python

```python
from musicmind import MusicMind

mind = MusicMind()

# Analyze music
result = mind.analyze("song.mp3")
print(result['analysis'])
print(f"Tempo: {result['tempo_bpm']:.1f} BPM")

# Party vibe check
vibe = mind.party_vibe("drop.wav")
print(vibe['analysis'])

# Transcribe lyrics
lyrics = mind.transcribe("song.mp3")
print(lyrics['lyrics'])
```

## Commands

| Command | Description | Example Output |
|---------|-------------|----------------|
| `analyze` | Full music analysis | Genre, mood, tempo, recommendations |
| `party-vibe` | Party suitability rating | "🔥 BANGER - Drop at peak time!" |
| `transcribe` | Extract lyrics | Full song lyrics |
| `caption` | Social media caption | "This drop hits different 🚀" |
| `health` | Service status | Model health check |

## Use Cases

### 🎉 Party/Event Planning
```bash
# Check if tracks are dancefloor-ready
musicmind party-vibe track1.mp3
musicmind party-vibe track2.mp3

# Output: "🔥 BANGER - Peak time energy!" or "😴 Skip - Too chill"
```

### 📱 Content Creation
```bash
# Generate captions for music posts
musicmind caption new-release.mp3

# Output: "Late night studio vibes 🌙🔊 This one's special"
```

### 🎵 Music Discovery
```bash
# Analyze unknown tracks
musicmind analyze mystery-song.mp3

# Output: Genre, similar artists, production notes
```

### 📝 Documentation
```bash
# Transcribe lyrics for covers/remixes
musicmind transcribe original.mp3 > lyrics.txt
```

## API Endpoints

Once deployed, these endpoints are available:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze` | POST | Full music analysis |
| `/party-vibe` | POST | Party suitability check |
| `/transcribe` | POST | Lyrics transcription |
| `/caption` | POST | Social media caption |
| `/health` | GET | Health check |

### Example API Call

```bash
curl -X POST "https://your-endpoint.modal.run/analyze" \
  -F "file=@song.mp3" \
  -F "prompt=Analyze the production quality"
```

## Configuration

### Environment Variables

```bash
# Custom endpoint (if you deployed separately)
export MUSICMIND_ENDPOINT="https://your-endpoint.modal.run"

# Use custom endpoint
musicmind analyze song.mp3 --endpoint $MUSICMIND_ENDPOINT
```

### JSON Output

```bash
# Get raw JSON for scripting
musicmind analyze song.mp3 --json | jq '.tempo_bpm'
```

## Model Capabilities

Audio Flamingo 3 understands:

**Music:**
- Genre classification
- Mood/emotion detection
- Instrument identification
- Tempo/key detection
- Production quality
- Similar artist recommendations

**Speech:**
- Lyrics transcription
- Speaker emotion
- Sarcasm detection
- Language identification

**Sounds:**
- Environmental sounds
- Event detection
- Audio quality assessment

## Deployment Options

### Option 1: Modal (Recommended)
Serverless, auto-scales, pay-per-use
```bash
modal deploy modal_deploy/modal_app.py
```

### Option 2: RunPod (Persistent)
Always-on GPU for high-frequency use
```bash
# Use RunPod manager script
./scripts/runpod-manager.sh deploy musicmind A100 audio-flamingo
```

### Option 3: Local (Development)
```bash
pip install transformers torch
python3 -c "from musicmind import MusicMind; ..."
```

## Cost Estimation

| Usage Pattern | Monthly Cost |
|--------------|--------------|
| Light (100 calls/month) | ~$5 |
| Medium (1000 calls/month) | ~$40 |
| Heavy (10k calls/month) | ~$300 |

*Based on Modal pricing with cold start optimizations*

## Files

```
audio-flamingo/
├── musicmind.py              # CLI tool
├── modal_deploy/
│   └── modal_app.py          # Modal deployment
├── SKILL.md                  # This file
└── update-from-upstream.sh   # Sync with NVIDIA
```

## Fork Info

This is a fork of NVIDIA's Audio Flamingo 3:
- **Our fork:** https://github.com/TheMindExpansionNetwork/audio-flamingo
- **Original:** https://github.com/NVIDIA/audio-flamingo
- **License:** NVIDIA OneWay Noncommercial License

To sync with upstream:
```bash
cd /home/ubuntu/clawd/skills/audio-flamingo
./update-from-upstream.sh
```

## Integration with MindBots

MusicMind can be used by other agents:

```python
# In another agent
from skills.audio_flamingo.musicmind import MusicMind

music_agent = MusicMind()

# Agent analyzes music for event planning
def plan_event_playlist(tracks):
    bangers = []
    for track in tracks:
        vibe = music_agent.party_vibe(track)
        if "BANGER" in vibe['analysis']:
            bangers.append(track)
    return bangers
```

## Roadmap

- [ ] Playlist generation based on vibe
- [ ] DJ mix analysis and recommendations
- [ ] Real-time party energy monitoring
- [ ] Integration with Spotify/Apple Music APIs
- [ ] Stem separation (vocals, drums, bass, etc.)

## Support

- GitHub: https://github.com/TheMindExpansionNetwork/audio-flamingo
- Model Card: https://huggingface.co/nvidia/audio-flamingo-3-hf
- Paper: https://arxiv.org/abs/2501.XXX

---

**Bring AI music intelligence to your projects!** 🎵🔥
