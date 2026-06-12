# Superpowers Integration — Bizrious

**Fecha:** 2026-06-12  
**Estado:** Aprobado

---

## Objetivo

Integrar las 14 skills de superpowers al flujo de trabajo de Bizrious de forma que:
1. Los archivos de skills viajen con el repo (autocontenido, sin depender del plugin global)
2. CLAUDE.md mapee explícitamente qué skill usar en cada paso del flujo
3. Los permisos en `.claude/settings.local.json` incluyan `Skill(superpowers:*)`

---

## Estructura de archivos

```
Bizrious/
├── .claude/
│   ├── settings.local.json          (añadir Skill(superpowers:*) permissions)
│   └── skills/
│       └── superpowers/
│           ├── brainstorming.md
│           ├── writing-plans.md
│           ├── executing-plans.md
│           ├── subagent-driven-development.md
│           ├── systematic-debugging.md
│           ├── test-driven-development.md
│           ├── verification-before-completion.md
│           ├── finishing-a-development-branch.md
│           ├── requesting-code-review.md
│           ├── receiving-code-review.md
│           ├── dispatching-parallel-agents.md
│           ├── using-git-worktrees.md
│           ├── using-superpowers.md
│           └── writing-skills.md
├── CLAUDE.md                         (nuevo — instrucciones + mapa del flujo)
└── docs/superpowers/specs/           (este archivo)
```

---

## CLAUDE.md — contenido

### Sección 1: Instrucciones generales
- Proyecto: pipeline Python para YouTube Shorts (Business Facts)
- Estructura obligatoria del guión (4 bloques)
- Reglas de formato

### Sección 2: Mapa explícito de skills por paso del flujo

| Paso | Skill |
|------|-------|
| Idear tema + estructura de un Short nuevo | `superpowers:brainstorming` |
| Planear cambios al pipeline | `superpowers:writing-plans` |
| Ejecutar plan con tareas independientes | `superpowers:subagent-driven-development` |
| Depurar errores del pipeline | `superpowers:systematic-debugging` |
| Añadir features con tests | `superpowers:test-driven-development` |
| Antes de declarar el Short listo | `superpowers:verification-before-completion` |
| Antes de hacer push a GitHub | `superpowers:requesting-code-review` + `superpowers:verification-before-completion` |
| Al recibir feedback sobre el pipeline | `superpowers:receiving-code-review` |
| Al terminar una rama de desarrollo | `superpowers:finishing-a-development-branch` |

---

## Permisos a añadir

En `.claude/settings.local.json`, agregar a la lista `allow`:
```json
"Skill(superpowers:*)"
```

---

## Fuente de los archivos de skills

Copiar desde:
```
/Users/soltero/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/<nombre>/
```

Cada skill es una carpeta — se toma el archivo principal `*.md` de cada una.

---

## Qué NO se incluye en el mapa

- `using-superpowers` — se usa siempre al inicio de sesión, no es específica del flujo
- `using-git-worktrees` — overkill para repo de una sola persona
- `writing-skills` — skill meta, no aplica al flujo de Bizrious
- `dispatching-parallel-agents` — disponible en el repo pero sin mapeo explícito (uso ocasional)
