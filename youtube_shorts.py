import os
import re
import json
import requests
import textwrap
import numpy as np
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import anthropic
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.VideoClip import ImageClip
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
VOICE_ID           = "WTUK291rZZ9CLPCiFTfh"
MODEL_TTS          = "eleven_multilingual_v2"
NUM_CLIPS          = 7
SKIP_SECONDS       = 18
MAX_DURATION       = 60
TARGET_W, TARGET_H = 1080, 1920

# Subtitle design
WORDS_PER_CAPTION  = 3          # words shown at once
FONT_SIZE          = 90
CAPTION_Y_RATIO    = 0.72       # vertical position (0=top, 1=bottom)

OUTPUT_AUDIO_PATH  = Path("outputs/audio")
OUTPUT_VIDEO_PATH  = Path("outputs/videos_raw")
OUTPUT_FINAL_PATH  = Path("outputs/final")
SHORT_NUMBER       = 16
OUTPUT_AUDIO_FILE  = OUTPUT_AUDIO_PATH / f"business_short_{SHORT_NUMBER}.mp3"
OUTPUT_FINAL_FILE  = OUTPUT_FINAL_PATH / f"short_bizrious_{SHORT_NUMBER}_final.mp4"
OUTPUT_VIDEO_PATH  = OUTPUT_VIDEO_PATH / f"short_{SHORT_NUMBER}"

# Brand logo config — set BRAND_NAME to trigger logo clip insertion.
# Drop a PNG/JPG into assets/logos/<brand_name_lowercase>.png for best results.
# If no file is found, a text card is generated automatically.
BRAND_NAME   = "Cinnabon"
ASSETS_PATH  = Path("assets/logos")

APPROVED_SCRIPT = """Cinnabon deliberately pumps scent through shopping mall ventilation systems to hijack your brain before you even see the store.
It is not an accident. Cinnabon places its ovens at the front of every location specifically to maximize scent exposure. They use pure cinnamon extract — one of the most powerful appetite triggers known to neuroscience.
The smell travels dozens of meters through mall corridors. Before your eyes find the store, your brain has already released dopamine and activated hunger signals. You weren't hungry. Now you are. Biologically.
This is called scent marketing, and Cinnabon has perfected it into a science. Their entire business model depends on impulse purchases driven entirely by smell.
You didn't choose to stop. Your nervous system did. Next time you find yourself walking toward a Cinnabon you didn't plan to visit — now you know exactly why."""

TOPIC = "Yahoo rejected buying Google for one million dollars"

# Optional: your own Pexels search keywords (aesthetic/cinematic).
# Fill these when you have a vision for the visuals — Claude will supplement
# any remaining slots up to NUM_CLIPS. Leave empty to let Claude generate all.
USER_KEYWORDS: list[str] = [
    "cinnamon sticks close up macro warm",
    "steam rising baked goods cinematic",
    "brain neurons light cinematic",
    "shopping mall crowd busy aerial",
    "mall corridor people walking cinematic",
    "cinnabon oven front store display",
    "ventilation system building industrial",
]

# ── Prompts ───────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You write scripts for YouTube Shorts about business facts. "
    "Your output must be ONLY the words that will be spoken aloud — "
    "no introductions, no sound cues, no brackets like [Music] or [Pause], "
    "no stage directions, no extra commentary. "
    "Structure EVERY script in exactly these 4 timed blocks:\n"
    "- 0-3s   HOOK: shocking fact or intriguing question. Never start with a date or 'In year X'.\n"
    "- 3-8s   CONTEXT: why this fact matters.\n"
    "- 8-45s  DEVELOPMENT: the full story or data explained.\n"
    "- 45-60s REVELATION: the surprising final fact + a direct question to the viewer to drive engagement.\n"
    "Additional rules:\n"
    "- Use digits for numbers when it sounds cleaner aloud (e.g. '17 hours', not 'seventeen hours').\n"
    "- Total read time must be 55-60 seconds at a natural pace."
)

LOGO_POSITION_PROMPT = """You are a video editor for YouTube Shorts.

Given the script and a list of {n} video clips (indexed 0 to {n_minus_1}), decide the single best position
to insert a brand clip for "{brand}".

Rules:
- The brand clip should feel like a natural reveal or punctuation moment
- Good positions: right after the hook (index 1-2), or just before the final question (second-to-last index)
- Return ONLY a single integer (the index where the brand clip will be inserted). Nothing else.

Script:
{script}

Clip keywords:
{keywords}"""

KEYWORDS_PROMPT = """You are a cinematographic art director for YouTube Shorts.

Split the script below into exactly {n} chronological segments of roughly equal length.
For each segment write ONE Pexels search keyword that is abstract, cinematic, and atmospheric.
Examples: 'vintage 1970s office dark aesthetic', 'artist sketching paper close up portrait',
'counting dollar bills texture slow motion', 'luxury business stock charts dark'.
NEVER: people smiling at camera, fake handshakes, generic office.

Return a valid JSON array of exactly {n} strings. No explanation, no markdown, just the array.

Script:
{script}"""


# ── Step 1: Script ────────────────────────────────────────────────────────────
def generate_script() -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Write a YouTube Short script about: {TOPIC}"}],
    )
    return msg.content[0].text


# ── Step 2: Audio ─────────────────────────────────────────────────────────────
def generate_audio(script: str) -> None:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=script,
        model_id=MODEL_TTS,
    )
    save(audio, str(OUTPUT_AUDIO_FILE))


# ── Step 3: Keywords ──────────────────────────────────────────────────────────
def extract_keywords(script: str, n: int) -> list[str]:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=256,
        messages=[{"role": "user", "content": KEYWORDS_PROMPT.format(n=n, script=script)}],
    )
    raw = msg.content[0].text.strip()
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)[:n]


# ── Step 4: Download videos (top-3 per keyword → Claude picks best) ──────────
CLIP_PICK_PROMPT = """You are a video editor selecting the best stock footage for a YouTube Short.

Keyword: "{keyword}"
Script context: "{context}"

Choose the single best video from the candidates below based on visual quality,
cinematic feel, and relevance. Return ONLY the index number (0, 1, or 2). Nothing else.

Candidates:
{candidates}"""


def pick_best_clip(keyword: str, context: str, candidates: list[dict]) -> int:
    desc = "\n".join(
        f"{i}: duration={c['duration']}s  size={c['width']}x{c['height']}  url_hint={c['url'][-40:]}"
        for i, c in enumerate(candidates)
    )
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4,
        messages=[{"role": "user", "content": CLIP_PICK_PROMPT.format(
            keyword=keyword, context=context, candidates=desc
        )}],
    )
    try:
        return int(msg.content[0].text.strip()[0])
    except (ValueError, IndexError):
        return 0


def download_pexels_videos(keywords: list[str], script: str) -> list[Path]:
    headers    = {"Authorization": os.environ["PEXELS_API_KEY"]}
    downloaded = []
    # Split script into segments to give Claude context per keyword
    seg_len = max(1, len(script) // len(keywords))

    for i, keyword in enumerate(keywords):
        print(f"  [{i+1}/{len(keywords)}] '{keyword}'")
        resp = requests.get(
            "https://api.pexels.com/videos/search",
            headers=headers,
            params={"query": keyword, "orientation": "portrait", "per_page": 10},
        )
        resp.raise_for_status()
        results = resp.json().get("videos", [])
        if not results:
            print(f"  ⚠  No results, skipping.")
            continue

        # Collect up to 3 candidates with usable files
        candidates = []
        candidate_urls = []
        for video in results:
            files = sorted(
                [f for f in video["video_files"] if f.get("quality") in ("hd", "sd")],
                key=lambda f: f.get("width", 0), reverse=True,
            )
            if files:
                candidates.append({
                    "duration": video.get("duration", 0),
                    "width":    files[0].get("width", 0),
                    "height":   files[0].get("height", 0),
                    "url":      files[0]["link"],
                })
                candidate_urls.append(files[0]["link"])
            if len(candidates) == 3:
                break

        if not candidates:
            continue

        # Ask Claude to pick the best one
        context   = script[i * seg_len:(i + 1) * seg_len]
        best_idx  = pick_best_clip(keyword, context, candidates) if len(candidates) > 1 else 0
        best_idx  = min(best_idx, len(candidates) - 1)
        video_url = candidate_urls[best_idx]
        print(f"  ✓  Claude picked candidate {best_idx} of {len(candidates)}")

        safe = re.sub(r"[^a-z0-9_]", "_", keyword.lower())[:40]
        dest = OUTPUT_VIDEO_PATH / f"clip_{i+1:02d}_{safe}.mp4"
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"  ✓  Saved: {dest.name}")
        downloaded.append(dest)
    return downloaded


# ── Step 5: Transcribe with Whisper ──────────────────────────────────────────
def transcribe_audio(audio_path: Path) -> list[dict]:
    """Returns list of word-level segments: [{word, start, end}, ...]"""
    import whisper
    import imageio_ffmpeg
    import tempfile
    import stat

    # Whisper calls 'ffmpeg' by name; imageio_ffmpeg has the binary but with a
    # platform-specific filename. Create a symlink called 'ffmpeg' in a temp dir
    # and prepend that dir to PATH so Whisper finds it.
    ffmpeg_exe  = imageio_ffmpeg.get_ffmpeg_exe()
    tmp_bin_dir = Path(tempfile.mkdtemp())
    ffmpeg_link = tmp_bin_dir / "ffmpeg"
    if not ffmpeg_link.exists():
        ffmpeg_link.symlink_to(ffmpeg_exe)
        ffmpeg_link.chmod(ffmpeg_link.stat().st_mode | stat.S_IEXEC)
    os.environ["PATH"] = str(tmp_bin_dir) + os.pathsep + os.environ.get("PATH", "")

    print("  Loading Whisper model (base)...")
    model = whisper.load_model("base")
    print("  Transcribing audio...")
    result = model.transcribe(
        str(audio_path),
        word_timestamps=True,
        language="en",
        fp16=False,
    )
    words = []
    for seg in result["segments"]:
        for w in seg.get("words", []):
            words.append({
                "word":  w["word"].strip(),
                "start": w["start"],
                "end":   w["end"],
            })
    print(f"  ✓  {len(words)} words transcribed")
    return words


def group_words(words: list[dict], n: int = WORDS_PER_CAPTION) -> list[dict]:
    """Bundle words into caption groups of n words, auto-reducing if text is too wide."""
    font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"
    fallback  = "/System/Library/Fonts/Helvetica.ttc"
    try:
        font = ImageFont.truetype(font_path, FONT_SIZE)
    except OSError:
        font = ImageFont.truetype(fallback, FONT_SIZE)

    max_text_w = TARGET_W - 80  # 40px safe margin each side

    captions = []
    i = 0
    while i < len(words):
        chunk = words[i:i + n]
        text  = " ".join(w["word"] for w in chunk).upper()

        # Measure rendered width — if too wide, drop to n-1 words
        dummy = Image.new("RGBA", (1, 1))
        bbox  = ImageDraw.Draw(dummy).textbbox((0, 0), text, font=font)
        tw    = bbox[2] - bbox[0]

        if tw > max_text_w and len(chunk) > 1:
            chunk = words[i:i + n - 1]
            text  = " ".join(w["word"] for w in chunk).upper()

        captions.append({
            "text":  text,
            "start": chunk[0]["start"],
            "end":   chunk[-1]["end"],
        })
        i += len(chunk)
    return captions


# ── Step 6: Render subtitles ──────────────────────────────────────────────────
def make_caption_clip(text: str, duration: float) -> ImageClip:
    """Create a transparent ImageClip with bold white text + black stroke."""
    font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"
    fallback   = "/System/Library/Fonts/Helvetica.ttc"

    try:
        font = ImageFont.truetype(font_path, FONT_SIZE)
    except OSError:
        font = ImageFont.truetype(fallback, FONT_SIZE)

    # Measure text size
    dummy = Image.new("RGBA", (1, 1))
    draw  = ImageDraw.Draw(dummy)
    bbox  = draw.textbbox((0, 0), text, font=font)
    tw    = bbox[2] - bbox[0] + 20
    th    = bbox[3] - bbox[1] + 20

    # Draw on transparent canvas
    img  = Image.new("RGBA", (tw + 20, th + 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Black stroke (outline)
    stroke = 6
    x, y = 10 - bbox[0], 10 - bbox[1]
    for dx in range(-stroke, stroke + 1):
        for dy in range(-stroke, stroke + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 255))

    # White fill
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    frame = np.array(img)
    clip  = (
        ImageClip(frame, duration=duration)
        .with_position(("center", int(TARGET_H * CAPTION_Y_RATIO)))
    )
    return clip


def build_subtitle_clips(captions: list[dict]) -> list[ImageClip]:
    clips = []
    for cap in captions:
        dur = max(cap["end"] - cap["start"], 0.05)
        c   = make_caption_clip(cap["text"], dur).with_start(cap["start"])
        clips.append(c)
    return clips


# ── Step 7a: Brand clip (Pexels) ──────────────────────────────────────────────
def decide_logo_position(script: str, keywords: list[str], brand: str) -> int:
    n = len(keywords) + 1  # total clips after insertion
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8,
        messages=[{"role": "user", "content": LOGO_POSITION_PROMPT.format(
            n=n,
            n_minus_1=n - 1,
            brand=brand,
            script=script,
            keywords="\n".join(f"{i}: {k}" for i, k in enumerate(keywords)),
        )}],
    )
    try:
        return int(msg.content[0].text.strip())
    except ValueError:
        return 1  # fallback: insert after hook


def download_brand_clip(brand: str) -> Optional[Path]:
    """Search Pexels for a brand-specific video clip and download it."""
    headers  = {"Authorization": os.environ["PEXELS_API_KEY"]}
    # Two attempts: specific brand query first, then a generic product shot
    queries  = [f"{brand} can product close up", f"{brand} logo brand identity"]

    for query in queries:
        print(f"  Searching Pexels for brand clip: '{query}'")
        resp = requests.get(
            "https://api.pexels.com/videos/search",
            headers=headers,
            params={"query": query, "orientation": "portrait", "per_page": 8},
        )
        resp.raise_for_status()
        results = resp.json().get("videos", [])
        if not results:
            continue

        for video in results:
            files = sorted(
                [f for f in video["video_files"] if f.get("quality") in ("hd", "sd")],
                key=lambda f: f.get("width", 0), reverse=True,
            )
            if not files:
                continue

            safe = re.sub(r"[^a-z0-9_]", "_", brand.lower())
            dest = OUTPUT_VIDEO_PATH / f"brand_{safe}.mp4"
            with requests.get(files[0]["link"], stream=True) as r:
                r.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"  ✓  Brand clip saved: {dest.name}")
            return dest

    print(f"  ⚠  No brand clip found for '{brand}', skipping.")
    return None


# ── Step 7b: Edit & export ─────────────────────────────────────────────────────
def crop_to_916(clip):
    scale = max(TARGET_W / clip.w, TARGET_H / clip.h)
    new_w, new_h = int(clip.w * scale), int(clip.h * scale)
    clip = clip.resized((new_w, new_h))
    x1 = (new_w - TARGET_W) / 2
    y1 = (new_h - TARGET_H) / 2
    return clip.cropped(x1=x1, y1=y1, x2=x1 + TARGET_W, y2=y1 + TARGET_H)


def speech_aligned_boundaries(words: list[dict], n: int, total_duration: float) -> list[tuple]:
    """
    Divide word timestamps into n segments aligned to actual speech.
    Rhythm weights: HOOK clips (first 2) get fewer words → shorter, faster cuts.
    REVELATION clip (last 1) also gets fewer words → punchy ending.
    DEVELOPMENT clips (middle) get more words → slower, let the story breathe.
    """
    if not words:
        dur = total_duration / n
        return [(i * dur, dur) for i in range(n)]

    # Weight per clip: hook=0.7, dev=1.0, revelation=0.8
    weights = []
    for i in range(n):
        if i < 2:
            weights.append(0.7)    # HOOK — fast
        elif i >= n - 1:
            weights.append(0.8)    # REVELATION — punchy
        else:
            weights.append(1.0)    # DEVELOPMENT — normal

    total_weight  = sum(weights)
    words_per_unit = len(words) / total_weight

    boundaries = []
    word_cursor = 0
    for i, w in enumerate(weights):
        word_count     = max(1, round(w * words_per_unit))
        first_word_idx = min(word_cursor, len(words) - 1)
        last_word_idx  = min(word_cursor + word_count - 1, len(words) - 1)

        seg_start = words[first_word_idx]["start"]
        if i < n - 1:
            next_idx  = min(word_cursor + word_count, len(words) - 1)
            seg_dur   = words[next_idx]["start"] - seg_start
        else:
            seg_dur = total_duration - seg_start

        boundaries.append((seg_start, max(seg_dur, 0.1)))
        word_cursor += word_count

    return boundaries


def edit_video(video_paths: list[Path], audio_path: Path,
               subtitle_clips: list[ImageClip], words: list[dict],
               brand_clip: Optional[Path] = None, brand_position: int = 1) -> None:
    audio          = AudioFileClip(str(audio_path))
    voice_duration = min(audio.duration, MAX_DURATION)
    if audio.duration > MAX_DURATION:
        print(f"  ⚠  Audio trimmed from {audio.duration:.1f}s to {MAX_DURATION}s")
        audio = audio.subclipped(0, MAX_DURATION)

    # ── Insert brand clip into the sequence at the decided position ──────────
    if brand_clip and brand_clip.exists():
        video_paths = list(video_paths)
        pos = max(0, min(brand_position, len(video_paths)))
        video_paths.insert(pos, brand_clip)
        print(f"  ✓  Brand clip inserted at position {pos}")

    # ── Align clips to actual speech timestamps ───────────────────────────────
    boundaries = speech_aligned_boundaries(words, len(video_paths), voice_duration)
    print(f"  Audio: {voice_duration:.2f}s  |  {len(video_paths)} clips (speech-aligned)")

    clips = []
    for i, (path, (seg_start, seg_dur)) in enumerate(zip(video_paths, boundaries)):
        raw   = VideoFileClip(str(path))
        skip  = SKIP_SECONDS if raw.duration > SKIP_SECONDS + seg_dur else 0
        avail = raw.duration - skip

        if avail < seg_dur:
            seg   = raw.subclipped(skip, raw.duration)
            times = int(seg_dur / seg.duration) + 1
            seg   = concatenate_videoclips([seg] * times)
        else:
            seg = raw.subclipped(skip, skip + seg_dur)

        seg = seg.subclipped(0, seg_dur)
        seg = crop_to_916(seg)
        clips.append(seg)
        print(f"  ✓  Clip {i+1}: {path.name}  starts at {seg_start:.2f}s  dur {seg_dur:.2f}s")

    base  = concatenate_videoclips(clips).with_audio(audio)
    final = CompositeVideoClip([base] + subtitle_clips)

    print(f"\n  Exporting → {OUTPUT_FINAL_FILE}")
    final.write_videofile(
        str(OUTPUT_FINAL_FILE),
        codec="libx264",
        audio_codec="aac",
        fps=30,
        preset="fast",
        logger="bar",
    )

    audio.close()
    for c in clips:
        c.close()
    base.close()
    final.close()


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUTPUT_AUDIO_PATH.mkdir(parents=True, exist_ok=True)
    OUTPUT_VIDEO_PATH.mkdir(parents=True, exist_ok=True)
    OUTPUT_FINAL_PATH.mkdir(parents=True, exist_ok=True)

    print("━" * 60)
    print("STEP 1 — Script (approved)")
    print("━" * 60)
    script = APPROVED_SCRIPT
    print("\n" + script + "\n")

    print("━" * 60)
    print("STEP 2 — Generating voiceover with ElevenLabs")
    print("━" * 60)
    generate_audio(script)
    print(f"✓  Audio saved: {OUTPUT_AUDIO_FILE}\n")

    print("━" * 60)
    print(f"STEP 3 — Building {NUM_CLIPS} cinematic keywords")
    print("━" * 60)
    if USER_KEYWORDS:
        keywords = list(USER_KEYWORDS)
        remaining = NUM_CLIPS - len(keywords)
        if remaining > 0:
            print(f"  Using {len(keywords)} user keywords, Claude fills {remaining} more...")
            claude_keywords = extract_keywords(script, remaining)
            keywords += claude_keywords
        else:
            keywords = keywords[:NUM_CLIPS]
        print(f"  Source: {len(USER_KEYWORDS)} user + {NUM_CLIPS - len(USER_KEYWORDS)} Claude")
    else:
        print(f"  Claude generating all {NUM_CLIPS} keywords...")
        keywords = extract_keywords(script, NUM_CLIPS)
    for k in keywords:
        print(f"  • {k}")
    print()

    print("━" * 60)
    print("STEP 4 — Downloading portrait clips from Pexels")
    print("━" * 60)
    videos = download_pexels_videos(keywords, script)
    print(f"\n✓  {len(videos)} clips ready\n")
    if not videos:
        print("✗  No videos downloaded. Aborting.")
        return

    print("━" * 60)
    print("STEP 5 — Transcribing audio with Whisper")
    print("━" * 60)
    words    = transcribe_audio(OUTPUT_AUDIO_FILE)
    captions = group_words(words, WORDS_PER_CAPTION)
    print(f"  ✓  {len(captions)} caption groups\n")

    print("━" * 60)
    print("STEP 6 — Building subtitle clips")
    print("━" * 60)
    subtitle_clips = build_subtitle_clips(captions)
    print(f"  ✓  {len(subtitle_clips)} subtitle clips rendered\n")

    # ── Brand clip (optional) ─────────────────────────────────────────────────
    brand_clip     = None
    brand_position = 1
    if BRAND_NAME:
        print("━" * 60)
        print(f"STEP 7a — Downloading brand clip for '{BRAND_NAME}'")
        print("━" * 60)
        brand_clip = download_brand_clip(BRAND_NAME)
        if brand_clip:
            print(f"  Asking Claude where to insert the brand clip...")
            brand_position = decide_logo_position(script, keywords, BRAND_NAME)
            print(f"  ✓  Claude chose position {brand_position}\n")

    print("━" * 60)
    print("STEP 7b — Editing and exporting final video")
    print("━" * 60)
    edit_video(videos, OUTPUT_AUDIO_FILE, subtitle_clips, words,
               brand_clip=brand_clip, brand_position=brand_position)
    print(f"\n✅  DONE → {OUTPUT_FINAL_FILE}")

    # ── Cleanup: delete all raw clips after export ────────────────────────────
    print("\nCleaning up raw clips...")
    deleted = 0
    for f in OUTPUT_VIDEO_PATH.glob("*.mp4"):
        f.unlink()
        deleted += 1
    print(f"  ✓  {deleted} raw clips deleted from {OUTPUT_VIDEO_PATH}/")


if __name__ == "__main__":
    main()
