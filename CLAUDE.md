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
