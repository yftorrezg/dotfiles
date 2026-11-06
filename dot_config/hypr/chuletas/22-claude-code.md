# ✳️ Claude Code · Atajos, comandos y trucos
> El agente de Anthropic en la terminal (versión 2.1.318 en este PC): cada atajo, los comandos `/`, permisos, memoria, hooks, MCP, agentes en segundo plano y modo sin interfaz.

## 🧭 Resumen en 30 segundos

| Tecla | Qué hace |
|---|---|
| `Enter` | Enviar (si está trabajando, lo pone en cola) |
| `Shift+Enter` / `Ctrl+J` | Nueva línea (en kitty funciona solo) |
| `Esc` | Interrumpir a Claude (guarda lo que ya hizo) |
| `Esc Esc` | Con texto: borrar borrador. Vacío: rebobinar (rewind) |
| `Shift+Tab` | Cambiar modo de permisos: Manual → acceptEdits → plan → … |
| `Ctrl+C` | Interrumpir; con el prompt vacío, 2 veces = salir |
| `Ctrl+O` | Ver la transcripción detallada (herramientas usadas) |
| `Ctrl+B` | Mandar el comando o agente actual a segundo plano |
| `Ctrl+R` | Buscar en el historial de prompts |
| `Ctrl+G` | Escribir el prompt en tu editor ($EDITOR) |
| `Alt+P` | Cambiar de modelo sin borrar lo escrito |
| `?` | Panel de atajos (con el prompt vacío) |
| `/` `!` `@` | Comandos · shell directa · mencionar archivo |

🧠 Concepto: Claude Code tiene dos "dibujadores" de pantalla: el **clásico** y el **fullscreen** (sin parpadeo, con paneles). Cámbialo con `/tui fullscreen` o `/tui default`; `/tui` sin nada te dice cuál usas. Algunos atajos solo existen en uno de los dos (te lo marco).

## 🚀 Arrancar desde la terminal

- `claude` :: Abre una sesión interactiva en la carpeta actual
- `claude "explica este repo"` :: Abre la sesión y manda ese primer mensaje
- `claude -c` :: Continúa la conversación más reciente de esta carpeta
- `claude -r` :: Abre el selector para retomar una sesión (`-r nombre` va directo)
- `claude -n "login-fix"` :: Pone nombre a la sesión (sale en `/resume` y en el título)
- `claude --model opus` :: Elige modelo (`fable`, `opus`, `sonnet` o el nombre completo)
- `claude --effort high` :: Esfuerzo de razonamiento: `low`, `medium`, `high`, `xhigh`, `max`
- `claude --permission-mode plan` :: Empieza en modo plan (también `acceptEdits`, `auto`, `manual`, `dontAsk`…)
- `claude --add-dir ../otra` :: Da acceso a otra carpeta además de la actual
- `claude -w nueva-func` :: Crea un worktree de git y trabaja ahí (aislado de tu rama)
- `claude --bg "corre los tests"` :: Lanza la sesión en segundo plano y te devuelve la terminal
- `claude -p "pregunta"` :: Modo sin interfaz: responde e imprime, ideal para scripts
- `claude --safe-mode` :: Arranca sin CLAUDE.md, skills, hooks, MCP ni plugins (para arreglar una config rota)
- `claude --chrome` :: Activa Claude in Chrome (controlar el navegador)
- `claude doctor` :: Revisa que la instalación esté sana
- `claude update` :: Busca e instala la versión nueva
- `claude --version` :: Muestra la versión

💡 Consejo: si una config rota no te deja trabajar, `claude --safe-mode` desactiva todas tus personalizaciones (CLAUDE.md, skills, plugins, hooks, MCP, atajos) pero mantiene login, modelo y permisos.

## ⌨️ Atajos generales

| Atajo | Qué hace | Detalle |
|---|---|---|
| `Ctrl+C` | Interrumpir o limpiar | Vacío: 1ª vez limpia, 2ª sale. Recupera lo borrado con `↑` |
| `Ctrl+D` | Salir | Pide confirmar; 2ª vez en menos de 0,8 s. Con texto borra el carácter siguiente |
| `Esc` | Interrumpir o cerrar diálogo | En un permiso, `Esc` = responder No |
| `Esc Esc` | Borrar borrador o rebobinar | El borrador queda en el historial (`↑`) |
| `Ctrl+G` | Editor externo | También `Ctrl+X Ctrl+E` |
| `Ctrl+L` | Redibujar la pantalla | Si la pantalla se ve rota |
| `Ctrl+O` | Transcripción detallada | Muestra herramientas, hora y modelo de cada respuesta |
| `Ctrl+R` | Buscar en el historial | Escribe y repite `Ctrl+R` para ir más atrás |
| `Ctrl+V` | Pegar imagen | Inserta `[Image #1]` donde está el cursor |
| `Ctrl+B` | Segundo plano | Bash o agentes largos siguen corriendo (en tmux: 2 veces) |
| `Ctrl+T` | Lista de tareas de Claude | La checklist de pasos (no son los procesos de fondo) |
| `Ctrl+S` | Guardar prompt para luego | Lo aparta; con el prompt vacío lo recupera |
| `Ctrl+Z` | Suspender | Vuelves con `fg` |
| `Ctrl+Enter` | Mandar ya lo que está en cola | Si tu terminal no lo envía, usa `Ctrl+X Ctrl+S` |
| `Ctrl+X Ctrl+K` | Parar todos los subagentes de fondo | Pulsa 2 veces en 3 s |
| `Shift+Tab` | Ciclar modos de permiso | Ver la sección de permisos |
| `Alt+P` | Cambiar modelo | Sin perder lo escrito |
| `Alt+T` | Pensamiento extendido sí/no | Sin efecto en Opus 5.5, Sonnet 5.5, Haiku 5.5 y Fable (siempre piensan) |
| `Alt+O` | Modo rápido (fast) sí/no | Igual que `/fast` |
| `Tab` | Aceptar sugerencia | En un permiso: añadir comentario a tu Sí/No |
| `↑` / `↓` | Mover cursor o historial | Si hay mensajes en cola, `↑` los recupera para editarlos |
| `←` / `→` | Pestañas de diálogos | `←` con el prompt vacío abre la vista de agentes |

💡 Consejo: mientras Claude trabaja puedes seguir escribiendo y pulsar `Enter`: el mensaje queda **en cola** (en gris) y Claude lo lee en cuanto termina las herramientas que está usando. No hace falta interrumpir para corregir el rumbo.

## ✏️ Editar el texto del prompt

| Atajo | Qué hace |
|---|---|
| `Ctrl+A` / `Ctrl+E` | Ir al inicio / final de la línea |
| `Alt+B` / `Alt+F` | Palabra anterior / siguiente |
| `Ctrl+W` | Borrar hacia atrás hasta el espacio (una ruta entera de un golpe) |
| `Ctrl+Backspace` | Borrar solo la palabra anterior |
| `Alt+D` | Borrar hasta el final de la palabra |
| `Ctrl+K` | Borrar hasta el final de la línea |
| `Ctrl+U` | Borrar hasta el inicio de la línea |
| `Ctrl+Y` | Pegar lo último que borraste con `Ctrl+K/U/W` |
| `Alt+Y` | Después de `Ctrl+Y`: ir rotando por lo borrado antes |
| `Ctrl+_` | Deshacer la última edición del prompt |

🧠 Concepto: estos atajos vienen de **readline**, la librería de edición de bash. Si los aprendes aquí, te sirven igual en bash, zsh, Python, psql y casi cualquier terminal.

📌 Nota: para Claude Code una "palabra" son letras y números; `_`, `.` y `/` separan palabras. Con `src/utils/foo.ts`, `Alt+B` se detiene en `ts`, `foo`, `utils`, `src`. En cambio `Ctrl+W` borra todo `src/utils/foo.ts` de una vez.

## ⚡ Prefijos y escritura rápida

- `/` :: Al inicio: comando o skill. A mitad de frase, `Tab` completa el nombre
- `!` :: Al inicio: modo shell. Corre el comando, agrega la salida a la conversación y Claude la comenta
- `@` :: Autocompletar rutas de archivos para mencionarlos
- `:heart:` :: Atajos de emoji (`:` + 2 letras muestra sugerencias)
- `?` :: Con el prompt vacío: panel de atajos
- `\` + `Enter` :: Nueva línea en cualquier terminal
- `Ctrl+J` :: Nueva línea sin configurar nada
- `Shift+Enter` :: Nueva línea (nativo en kitty, WezTerm, Ghostty, iTerm2…)
- `Espacio (mantener)` :: Dictado por voz (si activaste `/voice`)

```bash
! npm test          # Claude ve la salida y te explica los fallos
! git status
! ls -la src/
```

💡 Consejo: `! comando` no pasa por los permisos de Claude: lo escribiste tú. Si solo quieres que la salida quede en contexto sin que Claude responda, pon `"respondToBashCommands": false` en `settings.json`.

⚠️ Cuidado: si no hay hueco en el contexto, no pegues logs gigantes. Mejor: `! tail -50 app.log` o pide a Claude que busque con grep.

## 🛡️ Modos de permiso

`Shift+Tab` va rotando: **Manual** (`default`) → `acceptEdits` → `plan` → y, si están disponibles, `bypassPermissions` y `auto`.

| Modo | Qué hace | Cuándo usarlo |
|---|---|---|
| `default` (Manual) | Pregunta antes de editar y de ejecutar | Por defecto, código que te importa |
| `acceptEdits` | Edita archivos sin preguntar; pregunta comandos | Cuando confías en los cambios y revisas el diff |
| `plan` | Investiga y propone un plan, **no edita** | Antes de un cambio grande |
| `auto` | Un clasificador aprueba lo seguro y bloquea lo riesgoso | Tareas largas sin estar mirando |
| `dontAsk` | No pregunta: lo que no está permitido se rechaza | Scripts con reglas claras |
| `bypassPermissions` | No pregunta nada | Solo en contenedores o VMs aisladas |

```flujo
dir: derecha
Manual -> acceptEdits -> plan -> bypassPermissions -> auto
auto --> Manual : Shift+Tab
```

En un diálogo de permiso: `Enter` acepta la opción marcada, `Esc` = No, `Tab` añade un comentario ("sí, pero usa pnpm"), y `Shift+Tab` elige "permitir para el resto de la sesión" cuando existe esa opción.

### 📜 Reglas permanentes (allow / ask / deny)

Con `/permissions` las ves y editas; también puedes escribirlas en `settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash(npm run test *)", "Bash(git status)", "Edit"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Read(./.env)", "Bash(rm -rf *)"]
  }
}
```

- `Bash(git *)` :: Cualquier comando que empiece con `git`
- `Read(./.env)` :: Leer ese archivo concreto
- `Edit` :: Todas las ediciones de archivos
- `mcp__github` :: Todas las herramientas del servidor MCP "github"

💡 Consejo: `/fewer-permission-prompts` revisa tus sesiones anteriores y te propone una lista de comandos de solo lectura para permitir siempre. Menos ventanitas, mismo control.

## 🧰 Comandos `/` más útiles

Escribe `/` y unas letras para filtrar. Un comando solo se reconoce al **inicio** del mensaje; lo que escribas después son sus argumentos.

### 💬 Conversación y sesiones

- `/clear` :: Conversación nueva con el contexto vacío (alias `/new`, `/reset`). La anterior se puede retomar
- `/resume` :: Elegir una sesión anterior para seguirla (alias `/continue`)
- `/rename nombre` :: Poner nombre a la sesión
- `/branch` :: Crear una rama de la conversación para probar otro camino (la original se guarda)
- `/fork tarea` :: Copiar la conversación a una sesión en segundo plano y seguir aquí
- `/rewind` :: Volver código y conversación a un punto anterior (alias `/undo`, `/checkpoint`)
- `/btw pregunta` :: Pregunta al margen: no entra en la conversación ni usa herramientas
- `/recap` :: Resumen de una línea de lo que va la sesión
- `/export archivo.txt` :: Exportar la conversación como texto
- `/copy` :: Copiar la última respuesta (`/copy 2` = la penúltima). En el selector, `w` la guarda en archivo
- `/exit` :: Salir (alias `/quit`)

### 🧠 Contexto y modelo

- `/context` :: Cuadrícula de colores con qué ocupa el contexto y consejos para liberarlo
- `/compact` :: Resumir la conversación para liberar espacio. Puedes guiarlo: `/compact céntrate en el bug de login`
- `/autocompact 500k` :: A qué tamaño se compacta solo (`auto` vuelve al valor por defecto)
- `/model` :: Elegir modelo (se guarda como predeterminado). En el selector, `s` = solo esta sesión; `←` `→` ajustan el esfuerzo
- `/effort high` :: Nivel de razonamiento: `low` … `xhigh`, `max` (solo esta sesión) o `auto`
- `/fast` :: Modo rápido sí/no
- `/advisor opus` :: Un segundo modelo aconseja en momentos clave (`off` lo apaga)
- `/usage` :: Costo de la sesión, límites del plan y estadísticas (alias `/cost`, `/stats`)
- `/goal condición` :: Claude sigue trabajando en varios turnos hasta cumplir la condición

### 🛠️ Código y revisión

- `/init` :: Crea un `CLAUDE.md` inicial analizando el proyecto
- `/plan tarea` :: Entra en modo plan y empieza con esa tarea
- `/diff` :: Ver los cambios sin commitear y los de cada turno de Claude
- `/code-review` :: Revisa el diff en busca de bugs (alias `/review`). Con `--fix` aplica los arreglos
- `/code-review high 1234` :: Revisa el PR 1234 con esfuerzo alto
- `/simplify` :: 4 agentes buscan código repetido, simplificaciones y mejoras de eficiencia, y las aplican
- `/security-review` :: Busca vulnerabilidades en los cambios de tu rama
- `/batch instrucción` :: Divide un cambio enorme en 5–30 partes y lanza un agente por parte, cada uno en su worktree
- `/run` :: Lanza tu app para ver el cambio funcionando, no solo los tests
- `/verify` :: Comprueba que el cambio hace lo que debe, ejecutando la app

### 🌙 Trabajo en paralelo

- `/tasks` :: Ver y gestionar lo que corre en segundo plano (shells y subagentes)
- `/background` :: Mandar toda la sesión a segundo plano y liberar la terminal (alias `/bg`)
- `/subtask tarea` :: Un subagente con toda la conversación hace la tarea; su resultado vuelve aquí
- `/loop 5m revisa si terminó el deploy` :: Repetir un prompt cada cierto tiempo mientras la sesión está abierta
- `/schedule` :: Tareas programadas en la nube (alias `/routines`)

### ⚙️ Configuración

- `/config` :: Panel de ajustes (tema, modelo, editor vim…). También `/config theme=dark`
- `/permissions` :: Reglas allow / ask / deny
- `/memory` :: Editar los `CLAUDE.md` y la memoria automática
- `/hooks` :: Ver los hooks configurados
- `/mcp` :: Servidores MCP: estado, login OAuth, `reconnect all`
- `/skills` :: Lista de skills; `t` ordena por tokens, `Espacio` cambia su visibilidad
- `/agents` :: Subagentes (pídele a Claude que los cree o edita `.claude/agents/`)
- `/plugin` :: Instalar, activar y desactivar plugins
- `/keybindings` :: Abrir tu archivo de atajos `~/.claude/keybindings.json`
- `/statusline` :: Configurar la barra de estado
- `/theme` :: Tema de colores (incluye `auto`, claro/oscuro y daltónicos)
- `/output-style` :: Estilo de respuesta (por ejemplo, más conciso)
- `/terminal-setup` :: Activa `Shift+Enter` en terminales que no lo traen (VS Code, Alacritty, Zed…)
- `/add-dir ruta` :: Dar acceso a otra carpeta · `/cd ruta` mueve la sesión a otra carpeta

### 🩺 Problemas y ayuda

- `/doctor` :: Revisión completa de instalación, ajustes y CLAUDE.md; propone arreglos
- `/debug` :: Activa el registro de depuración y lo analiza
- `/status` :: Versión, modelo, cuenta y conexión
- `/help` :: Ayuda y lista de comandos
- `/release-notes` :: Novedades de cada versión
- `/bug` :: Reportar un error (te pide confirmar qué se envía)
- `/powerup` :: Lecciones interactivas de funciones de Claude Code
- `/insights` :: Informe HTML de cómo usas Claude Code y dónde fallan las cosas

📌 Nota: `/vim` se eliminó (v2.1.92): el modo vim se activa en `/config` → Editor mode. `/pr-comments` también se eliminó: pide a Claude directamente que lea los comentarios del PR.

## 📜 Transcripción, /btw y diff

### 🔎 Transcripción (`Ctrl+O`)

| Tecla | Qué hace |
|---|---|
| `{` / `}` | Saltar al prompt anterior / siguiente (fullscreen) |
| `[` | Volcar la conversación al scroll de la terminal para buscar con tus herramientas (fullscreen) |
| `v` | Abrir la conversación en tu editor (fullscreen) |
| `Ctrl+E` | Mostrar todo el contenido (solo renderer clásico) |
| `?` | Atajos de la transcripción (fullscreen) |
| `q` / `Esc` / `Ctrl+C` | Salir de la transcripción |

### 💭 Ventana de `/btw`

| Tecla | Qué hace |
|---|---|
| `Espacio` / `Enter` / `Esc` | Cerrar la respuesta |
| `↑` / `↓` | Desplazar la respuesta |
| `Shift+←` / `Shift+→` | Ir a respuestas `/btw` anteriores (también `[` y `]`) |
| `c` | Copiar la respuesta como Markdown |
| `f` | Convertirla en subagente con herramientas que sigue trabajando |
| `x` | Borrar la lista de `/btw` anteriores |

🧠 Concepto: `/btw` responde **solo con lo que ya está en la conversación** (no lee archivos ni ejecuta nada) y no ensucia el historial. Es perfecto para "¿cómo se llamaba ese archivo?" mientras Claude sigue trabajando.

### 🧾 Panel de diff (`/diff`)

En fullscreen se abre al lado de la conversación (terminal de al menos 110 columnas, en un repo git). Clic en un archivo para saltar a él, `ask` para preguntar a Claude sobre ese diff, `source` para ver solo los cambios de un turno (`T1`, `T2`…), y `Ctrl+X B` para comparar contra: cambios de esta sesión → todo lo no commiteado → todo desde que tu rama salió de la principal.

## 🧠 Memoria: CLAUDE.md

| Archivo | Para qué | Quién lo ve |
|---|---|---|
| `~/.claude/CLAUDE.md` | Tus preferencias en todos los proyectos | Solo tú |
| `./CLAUDE.md` o `./.claude/CLAUDE.md` | Reglas del proyecto (se sube a git) | Todo el equipo |
| `./CLAUDE.local.md` | Tus notas privadas del proyecto (ponlo en `.gitignore`) | Solo tú |
| `.claude/rules/*.md` | Reglas por tema; pueden aplicarse solo a ciertas rutas | Equipo |
| `/etc/claude-code/CLAUDE.md` | Reglas de la organización (Linux) | Todos |

- Se cargan los `CLAUDE.md` de la carpeta actual **y de todas las carpetas de arriba**; los de subcarpetas se cargan cuando Claude toca archivos de ahí.
- Se **suman** (no se pisan): primero lo de la raíz del disco, al final lo más cercano a tu carpeta.
- `@docs/api.md` dentro de un CLAUDE.md **importa** ese archivo. Entre comillas invertidas no se importa.
- La **memoria automática** son notas que Claude escribe solo (en `~/.claude/projects/<proyecto>/memory/`); se cargan las primeras 200 líneas o 25 KB.

```text
# Proyecto tienda
- Tests: `pnpm test` (rápidos) y `pnpm test:e2e` (lentos, solo si te lo pido)
- Código en TypeScript estricto; nada de `any`.
- Nunca edites archivos de `src/generated/`.
- Antes de terminar, corre `pnpm lint`.
@docs/arquitectura.md
```

✅ Bien: reglas cortas, concretas y verificables ("corre `pnpm lint`").
❌ Mal: "escribe buen código" o copiar media documentación. La doc oficial recomienda menos de **200 líneas** por archivo.

⚠️ Cuidado: CLAUDE.md es **contexto**, no una ley: Claude puede saltárselo. Si algo debe cumplirse siempre (por ejemplo, "nunca toques `.env`"), usa una regla `deny` o un hook `PreToolUse`.

## ⚙️ settings.json

| Archivo | Alcance |
|---|---|
| `~/.claude/settings.json` | Todos tus proyectos |
| `.claude/settings.json` | Este proyecto, se comparte en git |
| `.claude/settings.local.json` | Este proyecto, solo tú (git lo ignora) |
| Ajustes administrados | La organización; no se pueden pisar |

```json
{
  "model": "opus",
  "theme": "auto",
  "editorMode": "vim",
  "vimInsertModeRemaps": { "jj": "<Esc>" },
  "env": { "NODE_ENV": "development" },
  "permissions": {
    "allow": ["Bash(pnpm *)"],
    "deny": ["Read(./.env)"]
  }
}
```

💡 Consejo: no hace falta editar JSON a mano: `/config` cambia lo común, y el skill `/update-config` entiende pedidos como "permite siempre `npm test`" o "pon la variable X".

## 🪝 Hooks: reglas que siempre se cumplen

🧠 Concepto: un **hook** es un comando tuyo que Claude Code ejecuta en un momento fijo. A diferencia de CLAUDE.md, no depende de que el modelo "se acuerde".

| Evento | Cuándo salta | Ejemplo de uso |
|---|---|---|
| `SessionStart` | Al empezar o retomar sesión | Cargar contexto (rama, tickets) |
| `UserPromptSubmit` | Al enviar un prompt | Bloquear pedidos o añadir info |
| `PreToolUse` | Antes de usar una herramienta | Prohibir editar `.env` |
| `PermissionRequest` | Cuando hace falta un permiso | Decidir automáticamente |
| `PostToolUse` | Después de usarla con éxito | Formatear el archivo editado |
| `Notification` | Cuando Claude Code avisa | Notificación del escritorio |
| `Stop` | Cuando Claude termina de responder | Sonido o correr tests |
| `SubagentStop` | Cuando termina un subagente | Registrar resultados |
| `PreCompact` | Antes de compactar | Guardar un respaldo |
| `SessionEnd` | Al cerrar la sesión | Limpieza |

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "npx prettier --write \"$CLAUDE_PROJECT_DIR\"/src" }]
      }
    ],
    "Notification": [
      { "hooks": [{ "type": "command", "command": "notify-send 'Claude Code' 'Te necesita'" }] }
    ]
  }
}
```

- `exit 0` :: Todo bien, sigue
- `exit 2` :: **Bloquea** la acción (en eventos que pueden bloquear) y muestra tu stderr a Claude
- `/hooks` :: Ver los hooks activos
- `--bare` :: Arrancar sin hooks (también sin LSP, plugins ni CLAUDE.md automático)

📌 Nota: hay más de 30 eventos (`PostToolUseFailure`, `SubagentStart`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `PostCompact`…). La lista completa está en la documentación de hooks.

## 🔌 MCP: conectar herramientas externas

```bash
# Servidor local (stdio): todo lo que va después de -- es el comando del servidor
claude mcp add --env AIRTABLE_API_KEY=TU_CLAVE --transport stdio airtable -- npx -y airtable-mcp-server

# Servidor remoto por HTTP (lo recomendado)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Con cabecera de autenticación
claude mcp add --transport http mi-api https://api.ejemplo.com/mcp --header "Authorization: Bearer TOKEN"

claude mcp list            # ver todos
claude mcp get notion      # detalles de uno
claude mcp remove notion   # quitarlo
claude mcp login sentry    # login OAuth
```

| `--scope` | Dónde se guarda | Se comparte |
|---|---|---|
| `local` (por defecto) | `~/.claude.json`, solo este proyecto | No |
| `project` | `.mcp.json` en la raíz del repo | Sí, por git |
| `user` | `~/.claude.json`, todos tus proyectos | No |

💡 Consejo: dentro de la sesión, `/mcp` muestra qué servidores fallaron y `/mcp reconnect all` los reintenta. Cada servidor MCP gasta contexto con sus herramientas: activa solo los que uses.

## 🧩 Skills y subagentes

🧠 Concepto: un **skill** es una carpeta con un `SKILL.md`. Claude lee solo el nombre y la descripción; carga el resto cuando la tarea lo necesita. Lo invocas tú con `/nombre` o Claude lo usa solo. Un **subagente** es un Claude aparte con contexto limpio y sus propias herramientas.

```text
~/.claude/skills/revisar-sql/SKILL.md      ← skill personal (todos tus proyectos)
.claude/skills/deploy/SKILL.md             ← skill del proyecto
~/.claude/agents/revisor.md                ← subagente personal
.claude/agents/revisor.md                  ← subagente del proyecto
```

```text
---
name: revisar-sql
description: Revisa consultas SQL buscando inyección e índices faltantes. Úsalo al tocar archivos .sql o repositorios de datos.
---
1. Busca consultas armadas concatenando texto.
2. Revisa que las columnas de WHERE tengan índice.
3. Responde con una tabla: archivo, línea, problema, arreglo.
```

- `/revisar-sql` :: Invocar el skill a mano (puedes encadenar hasta 6: `/skill-a /skill-b haz X`)
- `/reload-skills` :: Recargar skills creados o cambiados sin reiniciar
- `/skill-doctor` :: Cuánto contexto gasta cada skill y cuánto se usa
- `usa el subagente revisor para…` :: Pedir que delegue en un subagente

💡 Consejo: la **descripción** decide cuándo se usa el skill. Escribe qué hace **y cuándo** usarlo ("Úsalo al tocar archivos .sql").

## 🌙 Segundo plano y agentes en paralelo

```flujo
dir: derecha
claude --bg -> Sesión de fondo : corre sola
Sesión de fondo -> claude agents : la listas
claude agents -> claude attach : la abres
claude attach --> Sesión de fondo : ← o /exit = soltar
```

- `Ctrl+B` :: Pasar el comando Bash o subagente actual a segundo plano
- `/tasks` :: Ver procesos de fondo de esta sesión
- `← (prompt vacío)` :: Vista de agentes (tus sesiones de fondo)
- `claude --bg "tarea"` :: Empezar una sesión ya en segundo plano (imprime su id)
- `claude agents` :: Listar las sesiones de fondo
- `claude attach <id>` :: Abrir una sesión de fondo en esta terminal
- `claude logs <id>` :: Ver lo último que imprimió
- `claude stop <id>` :: Pararla (la conversación se guarda)
- `claude rm <id>` :: Borrarla (y su worktree si es seguro)
- `claude -w nombre` :: Sesión en un worktree nuevo para no pisar tu rama

⚠️ Cuidado: varios agentes en el **mismo** directorio pueden pisarse los archivos. Para trabajo en paralelo usa worktrees (`-w`, `/batch`, `/fork`).

## 🤖 Modo sin interfaz (`-p`)

```bash
# Pregunta rápida e imprime la respuesta
claude -p "¿qué hace la función parseToken en src/auth.ts?"

# Pasarle datos por tubería
cat error.log | claude -p "explica el error principal y cómo arreglarlo"

# Salida JSON para scripts
claude -p "lista los TODO del repo" --output-format json

# Limitar herramientas y gasto
claude -p "corre los tests y resume" --allowedTools "Bash(npm test *)" "Read" --max-budget-usd 1

# Respuesta con forma fija (JSON Schema)
claude -p "extrae nombre y versión de package.json" \
  --json-schema '{"type":"object","properties":{"name":{"type":"string"},"version":{"type":"string"}},"required":["name","version"]}'
```

⚠️ Cuidado: con `-p` (o cuando la salida va a una tubería) se **salta** el diálogo de confianza de la carpeta. Úsalo solo en carpetas en las que confíes.

## 🟩 Modo vim del prompt

Actívalo en `/config` → Editor mode (o `"editorMode": "vim"`).

| Tecla | Modo | Qué hace |
|---|---|---|
| `Esc` | INSERT → NORMAL | Volver a NORMAL |
| `i` `a` `I` `A` | NORMAL | Insertar antes / después / inicio / final |
| `o` / `O` | NORMAL | Línea nueva abajo / arriba |
| `h j k l` | NORMAL | Moverse |
| `w` `b` `e` | NORMAL | Palabra siguiente / anterior / final |
| `0` `$` `^` | NORMAL | Inicio / final / primer carácter |
| `gg` / `G` | NORMAL | Principio / última línea |
| `f{c}` `t{c}` | NORMAL | Saltar a / antes de un carácter (`;` repite) |
| `%` | NORMAL | Paréntesis o llave pareja |
| `dd` `D` `dw` | NORMAL | Borrar línea / hasta el final / palabra |
| `cc` `cw` `ciw` | NORMAL | Cambiar línea / palabra / palabra interior |
| `yy` `p` `P` | NORMAL | Copiar línea / pegar después / antes |
| `u` `.` | NORMAL | Deshacer / repetir el último cambio |
| `v` / `V` | NORMAL | Selección por caracteres / por líneas |
| `/` | NORMAL | Buscar en el historial (como `Ctrl+R`) |

📌 Nota: no hay modo bloque (`Ctrl+V`). Objetos de texto disponibles: `iw aw iW aW i" a" i' a' i( a( i[ a[ i{ a{`.

## 🧑‍🍳 Recetas rápidas

### ✅ Arreglar un bug con método

1. `Shift+Tab` hasta **plan** y escribe: "El login acepta contraseñas vacías. Encuentra la causa en @src/auth/ y propón un arreglo con test. No edites todavía."
2. Lee el plan; corrígelo escribiendo en el chat.
3. Aprueba el plan y deja que implemente.
4. "Corre `npm test` y muéstrame la salida."
5. `/diff` para revisar y `/code-review` para una segunda mirada.
6. Commit tú (o pide "haz commit con un mensaje claro").

### ✅ Cuando el contexto se llena

1. `/context` para ver qué ocupa espacio.
2. Si sigues con la misma tarea: `/compact céntrate en X`.
3. Si cambias de tarea: `/clear` (la anterior se puede recuperar con `/resume`).

### ✅ Me equivoqué y quiero volver atrás

- `Esc Esc` con el prompt vacío o `/rewind` :: Elegir un punto anterior y restaurar código, conversación o ambos
- `/branch` :: Úsalo antes de experimentar: así siempre puedes volver a la versión original con `/resume`

⚠️ Cuidado: rewind restaura las ediciones que hizo Claude con sus herramientas de archivos. Lo que cambió un comando de shell (por ejemplo `rm` o una migración de base de datos) no se deshace. Git sigue siendo tu red de seguridad.

## 🇬🇧 Vocabulario

🇬🇧 **to rewind** /riːˈwaɪnd/ — rebobinar · **checkpoint** — punto de control · **to stash** — guardar para luego
🇬🇧 **to compact** — compactar · **effort** /ˈef.ət/ — esfuerzo · **thinking** — razonamiento · **fast mode** — modo rápido
🇬🇧 **to allow / to deny** /dɪˈnaɪ/ — permitir / negar · **permission prompt** — ventana de permiso
🇬🇧 **hook** — gancho (script automático) · **matcher** — filtro de herramientas · **scope** /skəʊp/ — alcance
🇬🇧 **background** — segundo plano · **to attach / to detach** — conectarse / soltarse · **queued** /kjuːd/ — en cola
🇬🇧 Frase útil: "Enter plan mode and propose a plan first." — Entra en modo plan y propón un plan primero.
🇬🇧 Frase útil: "Use a subagent to search the codebase so you keep your context clean." — Usa un subagente para buscar y así mantienes limpio tu contexto.
