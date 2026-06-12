# YouTube Videos Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear `youtube_videos.py` que genera kits de producción completos para documentales de negocios en inglés, y renombrar `pipeline.py` a `youtube_shorts.py` actualizando todas las referencias.

**Architecture:** Script Python independiente que llama a la API de Claude con un mega-prompt de producción documental, guarda el output como `.md` en `method_b/outputs/`. Renombrado de `pipeline.py` es un cambio de archivo + actualización de referencias en docs.

**Tech Stack:** Python 3.9, anthropic SDK, python-dotenv, pathlib

---

## File Map

| Archivo | Acción | Responsabilidad |
|---------|--------|----------------|
| `pipeline.py` | Renombrar → `youtube_shorts.py` | Pipeline de Shorts (sin cambios de lógica) |
| `youtube_videos.py` | Crear | Pipeline de Videos largos |
| `method_b/outputs/.gitkeep` | Crear | Carpeta de outputs del Método B |
| `CLAUDE.md` | Modificar | Actualizar nombres y añadir sección Método B |
| `CONTEXT.md` | Modificar | Actualizar referencias a pipeline.py |

---

### Task 1: Renombrar pipeline.py a youtube_shorts.py

**Files:**
- Rename: `pipeline.py` → `youtube_shorts.py`

- [ ] **Step 1: Renombrar el archivo**

```bash
mv /Users/soltero/Desktop/Bizrious/pipeline.py /Users/soltero/Desktop/Bizrious/youtube_shorts.py
```

- [ ] **Step 2: Verificar que existe con el nuevo nombre**

```bash
ls /Users/soltero/Desktop/Bizrious/youtube_shorts.py
```
Expected: `/Users/soltero/Desktop/Bizrious/youtube_shorts.py`

- [ ] **Step 3: Verificar que pipeline.py ya no existe**

```bash
ls /Users/soltero/Desktop/Bizrious/pipeline.py 2>&1
```
Expected: `No such file or directory`

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "Rename pipeline.py to youtube_shorts.py"
```

---

### Task 2: Actualizar referencias en CONTEXT.md

**Files:**
- Modify: `CONTEXT.md`

- [ ] **Step 1: Actualizar la referencia al archivo en CONTEXT.md**

Buscar en `CONTEXT.md` cualquier mención a `pipeline.py` y reemplazar por `youtube_shorts.py`. La línea actual dice:

```
**Ubicación:** `/Users/soltero/Desktop/Bizrious/pipeline.py`
```

Debe quedar:

```
**Ubicación:** `/Users/soltero/Desktop/Bizrious/youtube_shorts.py`
```

- [ ] **Step 2: Actualizar la sección "Cómo arrancar el Short 17"**

Buscar:
```
1. Abre `/Users/soltero/Desktop/Bizrious/pipeline.py`
```
Reemplazar por:
```
1. Abre `/Users/soltero/Desktop/Bizrious/youtube_shorts.py`
```

- [ ] **Step 3: Actualizar instrucción de ejecución**

Buscar:
```
3. Ejecuta: `python3 pipeline.py`
```
Reemplazar por:
```
3. Ejecuta: `python3 youtube_shorts.py`
```

- [ ] **Step 4: Verificar que no quedan referencias a pipeline.py**

```bash
grep -n "pipeline.py" /Users/soltero/Desktop/Bizrious/CONTEXT.md
```
Expected: sin output (ninguna línea encontrada)

- [ ] **Step 5: Commit**

```bash
git add CONTEXT.md
git commit -m "Update CONTEXT.md: pipeline.py → youtube_shorts.py"
```

---

### Task 3: Actualizar CLAUDE.md con ambos pipelines

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Reemplazar el contenido completo de CLAUDE.md**

El nuevo contenido debe ser exactamente:

```markdown
# Bizrious — Instrucciones para Claude

## Qué es este proyecto

Dos pipelines Python para crear contenido de YouTube sobre **Business Facts** en inglés:

- **YouTube Shorts** (`youtube_shorts.py`) — Shorts de 45-60 segundos, totalmente automático
- **YouTube Videos** (`youtube_videos.py`) — Documentales de 10-30 minutos, genera el kit de producción

---

## YouTube Shorts — Estructura del guión (4 bloques)

```
0–3s   → HOOK:        dato impactante o pregunta (nunca empieza con fecha)
3–8s   → CONTEXTO:    por qué importa
8–45s  → DESARROLLO:  la historia explicada
45–60s → REVELACIÓN:  dato sorpresa + pregunta al viewer
```

**Reglas de formato:**
- Números siempre en letras ("forty dollars", no "40 dollars")
- Sin etiquetas de escena en el texto final
- Duración objetivo: 45-50 segundos de lectura natural

---

## Skills — qué usar en cada paso

### Superpowers (archivos en `.claude/skills/superpowers/`)

| Cuando vayas a... | Usa esta skill |
|---|---|
| Idear tema + estructura de un Short nuevo | `superpowers:brainstorming` |
| Planear cambios al pipeline | `superpowers:writing-plans` |
| Ejecutar un plan con tareas independientes | `superpowers:subagent-driven-development` |
| Depurar errores del pipeline | `superpowers:systematic-debugging` |
| Añadir features con tests | `superpowers:test-driven-development` |
| Antes de declarar el Short listo | `superpowers:verification-before-completion` |
| Antes de hacer push a GitHub | `superpowers:requesting-code-review` + `superpowers:verification-before-completion` |
| Al recibir feedback sobre el pipeline | `superpowers:receiving-code-review` |
| Al terminar una rama de desarrollo | `superpowers:finishing-a-development-branch` |

### Skills del sistema (siempre disponibles, no requieren archivos)

| Cuando vayas a... | Usa esta skill |
|---|---|
| Investigar el hecho de negocio para un Short nuevo | `deep-research` |
| Escribir el guión del Short | `marketing:content-creation` |
| Hacer un borrador rápido del script | `marketing:draft-content` |
| Ejecutar el pipeline desde Claude | `run` |
| Confirmar que el video final es correcto | `verify` |
| Revisar cambios a youtube_shorts.py antes de pushear | `code-review` |

---

## Flujo de trabajo — YouTube Shorts

1. **Tú propones un tema** con keywords estéticos para Pexels
2. **Claude genera el guión** directo a 45-50 segundos con la estructura de 4 bloques
3. **Tú apruebas o ajustas** el guión
4. **Se ejecuta el pipeline** — todo lo demás es automático

### Variables a cambiar en cada Short (youtube_shorts.py)

```python
SHORT_NUMBER    = 17          # número del short
APPROVED_SCRIPT = """..."""   # guión aprobado
USER_KEYWORDS   = [...]       # keywords estéticos de Pexels (hasta 7)
BRAND_NAME      = "Nike"      # nombre de marca, o "" si no hay
```

Ejecutar con: `python3 youtube_shorts.py`

---

## Flujo de trabajo — YouTube Videos

1. **Tú propones un tema** para el documental
2. **Claude investiga** el tema con `deep-research`
3. **Se ejecuta el pipeline** — genera el kit completo como `.md`
4. **Tú produces el video** con Meta AI + Google Flow + ElevenLabs + Clipchamp

### Variables a cambiar en cada video (youtube_videos.py)

```python
TOPIC          = "How Kodak Invented and Buried the Digital Camera"
DURATION_RANGE = "15-20"   # minutos
```

Ejecutar con: `python3 youtube_videos.py`

El kit se guarda en `method_b/outputs/YYYY-MM-DD-<slug>.md`

---

## APIs configuradas (.env)

- `ANTHROPIC_API_KEY` — Claude `claude-sonnet-4-5-20250929`
- `ELEVENLABS_API_KEY` — TTS `eleven_multilingual_v2`, Voice ID `WTUK291rZZ9CLPCiFTfh`
- `PEXELS_API_KEY` — clips de video (solo Shorts)

## Dependencias

```
anthropic, elevenlabs, python-dotenv, moviepy, openai-whisper,
Pillow, requests, numpy, torch, imageio-ffmpeg
```
Python 3.9 — usar `Optional[X]`, no `X | None`
```

- [ ] **Step 2: Verificar que el archivo tiene el nuevo contenido**

```bash
head -5 /Users/soltero/Desktop/Bizrious/CLAUDE.md
```
Expected: `# Bizrious — Instrucciones para Claude`

```bash
grep "youtube_shorts\|youtube_videos" /Users/soltero/Desktop/Bizrious/CLAUDE.md | wc -l
```
Expected: número > 0 (hay referencias a ambos pipelines)

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "Update CLAUDE.md: add both pipelines, rename references"
```

---

### Task 4: Crear carpeta method_b/outputs/

**Files:**
- Create: `method_b/outputs/.gitkeep`

- [ ] **Step 1: Crear la carpeta con un .gitkeep**

```bash
mkdir -p /Users/soltero/Desktop/Bizrious/method_b/outputs
touch /Users/soltero/Desktop/Bizrious/method_b/outputs/.gitkeep
```

- [ ] **Step 2: Verificar estructura**

```bash
ls /Users/soltero/Desktop/Bizrious/method_b/outputs/
```
Expected: `.gitkeep`

- [ ] **Step 3: Commit**

```bash
git add method_b/outputs/.gitkeep
git commit -m "Add method_b/outputs directory for YouTube Videos kits"
```

---

### Task 5: Crear youtube_videos.py

**Files:**
- Create: `youtube_videos.py`

- [ ] **Step 1: Crear el archivo con el siguiente contenido exacto**

```python
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
- Re-hook at minute {dur_min + (dur_max - dur_min) // 2} approximately
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
```

- [ ] **Step 2: Verificar que el archivo existe**

```bash
ls /Users/soltero/Desktop/Bizrious/youtube_videos.py
```
Expected: `/Users/soltero/Desktop/Bizrious/youtube_videos.py`

- [ ] **Step 3: Verificar que importa correctamente (sin errores de sintaxis)**

```bash
python3 -c "import ast; ast.parse(open('/Users/soltero/Desktop/Bizrious/youtube_videos.py').read()); print('Syntax OK')"
```
Expected: `Syntax OK`

- [ ] **Step 4: Commit**

```bash
git add youtube_videos.py
git commit -m "Add youtube_videos.py — YouTube Videos pipeline (Method B)"
```

---

### Task 6: Push a GitHub

- [ ] **Step 1: Verificar commits pendientes**

```bash
git log --oneline origin/main..HEAD
```
Expected: los commits de las tareas 1-5

- [ ] **Step 2: Push**

```bash
git push origin main
```
Expected: `main -> main` sin errores

- [ ] **Step 3: Verificar en GitHub**

```bash
git log --oneline -6
```
Expected: todos los commits nuevos aparecen
