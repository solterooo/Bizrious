# Superpowers Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrar las 14 skills de superpowers al repo Bizrious para que sean autocontenidas, mapeadas al flujo de trabajo, y estén en GitHub.

**Architecture:** Copiar los archivos SKILL.md (y auxiliares) de cada skill al directorio `.claude/skills/superpowers/` del repo. Crear CLAUDE.md con instrucciones del proyecto y mapa explícito de skills por paso del flujo. Actualizar permissions en settings.local.json.

**Tech Stack:** Bash (cp/mkdir), git

---

### Task 1: Crear estructura de carpetas para las skills

**Files:**
- Create: `.claude/skills/superpowers/` (directorio)

- [ ] **Step 1: Crear el directorio**

```bash
mkdir -p /Users/soltero/Desktop/Bizrious/.claude/skills/superpowers
```

- [ ] **Step 2: Verificar que existe**

```bash
ls /Users/soltero/Desktop/Bizrious/.claude/skills/
```
Expected: `superpowers`

---

### Task 2: Copiar las 14 skills (SKILL.md de cada una)

**Files:**
- Create: `.claude/skills/superpowers/brainstorming.md`
- Create: `.claude/skills/superpowers/writing-plans.md`
- Create: `.claude/skills/superpowers/executing-plans.md`
- Create: `.claude/skills/superpowers/subagent-driven-development.md`
- Create: `.claude/skills/superpowers/systematic-debugging.md`
- Create: `.claude/skills/superpowers/test-driven-development.md`
- Create: `.claude/skills/superpowers/verification-before-completion.md`
- Create: `.claude/skills/superpowers/finishing-a-development-branch.md`
- Create: `.claude/skills/superpowers/requesting-code-review.md`
- Create: `.claude/skills/superpowers/receiving-code-review.md`
- Create: `.claude/skills/superpowers/dispatching-parallel-agents.md`
- Create: `.claude/skills/superpowers/using-git-worktrees.md`
- Create: `.claude/skills/superpowers/using-superpowers.md`
- Create: `.claude/skills/superpowers/writing-skills.md`

- [ ] **Step 1: Copiar SKILL.md de cada skill con nombre descriptivo**

```bash
BASE=/Users/soltero/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills
DEST=/Users/soltero/Desktop/Bizrious/.claude/skills/superpowers

for skill in brainstorming writing-plans executing-plans subagent-driven-development systematic-debugging test-driven-development verification-before-completion finishing-a-development-branch requesting-code-review receiving-code-review dispatching-parallel-agents using-git-worktrees using-superpowers writing-skills; do
  cp "$BASE/$skill/SKILL.md" "$DEST/$skill.md"
done
```

- [ ] **Step 2: Verificar que los 14 archivos están presentes**

```bash
ls /Users/soltero/Desktop/Bizrious/.claude/skills/superpowers/ | wc -l
```
Expected: `14`

```bash
ls /Users/soltero/Desktop/Bizrious/.claude/skills/superpowers/
```
Expected: los 14 archivos `.md`

- [ ] **Step 3: Commit**

```bash
cd /Users/soltero/Desktop/Bizrious
git add .claude/skills/superpowers/
git commit -m "Add superpowers skills to repo"
```

---

### Task 3: Crear CLAUDE.md con instrucciones del proyecto y mapa de skills

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Crear CLAUDE.md con el siguiente contenido exacto**

```markdown
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
```

- [ ] **Step 2: Verificar que el archivo existe y tiene contenido**

```bash
head -5 /Users/soltero/Desktop/Bizrious/CLAUDE.md
```
Expected: `# Bizrious — Instrucciones para Claude`

- [ ] **Step 3: Commit**

```bash
cd /Users/soltero/Desktop/Bizrious
git add CLAUDE.md
git commit -m "Add CLAUDE.md with Bizrious workflow and superpowers skill map"
```

---

### Task 4: Actualizar permissions en settings.local.json

**Files:**
- Modify: `.claude/settings.local.json`

- [ ] **Step 1: Añadir `Skill(superpowers:*)` a la lista `allow`**

Editar `.claude/settings.local.json` y agregar al array `allow`:
```json
"Skill(superpowers:*)"
```

El archivo resultante debe tener esta línea junto a las demás del array `allow`.

- [ ] **Step 2: Verificar que el JSON es válido**

```bash
python3 -c "import json; json.load(open('/Users/soltero/Desktop/Bizrious/.claude/settings.local.json')); print('JSON válido')"
```
Expected: `JSON válido`

- [ ] **Step 3: Commit**

```bash
cd /Users/soltero/Desktop/Bizrious
git add .claude/settings.local.json
git commit -m "Add Skill(superpowers:*) permission to settings"
```

---

### Task 5: Push a GitHub

- [ ] **Step 1: Verificar commits pendientes**

```bash
git log --oneline origin/main..HEAD
```
Expected: los 3 commits de las tareas anteriores

- [ ] **Step 2: Push**

```bash
git push origin main
```
Expected: `main -> main` sin errores

- [ ] **Step 3: Verificar en GitHub**

```bash
git log --oneline -4
```
Expected: los 3 commits nuevos aparecen con sus mensajes
