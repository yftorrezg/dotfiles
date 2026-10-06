---
name: ahorro-cuota
description: El usuario siente que la cuota se acaba rápido; qué la gasta de verdad (medido 29/09/2026) y cómo ahorrar
metadata:
  type: feedback
---

Medido el 29/09/2026 con los .jsonl de ~/.claude/projects (del 26/09 al 29/09): lo que más gasta son las sesiones interactivas largas con Opus. Hubo contextos de 614k, 469k y 354k tokens, y cada mensaje vuelve a leer todo el contexto: 700M de tokens leídos del caché y 21M escritos. Los subagentes fueron ~18 %. Los apuntes automáticos (`claude -p` con sonnet, `--no-session-persistence`, así que no aparecen en los .jsonl) son poco en comparación: ~113 clases, unos pocos M. Si el usuario pregunta por "caveman" (skill que responde en modo telegrama): solo recorta la salida (~10 % del gasto) y choca con que quiere explicaciones [[quiere-aprender-no-solo-soluciones]].

**Why:** quiere usar Claude más sin quedarse sin cuota.
**How to apply:** proponerle /clear al cambiar de tema (la memoria da la continuidad), no lanzar agentes en paralelo salvo que lo pida, y respuestas concisas.

Confirmado con el historial completo (29/09/2026): hasta el 20/09 el usuario usaba 100% Sonnet sin problema de cuota. El 23/09 pasó a Opus (coincide con el arranque del proyecto de auto-captura de cursos) y quedó de default así hasta el 29/09, que volvió a poner Sonnet con `/model`. Opus consume bastante más cuota por token que Sonnet; para las tareas de este usuario (scripts Python/bash, Hyprland, debug de logs, documentación) Sonnet rinde igual. Reservar Opus para problemas puntuales que se sientan trabados o con mucho razonamiento encadenado, y volver a Sonnet después.
