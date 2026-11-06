# 🟪 OpenCode · Atajos, comandos y agentes
> El agente de código abierto que funciona con cualquier proveedor (v2.0.32 en este PC): la tecla líder, todos los atajos, comandos `/`, agentes Build/Plan, permisos por reglas y config.

## 🧭 Resumen en 30 segundos

🧠 Concepto: OpenCode usa una **tecla líder** (leader): pulsas `Ctrl+X`, la sueltas y luego pulsas otra tecla. Por ejemplo, `Ctrl+X` y luego `M` = elegir modelo. En las tablas lo verás como `Ctrl+X M` (en la config se escribe `<leader>m`). Si dudas, `Ctrl+P` abre la **paleta** con todas las acciones disponibles en la vista actual.

| Tecla | Qué hace |
|---|---|
| `Enter` | Enviar. Si está trabajando: **corrige el rumbo** de la sesión activa |
| `Ctrl+X Enter` | Encolar el mensaje para después |
| `Shift+Enter` · `Ctrl+J` | Nueva línea |
| `Esc` | Interrumpir |
| `Ctrl+P` | Paleta de comandos (todas las acciones) |
| `Shift+Tab` | Cambiar de agente: **Build** ↔ **Plan** |
| `Ctrl+X M` · `F2` | Elegir modelo · ciclar modelos recientes |
| `Ctrl+T` | Cambiar la variante del modelo (nivel de razonamiento) |
| `Ctrl+X N` · `Ctrl+X L` | Sesión nueva · lista de sesiones |
| `Ctrl+X U` · `Ctrl+X R` | Deshacer · rehacer el último mensaje (con archivos) |
| `Ctrl+X E` | Escribir el prompt en tu editor |
| `@` · `!` · `/` | Archivo · shell · comandos |
| `Ctrl+C` · `Ctrl+X Q` | Salir |

## 🚀 Arrancar desde la terminal

- `opencode` :: Abre la interfaz completa (TUI) en la carpeta actual
- `opencode ruta/proyecto` :: Abre en otra carpeta
- `opencode -c` :: Continúa la última sesión
- `opencode -s ses_123` :: Continúa (o crea) la sesión con ese ID
- `opencode --prompt "explica el repo"` :: Empieza con ese mensaje
- `opencode --auto` :: Aprueba solo todo lo que no esté denegado explícitamente
- `opencode mini` :: Interfaz mínima (no ocupa toda la pantalla; conserva el scroll)
- `opencode run "mensaje"` :: Sin interfaz: manda el mensaje e imprime la respuesta
- `opencode models` :: Lista todos los modelos disponibles
- `opencode auth login anthropic` :: Conectar un proveedor (también `auth list`, `auth logout`, `auth switch`)
- `opencode session list` :: Sesiones del proyecto (también `delete`, `export`, `import`)
- `opencode mcp list` :: Servidores MCP y su estado
- `opencode stats` :: Estadísticas de uso (`--days 7`, `--models`, `--cost`)
- `opencode reload` :: Recargar la config sin reiniciar
- `opencode debug config` :: Ver de dónde sale la configuración (`debug paths` = rutas)
- `opencode serve` :: Servidor API y web · `opencode pair` = enlace para conectar navegador o app
- `opencode upgrade` :: Actualizar (alias `update`)

🧠 Concepto: en la v2, OpenCode corre un **servicio de fondo** (servidor) y la terminal es un cliente que se conecta a él. Por eso existen `--standalone` (servidor privado solo para esta vez), `--server URL` y `opencode service start|stop|status|restart`.

## ⌨️ Escribir en el prompt

- `@archivo` :: Buscar y adjuntar un archivo (sigue escribiendo para filtrar)
- `@src/auth.ts#20-45` :: Adjuntar solo esas líneas
- `!git status` :: Modo shell: `!` al inicio del prompt vacío; `Esc` para salir sin ejecutar
- `/` :: Lista de comandos; escribe para filtrar y `Enter`
- `Ctrl+V` :: Pegar. Si pegas (o arrastras) la ruta de una imagen o archivo, OpenCode lo adjunta
- `Ctrl+X I` :: Ver las imágenes adjuntas
- `↑` / `↓` :: Historial de prompts

### ✏️ Edición de texto

| Atajo | Qué hace |
|---|---|
| `Ctrl+A` / `Ctrl+E` | Inicio / final de la línea |
| `Alt+A` / `Alt+E` | Inicio / final de la línea **visual** (si el texto se ajustó) |
| `Alt+B` / `Alt+F` | Palabra anterior / siguiente (también `Ctrl+←` / `Ctrl+→`) |
| `Ctrl+B` / `Ctrl+F` | Carácter izquierda / derecha |
| `Ctrl+W` · `Ctrl+Backspace` | Borrar la palabra anterior |
| `Alt+D` · `Ctrl+Supr` | Borrar la palabra siguiente |
| `Ctrl+K` / `Ctrl+U` | Borrar hasta el final / el inicio de la línea |
| `Ctrl+Shift+D` | Borrar la línea entera |
| `Ctrl+-` / `Ctrl+.` | Deshacer / rehacer en el texto |
| `Shift+flechas` | Seleccionar |
| `Ctrl+Shift+A` / `Ctrl+Shift+E` | Seleccionar hasta el inicio / final de la línea |
| `Ctrl+C` | Borrar todo el texto del prompt |

## 🗝️ Atajos con la tecla líder (`Ctrl+X` …)

| Después de `Ctrl+X` | Acción | Comando equivalente |
|---|---|---|
| `N` | Sesión nueva | `/new` |
| `L` | Lista de sesiones | `/sessions` |
| `M` | Elegir modelo | `/models` |
| `A` | Elegir agente | `/agents` |
| `C` | Compactar la sesión | `/compact` |
| `U` | Deshacer el último mensaje y sus cambios | `/undo` |
| `R` | Rehacer lo deshecho | `/redo` |
| `E` | Editor externo | `/editor` |
| `G` | Línea de tiempo (saltar a un mensaje) | `/timeline` |
| `X` | Exportar la sesión a tu editor | `/export` |
| `Y` | Copiar mensaje | `/copy` |
| `B` | Mostrar u ocultar la barra lateral | — |
| `T` | Mostrar u ocultar el panel de terminal | `/terminal` abre una nueva |
| `S` | Ver estado | `/status` |
| `W` | Cerrar la pestaña de sesión | — |
| `Q` | Ver los prompts en cola · también salir | — |
| `Enter` | Encolar el prompt | — |
| `I` | Ver imágenes adjuntas | — |
| `1` … `9`, `0` | Ir a la pestaña de sesión 1…10 | — |

⚠️ Cuidado: la documentación lista `Ctrl+X Q` tanto en "salir" como en "gestionar prompts en cola". Si te pasa algo raro con esa combinación, usa `Ctrl+C` para salir y `/` para lo demás.

## 🧭 Otros atajos directos

### 💬 Sesiones y pestañas

| Atajo | Qué hace |
|---|---|
| `Ctrl+O` | Sesiones y proyectos recientes |
| `Ctrl+Tab` / `Ctrl+Shift+Tab` | Pestaña de sesión siguiente / anterior (también `Alt+↓` / `Alt+↑`) |
| `Alt+Shift+↓` / `Alt+Shift+↑` | Siguiente / anterior pestaña **no leída** |
| `Ctrl+Shift+T` | Reabrir la última pestaña cerrada |
| `Ctrl+1` … `Ctrl+0` | Ir a la pestaña 1…10 |
| `Ctrl+R` | Renombrar la sesión |
| `Ctrl+D` | Borrar la sesión (en la lista de sesiones) |
| `Ctrl+F` | Fijar la sesión en la lista |
| `Ctrl+B` | Mandar herramientas que bloquean a segundo plano |
| `Esc` | Interrumpir la sesión |
| `↓` · `←` `→` · `↑` | Subagentes: abrir selector · hijo anterior/siguiente · volver al padre |

### 🤖 Modelos y agentes

| Atajo | Qué hace |
|---|---|
| `Shift+Tab` | Siguiente agente (Build → Plan → …) |
| `F2` / `Shift+F2` | Modelo reciente siguiente / anterior |
| `Ctrl+T` | Ciclar las variantes del modelo (por ejemplo, razonamiento alto/bajo) |
| `Ctrl+A` | En el diálogo de modelos: lista de proveedores |
| `Ctrl+F` | En el diálogo de modelos: marcar favorito |

### 📜 Moverse por la conversación

| Atajo | Qué hace |
|---|---|
| `RePág` / `AvPág` | Una página arriba / abajo (también `Ctrl+Alt+B` / `Ctrl+Alt+F`) |
| `Ctrl+Alt+U` / `Ctrl+Alt+D` | Media página arriba / abajo |
| `Ctrl+Alt+Y` / `Ctrl+Alt+E` | Una línea arriba / abajo |
| `Ctrl+G` · `Inicio` | Primer mensaje |
| `Ctrl+Alt+G` · `Fin` | Último mensaje |
| `Alt+Fin` | Tu último mensaje |
| `Ctrl+Alt+K` | Panel "which-key": muestra qué teclas hay disponibles |
| `Ctrl+Z` | Suspender (vuelves con `fg`) |

### 🧾 Visor de diferencias (`/diff`)

| Tecla | Qué hace |
|---|---|
| `j` / `k` | Bajar / subir |
| `Ctrl+D` / `Ctrl+U` | Media página abajo / arriba |
| `gg` / `G` | Inicio / final del diff |
| `]` / `[` | Bloque de cambios siguiente / anterior |
| `n` / `p` | Archivo siguiente / anterior |
| `m` | Marcar el archivo como revisado |
| `v` | Vista dividida o unificada |
| `s` | Ver un solo archivo |
| `b` | Mostrar u ocultar el árbol de archivos |
| `d` | Qué comparar: todo, commiteado, sin commit o último turno |
| `?` | Más atajos del visor |
| `Esc` / `q` | Cerrar |

## 🧰 Comandos `/` (todos los incorporados)

Sacados del código de la v2.0.32. Escribe `/` y unas letras para filtrar; `Ctrl+P` muestra además las acciones sin comando.

### 💬 Sesiones

- `/new` :: Sesión nueva
- `/sessions` :: Cambiar de sesión (alias `/resume`, `/continue`)
- `/open` :: Abrir sesión o proyecto (alias `/projects`)
- `/clear` :: Limpiar la sesión
- `/rename nombre` :: Renombrar la sesión
- `/fork` :: Bifurcar la sesión
- `/timeline` :: Saltar a un mensaje
- `/compact` :: Compactar (resumir) la sesión
- `/undo` :: Deshacer el mensaje anterior **y** sus cambios en archivos
- `/redo` :: Rehacer lo deshecho
- `/copy` :: Copiar la última respuesta
- `/export` :: Exportar la transcripción
- `/btw pregunta` :: Pregunta al margen; no se añade a la conversación (`C` copia la respuesta)

### 🤖 Modelo y agente

- `/models` :: Cambiar de modelo
- `/agents` :: Cambiar de agente
- `/variants` :: Variante del modelo (alias `/thinking`, `/effort`)
- `/connect` :: Conectar un proveedor o integración
- `/skills` :: Elegir skills
- `/mcps` :: Servidores MCP (activar o desactivar con `Espacio`)

### 🛠️ Trabajo

- `/editor` :: Editar el prompt en tu `$EDITOR`
- `/diff` :: Visor de diferencias
- `/terminal` :: Terminal nueva dentro de OpenCode
- `/cd ruta` :: Cambiar la carpeta de trabajo
- `/worktrees` :: Gestionar espacios de trabajo (worktrees)

### ⚙️ Sistema

- `/settings` :: Ajustes
- `/themes` :: Cambiar tema
- `/status` :: Estado
- `/stats` :: Estadísticas de uso
- `/plugins` :: Plugins
- `/reload` :: Recargar la configuración
- `/restart` :: Reiniciar el servicio
- `/update` :: Actualizar OpenCode
- `/pair` :: Emparejar un dispositivo (alias `/web`)
- `/highlights` :: Volver a ver las novedades de la versión
- `/debug` :: Información de depuración
- `/help` :: Ayuda
- `/exit` :: Salir (alias `/quit`, `/q`)

⚠️ Cuidado: la v2 **no** tiene `/init` ni `/share` (compartir sesiones se eliminó). Escribe tu `AGENTS.md` a mano o pídeselo al agente: "crea un AGENTS.md con los comandos de build y test de este repo".

## 🤖 Agentes: Build, Plan y subagentes

| Agente | Tipo | Para qué |
|---|---|---|
| **Build** (`build`) | principal | Programar. Herramientas permitidas; pide permiso para leer `.env` sensibles y para salir del proyecto |
| **Plan** (`plan`) | principal | Explorar y planear **sin editar** archivos del proyecto |
| **General** (`general`) | subagente | Investigación y tareas de varios pasos (no lanza más subagentes) |
| **Explore** (`explore`) | subagente | Buscar y leer código o web, sin editar |

```flujo
dir: derecha
Plan -> Tú : propone
Tú -> Build : Shift+Tab y aprueba
Build -> Explore : busca cosas
Explore --> Build : resumen
```

### 🧩 Crear tu propio agente

```text
---
description: Revisa cambios buscando errores y regresiones
mode: subagent
model: anthropic/claude-sonnet-4-5#high
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: deny
---
Revisa los cambios actuales. Lista los hallazgos por gravedad con archivo y línea.
```

- `~/.config/opencode/agents/revisor.md` :: Agente para todos tus proyectos
- `.opencode/agents/revisor.md` :: Agente de este proyecto
- `mode: primary` :: Agente principal (sale en `Shift+Tab`); es el valor por defecto
- `mode: subagent` :: Solo lo lanza otro agente, en una sesión hija
- `mode: all` :: Sirve de las dos formas
- `model: proveedor/modelo#variante` :: Modelo preferido (si falta, el subagente hereda el del padre)
- `steps: 8` :: Máximo de pasos antes de resumir
- `hidden: true` :: Ocultarlo de las listas (no es seguridad)

Para usarlo: "usa el subagente revisor para revisar mis cambios".

## 🛡️ Permisos: reglas en orden

🧠 Concepto: cada regla tiene `action` (qué herramienta), `resource` (sobre qué) y `effect` (`allow`, `ask` o `deny`). **Gana la última regla que coincide**, así que va primero lo general y después las excepciones. Si ninguna coincide, pregunta (`ask`).

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    { "action": "shell", "resource": "*", "effect": "ask" },
    { "action": "shell", "resource": "git status *", "effect": "allow" },
    { "action": "shell", "resource": "git diff *", "effect": "allow" },
    { "action": "shell", "resource": "git push *", "effect": "deny" },
    { "action": "read", "resource": "*.env", "effect": "deny" }
  ]
}
```

| Acción | Qué controla |
|---|---|
| `shell` | Comandos de terminal |
| `edit` | Editar, escribir y parchear archivos |
| `read` · `glob` · `grep` | Leer y buscar |
| `webfetch` · `websearch` | Web |
| `subagent` | Qué agentes hijos puede lanzar |
| `skill` | Cargar skills |
| `external_directory` | Salir de la carpeta del proyecto |
| `servidor_herramienta` | Herramientas MCP |

- `*` :: Cualquier cosa (incluye `/`)
- `?` :: Exactamente un carácter
- `git status *` :: También coincide con `git status` sin argumentos
- `~/notas/**` :: En `read`, `edit` y `external_directory` se expanden `~` y `$HOME` (en `shell` no)

⚠️ Cuidado: la v1 usaba otros nombres (`permission`, `bash`, `task`). En la v2 son `permissions`, `shell` y `subagent`. Muchos tutoriales en internet siguen siendo de la v1.

⚠️ Cuidado: por defecto, salir del proyecto (`external_directory`) está **permitido**. Si quieres que pregunte, añade `{ "action": "external_directory", "resource": "*", "effect": "ask" }`.

## 📄 AGENTS.md e instrucciones

- `~/.config/opencode/AGENTS.md` :: Instrucciones globales (tú ya tienes uno)
- `./AGENTS.md` :: Del proyecto; también se leen los de las carpetas de arriba hasta la raíz del proyecto
- `packages/web/AGENTS.md` :: Los de subcarpetas se cargan cuando el agente lee archivos de ahí
- `"instructions": [...]` :: Más archivos, globs o URLs en la config

```json
{
  "instructions": ["CONTRIBUTING.md", "docs/guidelines/*.md", "~/rules/opencode.md"]
}
```

⚠️ Cuidado: OpenCode v2 reconoce **solo** `AGENTS.md`; no usa `CLAUDE.md` como respaldo. Si editas un `AGENTS.md` mientras trabajas, OpenCode lo detecta y avisa al agente antes del siguiente mensaje.

## ⚙️ Archivos de configuración

| Archivo | Para qué |
|---|---|
| `~/.config/opencode/opencode.jsonc` | Config global: modelo, permisos, agentes, MCP, plugins |
| `opencode.jsonc` o `.opencode/opencode.jsonc` | Config del proyecto |
| `~/.config/opencode/cli.json` | Solo la terminal: atajos, tema, avisos (en la v2 reemplaza a `tui.json`) |
| `.opencode/agents/` · `.opencode/commands/` · `.opencode/skills/` | Agentes, comandos y skills del proyecto |
| `/etc/opencode/` | Config del sistema (todos los usuarios) |

### 🎛️ Cambiar atajos (`cli.json`)

```json
{
  "$schema": "https://opencode.ai/v2/cli.json",
  "keybinds": {
    "leader": "ctrl+space",
    "command.palette.show": "ctrl+k",
    "model.list": "<leader>m",
    "app.debug": "none"
  },
  "leader": { "timeout": 2000 }
}
```

- `"ctrl+c,ctrl+d"` :: Varias teclas para lo mismo, separadas por coma
- `"none"` o `false` :: Desactivar un atajo
- `leader.timeout` :: Milisegundos que espera la segunda tecla tras `Ctrl+X`

### ✍️ Comandos propios

```text
.opencode/commands/revisar.md
---
description: Revisar código buscando errores
agent: plan
---
Revisa $ARGUMENTS. Primero los errores, luego los tests que faltan.
Cambios actuales:
!`git diff --stat`
```

📌 Nota: un `!` seguido de un comando entre comillas invertidas (como en la última línea) inserta la salida de ese comando antes de enviar. Se ejecuta **sin** pasar por los permisos: úsalo solo con comandos de confianza.

- `/revisar src/auth.ts` :: `$ARGUMENTS` se reemplaza por `src/auth.ts`
- `$1`, `$2` :: Argumentos por posición (las comillas agrupan palabras)
- `~/.config/opencode/commands/` :: Comandos para todos tus proyectos
- `subagent: true` :: Ejecutarlo en una sesión hija en segundo plano

## 🔌 MCP y modo sin interfaz

```bash
# Servidor remoto
opencode mcp add context7 --url https://mcp.context7.com/mcp

# Servidor local en la config global (todo después de -- es el comando)
opencode mcp add everything --global -- npx -y @modelcontextprotocol/server-everything

opencode mcp list        # estado de cada servidor
opencode mcp auth sentry # login OAuth
```

📌 Nota: en este PC `opencode mcp list` muestra `context7` y `playwright` conectados, y `github` y `vercel` pidiendo autenticación (`opencode mcp auth github`).

```bash
# Una pregunta y salir
opencode run "Explica este repositorio"

# Con modelo, agente y archivos adjuntos
opencode run --model anthropic/claude-sonnet-4-5 --agent plan --file src/server.ts "Busca bugs"

# Seguir la última sesión, o salida JSON para scripts
opencode run --continue "Ahora maneja el caso expirado"
opencode run --format json "Lista los comentarios TODO"
```

## 🧑‍🍳 Recetas rápidas

### ✅ Planear y luego construir

1. `Shift+Tab` hasta el agente **Plan**.
2. "Lee @src/auth.ts y propón cómo validar contraseñas vacías, con test. No edites."
3. Ajusta el plan escribiendo en el chat.
4. `Shift+Tab` a **Build**: "Implementa el plan y corre los tests."
5. `/diff`, revisa con `j`/`k`, marca con `m` lo revisado.

### ✅ Me equivoqué

1. `Ctrl+X U` (o `/undo`): revierte tu último mensaje y los archivos que cambió; tu prompt vuelve al cuadro para editarlo.
2. Corrige el texto y envía: así se confirma la reversión.
3. ¿Mejor como estaba? `Ctrl+X R` (o `/redo`) **antes** de enviar algo nuevo.

### ✅ Probar con otro modelo

- `F2` :: Alternar entre tus modelos recientes en un segundo
- `Ctrl+X M` :: Elegir cualquier modelo de tus proveedores
- `Ctrl+T` :: Misma IA, más o menos razonamiento

## 🇬🇧 Vocabulario

🇬🇧 **leader key** /ˈliː.dər/ — tecla líder · **command palette** /ˈpæl.ət/ — paleta de comandos · **which-key** — "¿qué tecla?"
🇬🇧 **to steer** — corregir el rumbo · **to queue** — encolar · **stash** — guardado temporal
🇬🇧 **variant** /ˈveə.ri.ənt/ — variante · **provider** /prəˈvaɪ.dər/ — proveedor · **child session** — sesión hija
🇬🇧 **effect: allow / ask / deny** — permitir / preguntar / negar · **last match wins** — gana la última coincidencia
🇬🇧 **hunk** /hʌŋk/ — bloque de cambios de un diff · **to revert** — revertir · **reviewed** — revisado
🇬🇧 Frase útil: "Switch to the plan agent and outline the steps first." — Cambia al agente plan y resume primero los pasos.
🇬🇧 Frase útil: "Use the explore subagent to find where tokens are validated." — Usa el subagente explore para encontrar dónde se validan los tokens.
