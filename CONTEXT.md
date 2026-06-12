# Bizrious — YouTube Shorts Pipeline
**Última actualización:** 2026-06-11  
**Shorts completados:** 16

---

## ¿Qué es este proyecto?

Pipeline 100% automatizado en Python que genera YouTube Shorts de temática **Business Facts** en inglés. Cada Short se produce de principio a fin sin intervención manual salvo la aprobación del guión.

---

## Flujo de trabajo

1. **Tú propones un tema** con keywords estéticos para Pexels
2. **Claude genera el guión** directo a 45-50 segundos con la estructura de 4 bloques
3. **Tú apruebas o ajustas** el guión
4. **Se ejecuta el pipeline** — todo lo demás es automático

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

## El pipeline — youtube_shorts.py

**Ubicación:** `/Users/soltero/Desktop/Bizrious/youtube_shorts.py`

### Variables que cambias en cada Short

```python
SHORT_NUMBER    = 17          # número del short
APPROVED_SCRIPT = """..."""   # guión aprobado por el usuario
USER_KEYWORDS   = [...]       # tus keywords estéticos de Pexels (hasta 7)
BRAND_NAME      = "Nike"      # nombre de marca para brand clip, o "" si no hay
```

### Lo que hace automáticamente

| Paso | Herramienta | Descripción |
|------|------------|-------------|
| 1 | — | Usa el `APPROVED_SCRIPT` directamente |
| 2 | ElevenLabs | Genera voz con Voice ID `WTUK291rZZ9CLPCiFTfh`, modelo `eleven_multilingual_v2` |
| 3 | Claude | Combina tus keywords con las que genera Claude hasta completar 7 |
| 4 | Pexels | Descarga 3 candidatos por keyword → Claude elige el mejor → 7 clips finales |
| 5 | Whisper | Transcribe el audio con timestamps palabra por palabra |
| 6 | moviepy + PIL | Renderiza subtítulos Impact blanco/borde negro, 3 palabras, auto-reduce si se sale del frame |
| 7a | Pexels | Si hay `BRAND_NAME`, descarga un clip de la marca y Claude decide dónde insertarlo |
| 7b | moviepy | Edita el video final: clips alineados al speech, ritmo variable, formato 1080×1920, hard cap 60s |
| 8 | — | Borra todos los clips crudos de `outputs/videos_raw/short_N/` |

### Outputs

```
outputs/
├── audio/          business_short_N.mp3
├── videos_raw/     short_N/  (se borra tras exportar)
└── final/          short_bizrious_N_final.mp4  ← producto final
```

---

## Configuración de APIs

**Archivo:** `/Users/soltero/Desktop/Bizrious/.env`

```
ANTHROPIC_API_KEY=...
ELEVENLABS_API_KEY=...
PEXELS_API_KEY=...
```

**Modelos en uso:**
- Claude: `claude-sonnet-4-5-20250929`
- ElevenLabs TTS: `eleven_multilingual_v2`
- Whisper: `base` (local, sin coste)

---

## Mejoras implementadas

- **Calidad visual:** 3 candidatos por keyword, Claude elige el mejor según contexto del guión
- **Subtítulos:** auto-reducen de 3 a 2 palabras si el texto se sale del frame (1080px - 80px margen)
- **Ritmo visual:** clips del HOOK más cortos (×0.7), DESARROLLO normal (×1.0), REVELACIÓN más corta (×0.8)
- **Speech alignment:** cada clip entra exactamente cuando Whisper detecta que empieza esa sección del audio
- **Brand clip:** Pexels busca un clip de la marca, Claude decide la posición en la secuencia
- **Aislamiento por Short:** cada run usa `outputs/videos_raw/short_N/` para evitar colisiones al correr en paralelo
- **Cleanup automático:** los clips crudos se borran tras exportar el video final

---

## Shorts completados

| # | Tema | Brand clip | Archivo final |
|---|------|-----------|---------------|
| 1 | Nike logo $35 | — | short_bizrious_1_final.mp4 |
| 2 | FedEx Las Vegas blackjack | — | short_bizrious_2_final.mp4 |
| 3 | Menu anchoring bias (restaurantes) | — | short_bizrious_3_final.mp4 |
| 4 | Zara fast fashion espionage | — | short_bizrious_4_final.mp4 |
| 5 | Red Bull trash can campaign | Red Bull | short_bizrious_5_final.mp4 |
| 6 | Blockbuster rechaza Netflix | — | short_bizrious_6_final.mp4 |
| 7 | Yahoo rechaza Google por $1M | — | short_bizrious_7_final.mp4 |
| 8 | Lamborghini vs Ferrari (insulto) | — | short_bizrious_8_final.mp4 |
| 9 | PlayStation — traición de Nintendo | — | short_bizrious_9_final.mp4 |
| 10 | Red Bull origen Tailandia | Red Bull | short_bizrious_10_final.mp4 |
| 11 | Subway — adolescente $1000 | Subway | short_bizrious_11_final.mp4 |
| 12 | Instagram comprada por $1B | Instagram | short_bizrious_12_final.mp4 |
| 13 | Agua embotellada — marketing | — | short_bizrious_13_final.mp4 |
| 14 | WhatsApp — rechazado por Facebook | WhatsApp | short_bizrious_14_final.mp4 |
| 15 | Starbucks nombre mal escrito | Starbucks | short_bizrious_15_final.mp4 |
| 16 | Cinnabon scent marketing | Cinnabon | short_bizrious_16_final.mp4 |

---

## Cómo arrancar el Short 17 en una nueva sesión

1. Abre `/Users/soltero/Desktop/Bizrious/youtube_shorts.py`
2. Cambia `SHORT_NUMBER`, `APPROVED_SCRIPT`, `USER_KEYWORDS` y `BRAND_NAME`
3. Ejecuta: `python3 youtube_shorts.py`

El pipeline se detiene automáticamente tras el guión y pide confirmación antes de continuar — aunque con los scripts aprobados directamente en `APPROVED_SCRIPT` ya no usa esa pausa.

---

## Dependencias instaladas

```
anthropic, elevenlabs, python-dotenv, moviepy, openai-whisper,
Pillow, requests, numpy, torch, imageio-ffmpeg
```

Python versión: **3.9** (importante — usar `Optional[X]` no `X | None`)
