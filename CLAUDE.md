# Bizrious — Instrucciones para Claude

## Qué es este proyecto

Pipeline Python que genera YouTube Shorts de temática **Business Facts** en inglés.
Cada Short se produce de principio a fin sin intervención manual salvo la aprobación del guión.

---

## Estructura obligatoria del guión (4 bloques)

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
| Revisar cambios a pipeline.py antes de pushear | `code-review` |

---

## Flujo de trabajo por sesión

1. **Tú propones un tema** con keywords estéticos para Pexels
2. **Claude genera el guión** directo a 45-50 segundos con la estructura de 4 bloques
3. **Tú apruebas o ajustas** el guión
4. **Se ejecuta el pipeline** — todo lo demás es automático

---

## Variables a cambiar en cada Short (pipeline.py)

```python
SHORT_NUMBER    = 17          # número del short
APPROVED_SCRIPT = """..."""   # guión aprobado
USER_KEYWORDS   = [...]       # keywords estéticos de Pexels (hasta 7)
BRAND_NAME      = "Nike"      # nombre de marca, o "" si no hay
```

Ejecutar con: `python3 pipeline.py`

---

## APIs configuradas (.env)

- `ANTHROPIC_API_KEY` — Claude `claude-sonnet-4-5-20250929`
- `ELEVENLABS_API_KEY` — TTS `eleven_multilingual_v2`, Voice ID `WTUK291rZZ9CLPCiFTfh`
- `PEXELS_API_KEY` — clips de video

## Dependencias

```
anthropic, elevenlabs, python-dotenv, moviepy, openai-whisper,
Pillow, requests, numpy, torch, imageio-ffmpeg
```
Python 3.9 — usar `Optional[X]`, no `X | None`
