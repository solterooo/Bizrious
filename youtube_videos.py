import os
import re
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import anthropic

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
TOPIC          = "How Kodak Invented and Buried the Digital Camera"
DURATION_RANGE = "15-20"   # minutos

# ── Claude client ─────────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── Mega-prompt ───────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a complete YouTube production team: professional scriptwriter,
audience retention specialist, YouTube SEO expert, viral copywriter, and art director.

Your task is to create a complete production kit for a long-form documentary-style YouTube video
about business facts, corporate scandals, brand origin stories, or shocking business decisions.

Style guidelines:
- English language, documentary tone
- Passionate narrator, NOT encyclopedic or robotic
- Short sentences. Very short. Like this.
- Alternate short and longer sentences for natural rhythm
- Dramatic pauses marked with "..."
- Frequent rhetorical questions to keep viewers engaged
- Natural expressions: "And here's where it gets complicated", "Wait. Because this gets better", "Nobody saw it coming"
- NEVER use: "fascinating", "in conclusion", "it's important to note", "without a doubt", "in the realm of"
- Each section ends with a continuity hook
- Re-hook at the midpoint reminding the promise + new twist
- Most impactful revelation saved for the end, teased from the beginning

Word count: calculate as DURATION_MIN * 140 minimum and DURATION_MAX * 140 maximum words for the script narration."""


def build_user_prompt(topic: str, duration_range: str) -> str:
    parts = duration_range.split("-")
    dur_min, dur_max = int(parts[0]), int(parts[1])
    word_min = dur_min * 140
    word_max = dur_max * 140
    midpoint = dur_min + (dur_max - dur_min) // 2

    return f"""Create a complete YouTube production kit for this topic:

**TOPIC:** {topic}
**TARGET DURATION:** {duration_range} minutes ({word_min}–{word_max} words of narration)

Generate ALL of the following elements in this exact order:

---

## 1. TITLES (5 options)

Create 5 alternative titles. Each must:
- Be 50-70 characters
- Include a number, promise, or high emotional impact word when possible
- Be SEO optimized for YouTube search
- Generate curiosity or urgency without empty clickbait
- Cover different approaches: informative, mysterious, revelation, emotional, shocking stat

---

## 2. THUMBNAIL DESCRIPTION

Design the thumbnail following viral YouTube channel principles. Apply these rules:

- MAXIMUM 4-5 words on screen, bold font (Impact style), thick black or white outline
- Absolute high contrast: dark backgrounds (black, dark blue, dark red) with gold, white, or bright orange elements
- One dominant visual element occupying at least 60% of the image
- If human face: exaggerated expression (shock, fear, awe) with wide eyes
- Clear visual hierarchy: eye knows in under 1 second what to look at first
- Text and image tell different but complementary stories

Describe:
- Background and dominant colors
- Exact text on screen
- Main visual element
- Emotion/tension to convey
- General style
- Text vs image composition

Include the AI generation prompt:

> 🎨 **THUMBNAIL PROMPT:** `[detailed prompt in English: main visual element description, exact colors, dramatic lighting, text position, epic dark style, YouTube thumbnail style, bold sans-serif text space, high contrast, cinematic, ultra-detailed, 8K]`

---

## 3. YOUTUBE DESCRIPTION (SEO optimized)

Write the complete video description ready to paste in YouTube:
- First 2-3 hook lines (visible before "show more"), with main promise
- Development paragraph with naturally integrated keywords
- List of topics covered (with fictional timestamps in 00:00 format)
- Relevant hashtags at the end (5-8)
- CTA to subscribe and ring the bell

---

## 4. YOUTUBE TAGS (20 tags)

List of 20 relevant tags to maximize organic reach, mixing:
- Exact topic tags
- Related broad search tags
- Tags in English and Spanish

---

## 5. OPENING HOOK (first 30 seconds)

Write the exact script for the first 30 seconds. Must:
- Start with a shocking stat, question, or controversial claim
- Promise what the viewer will learn or discover
- Create tension or curiosity only resolved by watching the full video
- Sound completely human, conversational, and passionate — nothing robotic
- NOT start with "In this video..." or generic greetings

---

## 6. FULL SCRIPT (voice-over — {duration_range} minutes)

Write the complete script following these retention rules:

- Narrator sounds like a real person passionate about the topic, not an encyclopedia
- Include a surprising stat that invites comments ("Write in the comments if you knew this")
- Every section ends with a continuity hook
- Re-hook at minute {midpoint} approximately
- Most impactful revelations saved for the end, teased from the beginning

Include image + animation prompts every 30-45 seconds of narration:

> 🎨 **IMAGE PROMPT — Scene [N]: [descriptive title]**
> `[prompt in English, very detailed, ending always with: cinematic documentary, photorealistic, dramatic lighting, ultra-detailed, 8K]`
>
> 🎬 **ANIMATION PROMPT — Scene [N]:**
> `[prompt for AI video tools like Runway, Kling, Google Flow, or Luma. Describe: camera movement (slow zoom in, dolly forward, aerial drone shot, pan left, tracking shot), element movement in scene (people walking, fire flickering, dust particles floating), approximate duration (5 seconds), cinematic atmosphere]`

---

## 7. PRODUCTION NOTES

Include final recommendations about:
- Recommended music (style, references like Epidemic Sound, Artlist)
- AI image tools (Meta AI, Leonardo, Midjourney) with usage tips
- Animation tools (Google Flow, Kling, Runway, Pika) with tips on which to use per scene type
- Editing pace and pacing advice
- How to maintain visual consistency across all AI-generated images

---"""


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    return text[:60]


def generate_kit(topic: str, duration_range: str) -> str:
    print(f"Generating YouTube Video kit for: {topic}")
    print(f"Target duration: {duration_range} minutes")
    print("Calling Claude API...")

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": build_user_prompt(topic, duration_range)}
        ]
    )

    return message.content[0].text


def save_kit(topic: str, content: str) -> Path:
    today = date.today().strftime("%Y-%m-%d")
    slug = slugify(topic)
    filename = f"{today}-{slug}.md"

    output_dir = Path(__file__).parent / "method_b" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename
    output_path.write_text(content, encoding="utf-8")

    return output_path


def main():
    kit_content = generate_kit(TOPIC, DURATION_RANGE)
    output_path = save_kit(TOPIC, kit_content)

    print(f"\n✓ Kit generated successfully!")
    print(f"  Saved to: {output_path}")
    print(f"\nNext steps:")
    print(f"  1. Open {output_path}")
    print(f"  2. Review and adjust the script")
    print(f"  3. Generate images with Meta AI or Leonardo using the IMAGE PROMPTS")
    print(f"  4. Animate images with Google Flow using the ANIMATION PROMPTS")
    print(f"  5. Record voice-over with ElevenLabs")
    print(f"  6. Edit in Clipchamp")


if __name__ == "__main__":
    main()
