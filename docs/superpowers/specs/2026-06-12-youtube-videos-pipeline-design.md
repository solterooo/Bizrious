# YouTube Videos Pipeline — Design Spec

**Fecha:** 2026-06-12
**Estado:** Aprobado

---

## Objetivo

Crear un segundo pipeline (`youtube_videos.py`) independiente del de Shorts, que genere kits completos de producción para documentales de negocios en inglés de 10-30 minutos. El kit es un archivo `.md` listo para producir manualmente con herramientas gratuitas (Meta AI, Google Flow, ElevenLabs, Clipchamp).

---

## Contexto

Método A — `youtube_shorts.py` (antes `pipeline.py`): genera Shorts de 45-60s automáticamente con Pexels + ElevenLabs + Whisper + moviepy.

Método B — `youtube_videos.py`: genera el kit de producción completo para documentales largos. Semi-automático: Claude genera todo el contenido, la producción visual es manual.

---

## Arquitectura

```
Bizrious/
├── youtube_shorts.py          ← Método A (renombrado de pipeline.py)
├── youtube_videos.py          ← Método B (nuevo)
├── method_b/
│   └── outputs/               ← kits generados YYYY-MM-DD-<slug>.md
├── outputs/                   ← outputs de Shorts (sin cambios)
├── CLAUDE.md                  ← actualizado con nuevos nombres
└── CONTEXT.md                 ← actualizado con nuevos nombres
```

---

## Flujo de youtube_videos.py

```
1. Usuario define TOPIC + DURATION_RANGE en el script
2. Script llama a Claude API con mega-prompt adaptado
3. Claude genera el kit completo en inglés
4. Kit guardado en method_b/outputs/YYYY-MM-DD-<slug>.md
5. Script imprime la ruta del archivo generado
```

---

## Variables por video

```python
TOPIC          = "How Kodak Invented and Buried the Digital Camera"
DURATION_RANGE = "15-20"  # minutos — Claude ajusta el guión a este rango
```

---

## Contenido del kit generado

### 1. Títulos (5 opciones)
- Entre 50-70 caracteres
- Un título por enfoque: informativo, misterioso, revelación, emocional, dato impactante
- SEO optimizados para búsquedas en YouTube

### 2. Thumbnail
- Descripción detallada del diseño (fondo, texto, elemento visual, emoción)
- Prompt en inglés para generar con IA (Meta AI, Midjourney, Leonardo)
- Reglas: alto contraste, máximo 4-5 palabras, elemento dominante al 60% de la imagen

### 3. Descripción YouTube (SEO)
- Primeras 2-3 líneas gancho
- Párrafo con palabras clave integradas
- Timestamps ficticios en formato 00:00
- 5-8 hashtags relevantes
- CTA para suscribirse

### 4. Tags (20)
- Mix de tags exactos del tema, búsqueda amplia, inglés y español

### 5. Hook (primeros 30 segundos)
- Dato impactante o pregunta polémica de apertura
- Promesa de lo que aprenderá el espectador
- Sin "En este video..." ni saludos genéricos

### 6. Guión completo
- Estilo documental de negocios en inglés
- Frases cortas, pausas dramáticas marcadas con "..."
- Preguntas retóricas frecuentes
- Ganchos de continuidad al final de cada sección
- Re-gancho a mitad del video
- Revelación guardada para el final
- Prompts de imagen + animación cada 30-45s de narración:
  - `PROMPT IMAGEN`: descripción en inglés, estilo cinematic documentary, 8K
  - `PROMPT ANIMACIÓN`: movimiento de cámara, elementos en escena, duración, atmósfera

### 7. Notas de producción
- Música recomendada (Epidemic Sound, Artlist)
- Herramientas de imagen (Meta AI, Leonardo, Midjourney)
- Herramientas de animación (Google Flow, Kling, Runway)
- Ritmo de edición y pacing
- Coherencia visual entre escenas

---

## Mega-prompt adaptado

El script usa un prompt de sistema que instruye a Claude a actuar como equipo completo de producción YouTube: guionista, especialista en retención, experto SEO, copywriter viral y director de arte. Estilo documental de negocios en inglés, tono de narrador apasionado (no enciclopédico), anti-IA en el lenguaje.

Duración calculada como `DURATION_RANGE_min * 140` palabras mínimo y `DURATION_RANGE_max * 140` palabras máximo.

---

## Renombrados

| Antes | Después |
|-------|---------|
| `pipeline.py` | `youtube_shorts.py` |
| Referencias en `CLAUDE.md` | Actualizadas |
| Referencias en `CONTEXT.md` | Actualizadas |

---

## Lo que NO hace este pipeline

- No genera audio automáticamente (ElevenLabs es manual)
- No genera imágenes automáticamente (Meta AI / Leonardo es manual)
- No anima clips (Google Flow es manual)
- No monta el video final (Clipchamp es manual)

Estos pasos se añadirán en versiones futuras cuando el canal demuestre tracción.

---

## Primer video de prueba

**Tema:** How Kodak Invented and Buried the Digital Camera
**Duración objetivo:** 15-20 minutos
**Hechos clave a incluir:**
- Kodak inventó el primer prototipo de cámara digital en 1975 (Steve Sasson, ingeniero interno)
- La guardaron en un cajón para no canibalizar el negocio de película fotográfica
- Tenían más de 1,000 patentes de imagen digital
- Quebraron en enero de 2012 (Chapter 11)
- Hay memos internos que prueban que los directivos sabían décadas antes
