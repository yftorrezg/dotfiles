# 🌀 Codex · Atajos, comandos y config
> El agente de OpenAI en la terminal (codex-cli 0.166.0 en este PC): atajos reales sacados de su código, todos los comandos `/`, permisos y sandbox, AGENTS.md, config.toml, `exec` y `review`.

## 🧭 Resumen en 30 segundos

Esto es **exactamente** lo que muestra Codex al pulsar `?` (en Linux `⌃` = Ctrl, `⌥` = Alt, `⇧` = Shift):

| Grupo | Atajo | Qué hace |
|---|---|---|
| Escribir | `/` | Comandos |
| Escribir | `@` | Mencionar archivos |
| Escribir | `!` | Comando de shell |
| Escribir | `Ctrl+J` | Nueva línea |
| Escribir | `Ctrl+V` | Pegar imagen |
| Escribir | `Ctrl+G` | Editor externo |
| Escribir | `Ctrl+R` | Buscar en el historial |
| Escribir | `Esc Esc` | Editar el último mensaje |
| Sesión | `Tab` | Encolar el mensaje mientras trabaja |
| Sesión | `Alt+,` | Menos razonamiento |
| Sesión | `Alt+.` | Más razonamiento |
| Sesión | `Alt+←` / `Alt+→` | Subagentes (con el prompt vacío) |
| Sesión | `F4` | Inspeccionar la actividad |
| Sesión | `Ctrl+C` | Salir |
| Transcripción | `Ctrl+T` | Abrir la transcripción |
| Transcripción | `F3` | Buscar texto |
| Transcripción | `RePág` / `AvPág` | Desplazar |
| Transcripción | `Ctrl+Espacio` | Empezar a seleccionar |
| Transcripción | `Ctrl+Inicio` / `Ctrl+Fin` | Arriba del todo / lo último |

📌 Nota: la ayuda termina con `/keymap customize`: con `/keymap` puedes cambiar cualquiera de estos atajos.

## 🚀 Arrancar desde la terminal

- `codex` :: Abre la interfaz interactiva (TUI) en la carpeta actual
- `codex "explica este repo"` :: Abre y manda ese primer mensaje
- `codex -m gpt-6.1-terra` :: Elegir modelo para esta sesión
- `codex -i captura.png "¿qué falla aquí?"` :: Adjuntar imágenes al primer mensaje
- `codex -C ruta/al/proyecto` :: Usar otra carpeta como raíz de trabajo
- `codex --add-dir ../libs` :: Dar permiso de escritura a otra carpeta además de la principal
- `codex --search` :: Activar búsqueda web en vivo
- `codex --worktree` :: Trabajar en un worktree de git nuevo y aislado
- `codex -s read-only` :: Sandbox: `read-only`, `workspace-write` o `danger-full-access`
- `codex -a never` :: Aprobaciones: `on-request` (el modelo decide cuándo pedir) o `never`
- `codex --approve-for-me` :: Una revisión automática aprueba lo seguro (sandbox workspace-write)
- `codex -p trabajo` :: Usar el perfil `~/.codex/trabajo.config.toml` encima de tu config
- `codex -c model_reasoning_effort="high"` :: Cambiar cualquier ajuste de config.toml solo esta vez
- `codex --oss --local-provider ollama` :: Usar un modelo local (Ollama o LM Studio)
- `codex --no-alt-screen` :: Modo en línea: conserva el scroll normal de la terminal
- `codex resume` :: Elegir una sesión anterior (`--last` = la más reciente, `--all` = de todas las carpetas)
- `codex fork --last` :: Copiar la última sesión en una nueva para probar otro camino
- `codex login` / `codex logout` :: Iniciar o cerrar sesión
- `codex doctor` :: Diagnóstico de instalación, config, login y entorno
- `codex update` :: Actualizar Codex
- `codex completion zsh` :: Generar autocompletado para tu shell (`bash`, `zsh`, `fish`…)

⚠️ Cuidado: `--dangerously-bypass-approvals-and-sandbox` quita **todas** las confirmaciones y el sandbox. La propia ayuda dice "EXTREMELY DANGEROUS": solo para entornos que ya están aislados por fuera (contenedor, VM).

📌 Nota: en esta versión, `approval_policy` solo acepta `on-request` y `never`. El valor antiguo `untrusted` fue retirado según la documentación oficial; si lo ves en tutoriales viejos, ya no aplica.

## ⌨️ Todos los atajos por defecto

### 💬 Chat y sesión

| Atajo | Qué hace |
|---|---|
| `Enter` | Enviar. Si Codex está trabajando, tu mensaje **corrige el rumbo** del turno actual |
| `Tab` | Encolar el mensaje mientras hay una tarea corriendo (se envía al terminar el turno) |
| `Esc` | Interrumpir el turno |
| `Esc Esc` | Editar tu último mensaje (y rehacer desde ahí) |
| `Shift+←` o `Alt+↑` | Avanzar por las preguntas pendientes y luego editar el último mensaje en cola |
| `Shift+→` o `Alt+↓` | Retroceder por las preguntas hacia el cuadro de texto |
| `Alt+,` o `Shift+↓` | Bajar el esfuerzo de razonamiento |
| `Alt+.` o `Shift+↑` | Subir el esfuerzo de razonamiento |
| `Shift+Tab` | Cambiar de modo (por ejemplo, entrar o salir del modo Plan) |
| `Ctrl+]` | Saltar una pregunta que te hace Codex |
| `Alt+←` / `Alt+→` | Moverte entre subagentes (con el prompt vacío) |
| `Ctrl+C` | Salir |

### 🪟 Ventanas y vistas

| Atajo | Qué hace |
|---|---|
| `Ctrl+T` | Abrir la transcripción completa |
| `F3` | Buscar texto en la transcripción |
| `F4` | Enfocar los grupos de actividad para abrir o cerrar sus detalles |
| `F2` | Ver advertencias guardadas |
| `Ctrl+O` | Copiar la última respuesta |
| `Ctrl+L` | Limpiar la terminal |
| `Ctrl+G` | Escribir el mensaje en tu editor (`$VISUAL` o `$EDITOR`) |
| `Alt+R` | Modo de scroll "crudo": copiar texto con el mouse sin bordes |
| `Ctrl+/` | Saltar entre la conversación al margen y la principal |
| `F8` | Voz sí/no |
| `F9` | Silenciar o activar el micrófono |
| `?` | Ayuda de atajos (con el prompt vacío) |

### ✏️ Editar el texto

| Atajo | Qué hace |
|---|---|
| `Ctrl+J` · `Shift+Enter` · `Alt+Enter` | Nueva línea |
| `Ctrl+A` / `Ctrl+E` | Inicio / final de la línea (también `Inicio` / `Fin`) |
| `Alt+B` / `Alt+F` | Palabra anterior / siguiente (también `Ctrl+←` / `Ctrl+→`) |
| `Ctrl+W` · `Alt+Backspace` | Borrar la palabra anterior |
| `Alt+D` · `Ctrl+Supr` | Borrar la palabra siguiente |
| `Ctrl+U` | Borrar hasta el inicio de la línea |
| `Ctrl+K` | Borrar hasta el final de la línea |
| `Ctrl+Y` | Pegar lo último borrado |
| `Ctrl+B` / `Ctrl+F` | Carácter izquierda / derecha |
| `Ctrl+P` / `Ctrl+N` | Arriba / abajo |
| `Ctrl+H` / `Ctrl+D` | Borrar carácter atrás / adelante |
| `Ctrl+R` / `Ctrl+S` | Buscar en el historial hacia atrás / adelante |

🧠 Concepto: son los mismos atajos de **readline** (bash, zsh, Emacs). Lo que aprendas aquí te sirve en toda la terminal.

### 🟩 Modo vim (`/vim`)

| Tecla | Qué hace |
|---|---|
| `i` `a` `I` `A` | Insertar antes / después / al inicio / al final |
| `o` / `O` | Línea nueva abajo / arriba |
| `R` | Modo reemplazar |
| `h j k l` | Moverse |
| `w` `b` `e` | Palabra siguiente / anterior / final |
| `0` / `$` | Inicio / final de la línea |
| `G` | Ir al final |
| `f` `F` `t` `T` | Saltar a un carácter |
| `x` `r` `s` | Borrar / reemplazar / sustituir carácter |
| `dd` `D` | Borrar línea / hasta el final |
| `cw` `C` `ciw` | Cambiar palabra / hasta el final / palabra interior |
| `yy` `Y` `p` | Copiar línea / pegar |
| `u` / `Ctrl+R` | Deshacer / rehacer |
| `.` | Repetir el último cambio |

📌 Nota: objetos de texto con `i`/`a`: `w`, `W`, `(` o `b`, `[`, `{` o `B`, `"`, `'` y la comilla invertida.

### 🎛️ Cambiar atajos en config.toml

```text
# ~/.codex/config.toml
[tui.keymap.global]
open_transcript = "ctrl-t"

[tui.keymap.composer]
submit = ["enter", "ctrl-m"]

[tui.keymap.chat]
interrupt_turn = "f12"
```

💡 Consejo: más fácil que escribirlo a mano: `/keymap` abre un selector, pulsas la acción y luego la tecla nueva.

## 🧰 Comandos `/` (todos)

Estos son los comandos de la versión 0.166 en el **orden** del menú (los más usados arriba). Algunos solo aparecen si tu cuenta o sistema los soporta (por ejemplo `/app` solo en macOS y Windows).

### 🧠 Modelo, modo y permisos

- `/model` :: Elegir modelo y esfuerzo de razonamiento
- `/permissions` :: Elegir qué puede hacer Codex (ver sección de permisos)
- `/plan` :: Pasar a modo Plan (investiga y planea, no edita)
- `/goal` :: Fijar o ver el objetivo de una tarea larga
- `/approve` :: Aprobar un reintento de algo que la revisión automática rechazó
- `/presets` :: Ejecutar o guardar prompts y comandos reutilizables
- `/experimental` :: Activar o desactivar funciones experimentales
- `/setup-default-sandbox` :: Configurar el sandbox elevado del agente
- `/daybreak` :: Activar o desactivar Daybreak
- `/voice` :: Empezar o parar la voz (`/voice settings` para elegir voz)

### 💬 Sesiones

- `/new` :: Chat nuevo sin salir de Codex
- `/clear` :: Limpiar la terminal y empezar chat nuevo
- `/resume` :: Retomar un chat guardado
- `/fork` :: Bifurcar el chat actual
- `/rename` :: Renombrar la conversación
- `/archive` :: Archivar esta sesión
- `/delete` :: Borrar esta sesión para siempre
- `/worktree` :: Empezar o seguir la conversación en un worktree nuevo
- `/side` o `/btw` :: Conversación al margen en una copia temporal (no ensucia el chat)
- `/compact` :: Resumir la conversación para no llegar al límite de contexto
- `/recap` :: Resumir ahora la conversación
- `/copy` :: Copiar la última respuesta o una parte
- `/export` :: Exportar la conversación como Markdown
- `/quit` o `/exit` :: Salir de Codex

### 🛠️ Proyecto y código

- `/init` :: Crear un `AGENTS.md` con instrucciones para Codex
- `/review` :: Revisar tus cambios actuales y buscar problemas
- `/diff` :: Ver el `git diff` (incluye archivos sin seguimiento)
- `/mention` :: Mencionar un archivo
- `/cd` :: Cambiar la carpeta de trabajo · `/pwd` muestra la actual
- `/ide` :: Traer contexto de tu IDE: selección, archivos abiertos…
- `/import` :: Importar config, proyecto y chats recientes desde Claude Code

### 🤖 Agentes y procesos

- `/agents` :: Abrir el centro de mando de agentes
- `/subagents` :: Cambiar entre los subagentes de esta sesión
- `/ps` :: Listar las terminales en segundo plano
- `/stop` :: Parar todas las terminales de fondo (alias `/clean`)

### 🧩 Extensiones

- `/skills` :: Usar skills para mejorar cómo hace ciertas tareas
- `/mcp` :: Listar herramientas MCP (`/mcp verbose`, `/mcp login nombre`)
- `/plugins` :: Explorar plugins
- `/apps` :: Gestionar apps
- `/hooks` :: Ver y gestionar hooks del ciclo de vida
- `/memories` :: Configurar el uso y la generación de memorias

### ⚙️ Interfaz y diagnóstico

- `/status` :: Configuración de la sesión y tokens usados
- `/usage` :: Uso de la cuenta (o usar un reinicio del límite)
- `/config` :: Preferencias de Codex
- `/keymap` :: Cambiar atajos
- `/vim` :: Modo vim sí/no en el cuadro de texto
- `/theme` :: Tema de resaltado de código
- `/statusline` :: Qué aparece en la barra de estado
- `/title` :: Qué aparece en el título de la terminal
- `/tui` :: Modo de la interfaz para el próximo arranque
- `/raw` :: Modo crudo para copiar texto cómodo
- `/pets` :: Elegir u ocultar la mascota de la terminal
- `/daemon` :: Gestionar el servidor local de fondo
- `/warnings` :: Ver advertencias guardadas y detalles
- `/debug-config` :: Ver las capas de config y de dónde sale cada valor
- `/feedback` :: Enviar registros a los desarrolladores
- `/logout` :: Cerrar sesión

💡 Consejo: muchos comandos aceptan argumentos en la misma línea: `/review enfócate en seguridad`, `/model …`, `/rename login-fix`, `/plan migrar a Vite`.

📌 Nota: mientras Codex trabaja, algunos comandos se pueden usar al momento (`/diff`, `/status`, `/copy`, `/model`, `/usage`…) y otros esperan a que termine el turno (`/new`, `/init`, `/compact`, `/review`, `/plan`…).

## 🛡️ Permisos y sandbox

🧠 Concepto: Codex separa dos cosas. El **sandbox** limita técnicamente lo que pueden tocar los comandos (carpetas, internet). La **política de aprobación** decide cuándo te pregunta.

`/permissions` muestra 4 opciones (texto real de la 0.166):

| Opción | Qué permite |
|---|---|
| **Ask for approval** | Lee y edita la carpeta del proyecto y corre comandos; pide permiso para internet o editar fuera |
| **Approve for me** | Solo pregunta por acciones detectadas como potencialmente peligrosas |
| **Full Access** | Edita fuera del proyecto y usa internet sin preguntar. "Use with caution" |
| **Read Only** | Solo lee; pide permiso para editar o usar internet |

| Sandbox (`-s`) | Qué pueden hacer los comandos |
|---|---|
| `read-only` | Leer, nada de escribir |
| `workspace-write` | Escribir solo dentro del proyecto (y las `--add-dir`) |
| `danger-full-access` | Todo, sin sandbox |

```text
# ~/.codex/config.toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

✅ Bien: trabajar con **Ask for approval** y subir a **Approve for me** cuando la tarea es larga y conoces el proyecto.
❌ Mal: **Full Access** en tu carpeta personal "para que no moleste".

## 📄 AGENTS.md: instrucciones del proyecto

1. **Global**: en `~/.codex/` lee `AGENTS.override.md` si existe; si no, `AGENTS.md`.
2. **Proyecto**: desde la raíz del repo (git) baja hasta tu carpeta actual. En cada carpeta toma **un** archivo: `AGENTS.override.md`, si no `AGENTS.md`, si no los nombres de `project_doc_fallback_filenames`.
3. Los junta de arriba abajo; lo más cercano a tu carpeta va al final y pesa más.
4. Deja de añadir al llegar a `project_doc_max_bytes` (por defecto **32 KiB**).

```arbol
~/.codex/AGENTS.md          (global)
mi-repo/
  AGENTS.md                 (todo el repo)
  services/
    pagos/
      AGENTS.override.md    (reemplaza al AGENTS.md de esta carpeta)
```

```text
# ~/.codex/config.toml — leer también otros nombres de archivo
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
project_doc_max_bytes = 65536
```

💡 Consejo: para comprobar qué instrucciones cargó: `codex --ask-for-approval never "Summarize the current instructions."` (ejemplo de la documentación oficial).

## ⚙️ config.toml

| Archivo | Alcance |
|---|---|
| `~/.codex/config.toml` | Tu config de usuario |
| `.codex/config.toml` | Config del proyecto (solo si confías en el proyecto) |
| `~/.codex/<perfil>.config.toml` | Perfil que activas con `-p perfil` |
| `/etc/codex/config.toml` | Config del sistema |

Orden de prioridad (gana el de arriba): flags y `-c` → config del proyecto → perfil → usuario → config de la nube → sistema → valores por defecto.

```text
# ~/.codex/config.toml (ejemplo)
model = "gpt-6.1-terra"
model_reasoning_effort = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"        # cached | indexed | live | disabled
personality = "none"

[features]
memories = true              # activar una función (o: codex --enable memories)

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

- `web_search = "cached"` :: Por defecto: resultados del caché de búsqueda
- `web_search = "live"` :: Datos frescos de la web (igual que `--search`)
- `codex features` :: Ver qué funciones existen y cuáles están activas
- `/debug-config` :: Ver de qué capa sale cada valor

📌 Nota: tu `~/.codex/config.toml` actual tiene `model = "gpt-6.1-terra"` y `model_reasoning_effort = "medium"`.

## 🤖 Sin interfaz: `codex exec`

```bash
# Tarea y salir (alias: codex e)
codex exec "arregla el test que falla en tests/test_api.py"

# Pasarle datos por stdin (con '-' o por tubería)
git diff | codex exec "escribe un mensaje de commit para este diff"

# Eventos en JSONL para scripts y guardar la respuesta final en un archivo
codex exec --json "lista los TODO" > eventos.jsonl
codex exec -o resumen.md "resume la arquitectura del proyecto"

# Respuesta con forma fija
codex exec --output-schema esquema.json "extrae nombre y versión de package.json"

# Fuera de un repo git, o sin guardar la sesión en disco
codex exec --skip-git-repo-check --ephemeral "explica este script"

# Continuar la última sesión de exec
codex exec resume --last "ahora añade los tests"
```

### 🔍 Revisar código sin abrir la interfaz

- `codex review --uncommitted` :: Revisar lo staged, lo no staged y lo nuevo sin seguimiento
- `codex review --base main` :: Revisar tu rama comparada con `main` (estilo PR)
- `codex review --commit abc123` :: Revisar lo que introdujo un commit
- `codex review "enfócate en seguridad"` :: Instrucciones propias para la revisión

## 🔌 MCP, skills y más

```bash
# Servidor local (stdio): después de -- va el comando
codex mcp add context7 -- npx -y @upstash/context7-mcp

# Servidor remoto (HTTP), con token leído de una variable de entorno
codex mcp add mi-api --url https://api.ejemplo.com/mcp --bearer-token-env-var MI_API_TOKEN

codex mcp list        # ver todos
codex mcp get context7
codex mcp remove context7
codex mcp login nombre   # OAuth
```

- `~/.agents/skills/<nombre>/SKILL.md` :: Skills de usuario (aquí ya tienes `systematic-debugging`, `test-driven-development`…)
- `.agents/skills/<nombre>/SKILL.md` :: Skills del proyecto
- `/skills` :: Ver y usar los skills
- `codex plugin` :: Gestionar plugins
- `codex cloud` :: (experimental) ver tareas de Codex Cloud y aplicar sus cambios
- `codex apply <id>` :: Aplicar con `git apply` el diff de una tarea de la nube (alias `codex a`)
- `codex sandbox` :: Ejecutar un comando dentro del sandbox de Codex

## 🧑‍🍳 Recetas rápidas

### ✅ Arreglar algo con cuidado

1. `/permissions` → **Ask for approval**.
2. `Shift+Tab` (o `/plan`): "Investiga por qué falla el login con contraseña vacía en @src/auth.ts y propón un plan con test. No edites."
3. Revisa el plan, ajústalo y sal del modo Plan para que implemente.
4. Mientras trabaja, escribe y pulsa `Enter` para corregir ("usa pytest, no unittest") o `Tab` para dejar la siguiente tarea en cola.
5. `/diff` y `/review` antes de hacer commit.

### ✅ Me equivoqué en el mensaje

- `Esc Esc` :: Editar tu último mensaje y rehacer desde ahí
- `Shift+←` :: Editar el último mensaje que todavía está en cola

### ✅ Probar otra idea sin perder la actual

- `/fork` :: Copia el chat y sigues en la copia
- `/worktree` :: Trabaja en un worktree nuevo para que los archivos tampoco choquen

⚠️ Cuidado: Codex 0.166 no tiene `/undo`. Para deshacer cambios de archivos usa git (`git diff`, `git restore archivo`, `git stash`). Haz commit antes de tareas grandes.

## 🇬🇧 Vocabulario

| English | Suena | Español |
|---|---|---|
| to steer | tu stíir | corregir el rumbo |
| queue / turn | kiú / tern | cola / turno (un pedido y su trabajo) |
| reasoning effort | rísoning éfort | esfuerzo de razonamiento |
| approval policy | apruval pólisi | política de aprobación |
| sandbox / workspace | sándboks / uérk-spéis | entorno aislado / carpeta de trabajo |
| full access | ful ákses | acceso total |
| rollout | róul-aut | registro de la sesión |
| side conversation | said konverséishon | conversación al margen |
| keymap | kí-map | mapa de teclas |
| uncommitted changes | ankomíted chéinyes | cambios sin commit |
| base branch | beis branch | rama base |
| "Review my uncommitted changes and list issues by severity." | riviú mai ankomíted chéinyes and list íshus bai sevériti | Revisa mis cambios sin commit y lista los problemas por gravedad |
| "Keep the public API unchanged." | kip de páblik ei-pi-ái anchéinchd | No cambies la API pública |
