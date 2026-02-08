#!/usr/bin/env python3
"""
MusicMind Demo - Test the music understanding agent
"""

import sys
sys.path.insert(0, '/home/ubuntu/clawd/skills/audio-flamingo')

from musicmind import MusicMind

def main():
    print("🎵 MusicMind Demo")
    print("=" * 50)
    
    mind = MusicMind()
    
    # Health check
    print("\n1. Health Check...")
    try:
        health = mind.health_check()
        print(f"   ✅ {health['model']} is ready!")
    except Exception as e:
        print(f"   ⚠️  Service not deployed yet: {e}")
        print("   Run: cd modal_deploy && modal deploy modal_app.py")
        return
    
    print("\n2. Available Commands:")
    print("   • analyze <file> - Full music analysis")
    print("   • party-vibe <file> - Party suitability check")
    print("   • transcribe <file> - Lyrics extraction")
    print("   • caption <file> - Social media caption")
    
    print("\n3. Example Usage:")
    print("   python3 musicmind.py analyze song.mp3")
    print("   python3 musicmind.py party-vibe drop.wav")
    
    print("\n✨ Ready to understand music with AI!")

if __name__ == "__main__":
    main()
