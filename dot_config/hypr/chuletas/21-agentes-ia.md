# 🤖 Agentes IA · Claude Code, Codex y OpenCode
> Los 3 agentes de programación en la terminal lado a lado: qué es cada uno, la misma acción en los 3, dónde se guarda cada cosa y cómo trabajar bien con ellos.

## 🧭 Qué es un agente de código en la terminal

🧠 Concepto: un **agente de código** es un programa que habla con un modelo de IA y además le da **herramientas**: leer archivos, buscar, editar, ejecutar comandos en tu shell y navegar la web. El modelo decide qué herramienta usar, mira el resultado y repite hasta terminar la tarea. A ese ciclo se le llama **bucle agéntico** (agentic loop).

```flujo
dir: abajo
Tú -> Agente : pides una tarea
Agente -> Modelo : contexto + herramientas
Modelo -> Herramienta : leer, editar, bash
Herramienta -> Permiso : ¿está permitido?
Permiso -> Resultado : ✅ sí, se ejecuta
Permiso --> Tú : ❓ te pregunta
Resultado -> Modelo : ve lo que pasó
Modelo -> Respuesta
```

La diferencia con un chat normal (ChatGPT o claude.ai en el navegador): el chat **te dice** qué hacer; el agente **lo hace** en tu proyecto y te pide permiso para lo peligroso.

- `Claude Code` :: Agente de **Anthropic**. Usa modelos Claude (Fable, Opus, Sonnet, Haiku). Código cerrado.
- `Codex CLI` :: Agente de **OpenAI**. Usa modelos GPT; con `--oss` puede usar modelos locales (Ollama o LM Studio). Código abierto (Apache-2.0), escrito en Rust.
- `OpenCode` :: Agente **independiente** (repo `anomalyco/opencode`, antes `sst/opencode`). Funciona con muchos proveedores (Anthropic, OpenAI, Google, locales…). Código abierto (MIT), escrito en TypeScript.

📌 Versiones instaladas en este equipo (noviembre 2026): `claude 2.1.318`, `codex-cli 0.166.0`, `opencode v2.0.32`. Todo lo de estas hojas sale de la ayuda (`--help`), la documentación oficial y el código fuente de **esas** versiones. En versiones más nuevas puede cambiar algo; para salir de dudas, pulsa `?` dentro de cada programa.

```tiempo
2025-02 : Claude Code sale como vista previa (repo anthropics/claude-code)
2025-04 : OpenAI publica Codex CLI (repo openai/codex)
2025-04 : Se crea el repo de OpenCode
2026 : Los 3 tienen subagentes, skills, MCP, hooks y modo plan
2026-11 : En este PC: claude 2.1.318 · codex 0.166 · opencode 2.0.32
```

## 🆚 Los 3 en una tabla

| Tema | Claude Code | Codex CLI | OpenCode |
|---|---|---|---|
| Empresa | Anthropic | OpenAI | Comunidad (anomalyco) |
| Licencia | Cerrado | Apache-2.0 | MIT |
| Lenguaje | (binario nativo) | Rust | TypeScript |
| Modelos | Claude | GPT / locales `--oss` | Cualquier proveedor |
| Abrir | `claude` | `codex` | `opencode` |
| Sin interfaz | `claude -p "…"` | `codex exec "…"` | `opencode run "…"` |
| Instrucciones | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| Config usuario | `~/.claude/settings.json` | `~/.codex/config.toml` | `~/.config/opencode/opencode.jsonc` |
| Ver atajos | `?` con el prompt vacío | `?` | `Ctrl+P` (paleta) |

💡 Consejo: `AGENTS.md` es un estándar abierto que leen Codex, OpenCode y muchos otros agentes. Claude Code usa `CLAUDE.md`, pero su documentación dice que también puede leer el `AGENTS.md` de un repo. Si trabajas con los 3, escribe las reglas del proyecto en `AGENTS.md`.

⚠️ Cuidado: OpenCode v2 **ya no** lee `CLAUDE.md` como respaldo (la documentación v2 lo dice textual). Si solo tienes `CLAUDE.md`, OpenCode no lo verá.

## 🔀 La misma acción en los 3

Esta es la tabla que más vas a usar: misma intención, tecla o comando de cada agente.

### ⌨️ Escribir y enviar

| Quiero… | Claude Code | Codex | OpenCode |
|---|---|---|---|
| Enviar | `Enter` | `Enter` | `Enter` |
| Salto de línea | `Shift+Enter` o `Ctrl+J` | `Ctrl+J` o `Shift+Enter` | `Shift+Enter` o `Ctrl+J` |
| Mencionar archivo | `@ruta` | `@ruta` | `@ruta` (y `@ruta#20-45`) |
| Ejecutar en la shell | `!comando` | `!comando` | `!comando` |
| Comandos | `/` | `/` | `/` o `Ctrl+P` |
| Editor externo | `Ctrl+G` | `Ctrl+G` | `Ctrl+X` y luego `E` |
| Pegar imagen | `Ctrl+V` | `Ctrl+V` | pegar o arrastrar la ruta del archivo |
| Buscar en historial | `Ctrl+R` | `Ctrl+R` | `↑` / `↓` |
| Ayuda de atajos | `?` | `?` | `Ctrl+P` |

### 🛑 Controlar al agente

| Quiero… | Claude Code | Codex | OpenCode |
|---|---|---|---|
| Interrumpir | `Esc` | `Esc` | `Esc` |
| Mensaje a la cola | `Enter` mientras trabaja | `Tab` | `Ctrl+X` y luego `Enter` |
| Corregir el rumbo en vivo | escribe y `Enter` | escribe y `Enter` | escribe y `Enter` |
| Mandar a segundo plano | `Ctrl+B` | `/ps` ve las terminales de fondo | `Ctrl+B` |
| Cambiar modelo | `/model` o `Alt+P` | `/model` | `/models` o `Ctrl+X M` |
| Más/menos razonamiento | `/effort` | `Alt+.` / `Alt+,` | `Ctrl+T` (variantes) |
| Modo plan | `Shift+Tab` o `/plan` | `Shift+Tab` o `/plan` | `Shift+Tab` → agente Plan |
| Permisos | `Shift+Tab` / `/permissions` | `/permissions` | reglas en `opencode.jsonc` |
| Salir | `Ctrl+D` dos veces | `Ctrl+C` | `Ctrl+C` / `Ctrl+X Q` |

### 💬 Sesiones y contexto

| Quiero… | Claude Code | Codex | OpenCode |
|---|---|---|---|
| Sesión nueva | `/clear` | `/new` | `/new` o `Ctrl+X N` |
| Retomar la última | `claude -c` | `codex resume --last` | `opencode -c` |
| Elegir sesión | `/resume` | `/resume` | `/sessions` o `Ctrl+X L` |
| Bifurcar | `/branch` | `/fork` | `/fork` |
| Compactar | `/compact` | `/compact` | `/compact` o `Ctrl+X C` |
| Deshacer cambios | `Esc Esc` o `/rewind` | — (usa git) | `/undo` o `Ctrl+X U` |
| Pregunta al margen | `/btw …` | `/btw …` o `/side` | `/btw …` |
| Ver el diff | `/diff` | `/diff` | `/diff` |
| Revisar código | `/code-review` | `/review` | comando propio en `.opencode/commands/` |
| Crear archivo de reglas | `/init` | `/init` | escribe `AGENTS.md` |
| Copiar respuesta | `/copy` | `/copy` o `Ctrl+O` | `/copy` o `Ctrl+X Y` |
| Exportar | `/export` | `/export` | `/export` o `Ctrl+X X` |
| Uso y gasto | `/usage` | `/usage` / `/status` | `/stats` |

⚠️ Cuidado: el mismo atajo **no** hace lo mismo en todos. `Ctrl+T` = lista de tareas en Claude Code, transcript en Codex y variante del modelo en OpenCode. `Ctrl+O` = transcript en Claude Code, copiar en Codex y sesiones recientes en OpenCode. `Shift+Tab` = modos de permiso en Claude Code, modo Plan en Codex y cambiar de agente en OpenCode.

## 🗂️ Dónde vive cada cosa

| Qué | Claude Code | Codex | OpenCode |
|---|---|---|---|
| Reglas globales | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | `~/.config/opencode/AGENTS.md` |
| Reglas del proyecto | `./CLAUDE.md` | `./AGENTS.md` | `./AGENTS.md` |
| Reglas extra | `./CLAUDE.local.md` (solo tú) | `AGENTS.override.md` (reemplaza) | `instructions` en la config |
| Config global | `~/.claude/settings.json` | `~/.codex/config.toml` | `~/.config/opencode/opencode.jsonc` |
| Config del proyecto | `.claude/settings.json` | `.codex/config.toml` | `opencode.jsonc` en el repo |
| Atajos | `~/.claude/keybindings.json` | `[tui.keymap]` en config.toml | `~/.config/opencode/cli.json` |
| Skills | `~/.claude/skills/` | `~/.agents/skills/` | `.opencode/skills/` |
| Subagentes | `~/.claude/agents/` | `/agents` (centro de agentes) | `~/.config/opencode/agents/` |
| Comandos propios | skills (`/nombre`) | `/presets` | `.opencode/commands/` |
| MCP | `claude mcp add` | `codex mcp add` | `opencode mcp add` |

🧠 Concepto: casi todo funciona en **capas**: global (para todos tus proyectos) → proyecto (se sube a git, lo comparte el equipo) → local (solo tú). Lo más cercano a la carpeta donde trabajas gana o se lee al final.

## 🛡️ Permisos comparados

Los 3 te protegen igual: **leer** suele estar permitido, **editar** y **ejecutar** pueden pedir permiso, y hay un modo "hazlo todo sin preguntar" que solo debes usar en entornos aislados.

| Nivel | Claude Code | Codex (`/permissions`) | OpenCode |
|---|---|---|---|
| Solo mirar | `plan` | Read Only | agente **Plan** |
| Pregunta antes de editar | `default` (Manual) | Ask for approval | regla `ask` |
| Edita solo, pregunta bash | `acceptEdits` | — | reglas por acción |
| Un clasificador decide | `auto` | Approve for me | — |
| Todo sin preguntar | `bypassPermissions` | Full Access | `--auto` (lo no denegado) |

❌ Mal: `claude --dangerously-skip-permissions` o `codex --dangerously-bypass-approvals-and-sandbox` en tu carpeta personal. El agente podría borrar o subir algo sin preguntarte.
✅ Bien: usar esos modos solo dentro de un contenedor o una máquina virtual sin datos importantes, como dice la propia ayuda ("Recommended only for sandboxes with no internet access").

## 🧠 Conceptos que comparten los 3

- `Contexto` :: Todo lo que el modelo "ve" en este momento: tus mensajes, sus respuestas, archivos leídos, salidas de comandos. Tiene un límite (ventana de contexto).
- `Token` :: Trocito de texto (más o menos ¾ de palabra en inglés). Los límites y los costos se miden en tokens.
- `Compactar` :: Resumir la conversación para liberar contexto sin empezar de cero (`/compact`).
- `Modo plan` :: El agente investiga y propone un plan **sin editar**. Tú lo apruebas y luego implementa.
- `Subagente` :: Un agente hijo con contexto limpio que hace una subtarea (buscar, revisar) y devuelve solo el resumen. Ahorra contexto al principal.
- `Skill` :: Carpeta con un `SKILL.md` (instrucciones + scripts) que el agente carga solo cuando hace falta.
- `MCP` :: Model Context Protocol: estándar para conectar herramientas externas (GitHub, navegador, bases de datos, documentación).
- `Hook` :: Script tuyo que se ejecuta en un momento fijo (antes de usar una herramienta, al terminar…). Sirve para reglas que **deben** cumplirse siempre.
- `Worktree` :: Copia de trabajo extra de git en otra carpeta: varios agentes trabajan en paralelo sin pisarse.
- `Headless` :: Usar el agente sin interfaz, desde un script o CI (`-p`, `exec`, `run`).

```capas
Tú : escribes el pedido y apruebas permisos
Agente (CLI) : interfaz, permisos, herramientas, sesiones
Instrucciones : CLAUDE.md / AGENTS.md + skills + MCP
Modelo : Claude / GPT / el que elijas en OpenCode
Tu proyecto : archivos, git, terminal
```

## 🚀 Cómo trabajar bien con cualquier agente

1. **Explora primero**: "lee el módulo de login y explícame cómo funciona, no cambies nada".
2. **Planea**: entra en modo plan y pide un plan corto; corrígelo antes de que toque código.
3. **Implementa en pasos pequeños**: un cambio, una verificación.
4. **Verifica**: que corra los tests, el linter o la app. Pide pruebas reales, no "debería funcionar".
5. **Revisa el diff** (`/diff`) y haz commit tú.

```flujo
dir: derecha
Explorar -> Planear -> Implementar -> Verificar -> Commit
Verificar --> Implementar : ❌ falla
```

💡 Consejo: el pedido vale más que el modelo. Di **qué**, **dónde** (`@archivo`), **cómo comprobarlo** y **qué no tocar**. Ejemplo: "Arregla el bug de @src/auth.ts que deja entrar con contraseña vacía. Añade un test que lo pruebe y corre `npm test`. No cambies la API pública."

💡 Consejo: una tarea = una sesión. Cuando cambies de tema, empieza sesión nueva (`/clear` o `/new`). El contexto lleno de cosas viejas hace que el agente se confunda y gaste más.

💡 Consejo: guarda en `CLAUDE.md` / `AGENTS.md` solo lo que el agente no puede adivinar: cómo correr tests, comandos de build, convenciones raras, "nunca edites X". Corto (la doc de Claude Code recomienda menos de 200 líneas).

### ⚖️ ¿Cuál uso?

| Situación | Buena opción | Por qué |
|---|---|---|
| Ya pagas Claude Pro/Max | Claude Code | Incluido en tu plan |
| Ya pagas ChatGPT Plus/Pro | Codex | Incluido en tu plan |
| Quieres cambiar de modelo libremente | OpenCode | Cualquier proveedor |
| Modelos locales, sin internet | OpenCode o `codex --oss` | Ollama / LM Studio |
| Leer o modificar el código del agente | Codex u OpenCode | Código abierto |
| Segunda opinión de un cambio | Otro de los 3 | Otro modelo ve otras cosas |

## ❌ Errores típicos y cómo evitarlos

| Error | Qué pasa | Solución |
|---|---|---|
| Sesión eterna | El agente olvida o mezcla temas | Sesión nueva por tarea; `/compact` |
| Pedido vago ("arréglalo") | Cambia cosas que no querías | Di archivo, objetivo y cómo verificar |
| Aceptar todo sin leer | Cambios raros entran al repo | Lee el diff antes del commit |
| Modo sin permisos en tu `$HOME` | Riesgo de borrar o filtrar datos | Úsalo solo en contenedores |
| `CLAUDE.md` gigante | Gasta contexto y se ignoran reglas | Reglas cortas; detalles en skills |
| Creer que "ya lo probó" | Solo lo dedujo | Pide que ejecute los tests y muestre la salida |
| Pegar secretos en el chat | Quedan en el historial | Usa variables de entorno |

## 🇬🇧 Vocabulario

🇬🇧 **agent** /ˈeɪ.dʒənt/ — agente · **prompt** /prɒmpt/ — pedido o instrucción · **context window** — ventana de contexto
🇬🇧 **to steer** /stɪər/ — corregir el rumbo · **to queue** /kjuː/ — poner en cola · **to interrupt** — interrumpir
🇬🇧 **approval** /əˈpruː.vəl/ — aprobación · **sandbox** — entorno aislado · **to bypass** — saltarse
🇬🇧 **to compact** — compactar · **to fork** — bifurcar · **to resume** /rɪˈzjuːm/ — retomar · **transcript** — transcripción
🇬🇧 **headless** — sin interfaz · **subagent** — subagente · **worktree** — copia de trabajo de git
🇬🇧 Frase útil: "Don't change anything yet, just explain how this works." — No cambies nada todavía, solo explica cómo funciona.
🇬🇧 Frase útil: "Run the tests and show me the output." — Corre los tests y muéstrame la salida.
