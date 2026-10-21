"""
Procedural Sound Effects Generator for AI Disaster Rescue Robot.
Synthesizes retro audio cues in-memory using NumPy and Pygame mixer
without requiring external audio files.
"""

import numpy as np

# Audio state
_sound_cache = {}
_audio_enabled = False


def init_audio():
    """Initializes Pygame audio mixer safely."""
    global _audio_enabled
    try:
        import pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init(44100, -16, 2, 512)
        _audio_enabled = True
        _build_sounds()
    except Exception as e:
        print(f"Audio disabled or unavailable: {e}")
        _audio_enabled = False


def _build_sounds():
    """Generates procedural sound effects."""
    if not _audio_enabled:
        return
    import pygame
    sr = 44100

    try:
        # 1. Step Tick: subtle low click
        t = np.linspace(0, 0.04, int(sr * 0.04), False)
        wave = np.sin(2 * np.pi * 320 * t) * np.linspace(1, 0, len(t))
        stereo = np.column_stack((wave, wave))
        _sound_cache["step"] = pygame.sndarray.make_sound((stereo * 4000).astype(np.int16))

        # 2. Rescue Chime: C5 -> G5 ascending arpeggio
        dur = 0.25
        t = np.linspace(0, dur, int(sr * dur), False)
        h = len(t) // 2
        tone1 = np.sin(2 * np.pi * 523.25 * t[:h])  # C5
        tone2 = np.sin(2 * np.pi * 783.99 * t[h:])  # G5
        wave = np.concatenate([tone1, tone2])
        env = np.linspace(1, 0, len(wave))
        stereo = np.column_stack((wave * env, wave * env))
        _sound_cache["rescue"] = pygame.sndarray.make_sound((stereo * 12000).astype(np.int16))

        # 3. Victory Fanfare: C5 -> E5 -> G5 -> C6
        dur = 0.5
        t = np.linspace(0, dur, int(sr * dur), False)
        q = len(t) // 4
        tone1 = np.sin(2 * np.pi * 523.25 * t[:q])
        tone2 = np.sin(2 * np.pi * 659.25 * t[q:2*q])
        tone3 = np.sin(2 * np.pi * 783.99 * t[2*q:3*q])
        tone4 = np.sin(2 * np.pi * 1046.50 * t[3*q:])
        wave = np.concatenate([tone1, tone2, tone3, tone4])
        env = np.linspace(1, 0, len(wave))
        stereo = np.column_stack((wave * env, wave * env))
        _sound_cache["victory"] = pygame.sndarray.make_sound((stereo * 14000).astype(np.int16))

        # 4. Wait / Conflict notification: soft double tap
        dur = 0.12
        t = np.linspace(0, dur, int(sr * dur), False)
        wave = np.sin(2 * np.pi * 440 * t) * np.linspace(0.8, 0, len(t))
        stereo = np.column_stack((wave, wave))
        _sound_cache["wait"] = pygame.sndarray.make_sound((stereo * 8000).astype(np.int16))

        # 5. Tactical Radio Chirp (Walkie-talkie click)
        dur = 0.08
        t = np.linspace(0, dur, int(sr * dur), False)
        h = len(t) // 2
        tone1 = np.sin(2 * np.pi * 880 * t[:h])
        tone2 = np.sin(2 * np.pi * 1760 * t[h:])
        wave = np.concatenate([tone1, tone2])
        env = np.linspace(1, 0, len(wave))
        stereo = np.column_stack((wave * env, wave * env))
        _sound_cache["radio"] = pygame.sndarray.make_sound((stereo * 9000).astype(np.int16))

    except Exception as e:
        print(f"Could not build procedural sounds: {e}")


def play_sound(name: str):
    """Plays a cached procedural sound effect if audio is enabled."""
    if _audio_enabled and name in _sound_cache:
        try:
            _sound_cache[name].play()
        except Exception:
            pass
