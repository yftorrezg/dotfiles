# 🇬🇧 Inglés 3 · Equipo, entrevistas y carrera
> Commits, PRs, code review, chat, emails, reuniones, entrevistas y trabajo remoto: el inglés que te da trabajo.

## 🧭 Cómo usar esta hoja

En un equipo internacional tu inglés se nota **antes** que tu código: en el commit, en el PR, en el mensaje de Slack y en la entrevista. Aquí está el inglés "social" del programador, con frases listas para copiar y los errores que otros ya cometieron para que tú no los repitas.

| Situación | Sección | Lo más importante |
|---|---|---|
| Guardar cambios en Git | 📝 Commits | Imperativo: `fix: handle empty list` |
| Reportar un problema | 🐛 Issues | Pasos para reproducir + expected vs actual |
| Proponer código | 🔀 Pull requests | Qué, por qué y cómo probarlo |
| Revisar código ajeno | 🔍 Code review | Critica el código, no a la persona |
| Pedir ayuda en internet | ❓ Preguntar bien | Ejemplo mínimo reproducible |
| Escribir en Slack | 💬 Chat de trabajo | Nada de "hi" solo: di todo en un mensaje |
| Escribir a un cliente | 📧 Emails | Asunto claro, una petición por email |
| Reunión diaria | ☀️ Standup | Ayer, hoy, bloqueos en 30 segundos |
| Entrevista | 🎤 Entrevistas | STAR + pensar en voz alta |
| Cobrar en dólares | 🌎 Trabajo remoto | Contractor, invoice, rate |

💡 Consejo: no memorices todo. Elige **una sección por semana** y úsala en tu vida real (tus propios repos, un Discord, tus apuntes). El inglés que usas se queda; el que solo lees se olvida.

📌 Regla de oro de toda la hoja: **claro > elegante**. Un inglés simple, corto y directo es más profesional que uno "bonito" y confuso.

## 📝 Mensajes de commit

Un commit es una nota para tu equipo del futuro (y para ti en 6 meses). Se escribe en **imperativo presente**, como una orden: "**Add** login page", no "Added" ni "Adding". Truco: la frase debe completar **"If applied, this commit will ___"**.

### 📐 Anatomía de un commit

```text
<type>(<scope>): <short summary in imperative mood>
                                      ← línea en blanco obligatoria
<body: what changed and WHY, wrapped at ~72 chars>
                                      ← línea en blanco
<footer: BREAKING CHANGE: ..., Closes #123, Co-authored-by: ...>
```

| Parte | Obligatoria | Regla | Ejemplo |
|---|---|---|---|
| type | Sí | Una palabra de la lista | `feat`, `fix` |
| scope | No | Módulo afectado, entre paréntesis | `(auth)`, `(api)` |
| summary | Sí | Imperativo, ≤ 50–72 caracteres, sin punto | `add Google sign-in` |
| body | No | El porqué, no el cómo | `Users asked for...` |
| footer | No | Metadatos | `Closes #42` |

### 🏷️ Conventional Commits: los tipos

| Tipo | Cuándo | Ejemplo | Sube versión |
|---|---|---|---|
| feat | Nueva funcionalidad para el usuario | `feat: add dark mode toggle` | minor (1.**2**.0) |
| fix | Corrección de un bug | `fix: prevent crash on empty input` | patch (1.2.**1**) |
| docs | Solo documentación | `docs: update installation steps` | no |
| style | Formato, espacios, comas (sin cambiar lógica) | `style: format with black` | no |
| refactor | Reestructurar sin cambiar comportamiento | `refactor: extract auth logic into service` | no |
| perf | Mejora de rendimiento | `perf: cache user queries` | patch |
| test | Añadir o corregir tests | `test: add unit tests for parser` | no |
| build | Build, empaquetado, dependencias | `build: bump numpy to 2.1` | no |
| ci | Integración continua | `ci: run tests on pull requests` | no |
| chore | Mantenimiento que no toca src ni tests | `chore: remove unused files` | no |
| revert | Deshacer un commit anterior | `revert: undo "feat: add dark mode"` | depende |
| `feat!` / `fix!` | Cambio que rompe compatibilidad | `feat!: drop Python 3.8 support` | major (**2**.0.0) |

💡 Consejo: `feat` y `fix` son "para el usuario"; `refactor`, `style`, `test`, `chore` son "para el desarrollador". Si dudas entre `feat` y `refactor`, pregúntate: ¿el usuario nota algo nuevo?

```arbol
Commit
  Para el usuario
    feat : algo nuevo
    fix : un bug corregido
    perf : más rápido
  Para el desarrollador
    refactor : misma conducta
    test : pruebas
    docs : documentación
    chore : mantenimiento
```

### ⚙️ Verbos de commit en imperativo

| Verbo | Significa | Úsalo para | Ejemplo |
|---|---|---|---|
| add | añadir | Algo nuevo | `feat: add CSV export` |
| remove | quitar | Borrar código/archivos | `chore: remove legacy API client` |
| fix | arreglar | Bugs | `fix: correct typo in error message` |
| update | actualizar | Cambios genéricos (evítalo si hay uno más preciso) | `docs: update README badges` |
| rename | renombrar | Cambiar nombres | `refactor: rename utils to helpers` |
| move | mover | Cambiar de lugar | `refactor: move config to settings.py` |
| refactor | reestructurar | Mejorar sin cambiar conducta | `refactor: simplify date parsing` |
| bump | subir versión | Dependencias o versión | `build: bump axios to 1.7.2` |
| revert | revertir | Deshacer | `revert: revert "add caching layer"` |
| replace | reemplazar | Cambiar X por Y | `refactor: replace moment with date-fns` |
| extract | extraer | Sacar a función/módulo | `refactor: extract validation into hook` |
| handle | manejar | Casos o errores | `fix: handle timeout from payment API` |
| prevent | evitar | Impedir un fallo | `fix: prevent double form submission` |
| allow | permitir | Habilitar algo | `feat: allow uploads up to 50 MB` |
| support | dar soporte | Nuevas plataformas/formatos | `feat: support WebP images` |
| drop | abandonar | Dejar de soportar | `build!: drop Node 16 support` |
| improve | mejorar | Calidad, mensajes, UX | `feat: improve error messages on login` |
| simplify | simplificar | Menos complejidad | `refactor: simplify retry logic` |
| clean up | limpiar | Orden general | `chore: clean up unused imports` |
| deprecate | marcar obsoleto | Avisar que algo se irá | `feat: deprecate v1 endpoints` |
| enable / disable | activar / desactivar | Flags, opciones | `ci: enable caching for pip` |
| tweak | ajustar | Cambio pequeño | `style: tweak button padding` |
| wire up | conectar | Unir piezas | `feat: wire up search bar to API` |
| guard against | protegerse de | Validaciones | `fix: guard against negative prices` |

⚠️ Cuidado: **"fix bug"** no dice nada. Di **qué** bug: `fix: prevent crash when cart is empty`. Y no repitas el verbo: `fix: fix login` suena pobre; mejor `fix: redirect to dashboard after login`.

### ❌ Malos vs ✅ buenos (30 ejemplos)

| ❌ Malo | Problema | ✅ Bueno |
|---|---|---|
| `fix` | No dice nada | `fix: handle null user in profile page` |
| `changes` | Vago | `refactor: split app.py into modules` |
| `asdf` | Basura | `chore: add .env.example` |
| `update stuff` | Vago | `docs: update setup steps for Windows` |
| `final final v2` | Sin significado | `feat: add PDF report generation` |
| `Added login` | Pasado | `feat: add login page` |
| `Adding tests` | Gerundio | `test: add tests for auth service` |
| `fixed the bug.` | Pasado + punto + vago | `fix: correct total in shopping cart` |
| `arreglé el login` | En español | `fix: show error on wrong password` |
| `WIP` | No es un cambio terminado | `feat: add draft of search filters` |
| `Fix Bug In Login` | Mayúsculas en todo | `fix: keep session after page reload` |
| `fix: fix fix` | Repetido | `fix: escape HTML in comments` |
| `feat: I added a new button that...` | Primera persona, largo | `feat: add share button to posts` |
| `update index.js` | Dice el archivo, no el cambio | `fix: validate email before submit` |
| `misc` | Mezcla de cosas | Haz varios commits pequeños |
| `fix + feat + docs` | Varios cambios juntos | Un commit por idea |
| `refactor: changes` | Tipo bien, resumen vacío | `refactor: replace for loops with map` |
| `feat: dark mode and also fixed the navbar` | 2 cosas | 2 commits separados |
| `oops` | Informal, vago | `fix: restore missing import in main.py` |
| `please work` | Frustración en el historial | `ci: set correct Python version` |
| `test` | Ambiguo | `test: cover empty input in parser` |
| `minor changes` | ¿Cuáles? | `style: rename variables for clarity` |
| `feat: added the feature` | Circular | `feat: add password reset via email` |
| `bump` | ¿Qué? ¿a cuánto? | `build: bump torch to 2.4.0` |
| `docs: readme` | Sin verbo | `docs: add usage examples to README` |
| `Merge branch 'main'` (x20) | Ruido en el historial | Usa `git pull --rebase` |
| `fix typo` (en código) | Sin tipo ni lugar | `fix: correct typo in config key` |
| `refactoring everything` | Gerundio, enorme | Refactor por partes, commits pequeños |
| `feat(ml): model` | Sin verbo | `feat(ml): add early stopping to training` |
| `fix: fixes #12` | El resumen no explica | `fix: prevent duplicate emails` + `Closes #12` |

💡 Consejo: si no puedes resumir el commit en una línea, probablemente **hace demasiadas cosas**. Divídelo con `git add -p`.

### 📖 El cuerpo: explica el PORQUÉ

El diff ya muestra **qué** cambió. El cuerpo debe contar **por qué** y cualquier cosa que no se vea en el código.

```text
fix(api): retry payment requests on 503 errors

The payment provider sometimes returns 503 during peak hours.
Before this change, we showed a generic error and users had to
pay again, which caused duplicate charges in some cases.

Now we retry up to 3 times with exponential backoff (1s, 2s, 4s).
The idempotency key prevents double charges.

Closes #318
```

📌 Traducción: "El proveedor de pagos a veces devuelve 503 en horas pico. Antes mostrábamos un error genérico y el usuario pagaba otra vez (cobros duplicados). Ahora reintentamos 3 veces con espera exponencial; la clave de idempotencia evita cobros dobles."

| Frase para el cuerpo | Traducción |
|---|---|
| Before this change, ... | Antes de este cambio, ... |
| This caused ... | Esto causaba ... |
| Now we ... | Ahora ... |
| This makes it easier to ... | Esto facilita ... |
| As a side effect, ... | Como efecto secundario, ... |
| This is a temporary workaround until ... | Es un parche temporal hasta que ... |
| See the discussion in #42. | Ver la discusión en #42. |
| No functional changes. | Sin cambios funcionales (típico de refactor). |
| Reported by @ana in #77. | Reportado por @ana en #77. |

### 💥 BREAKING CHANGE

Un cambio que obliga a los usuarios de tu código a modificar el suyo. Se marca con `!` y/o en el pie.

```text
feat(api)!: rename /users endpoint to /accounts

BREAKING CHANGE: the /users endpoint has been removed.
Clients must use /accounts instead. The response format is the same.
Migration guide: docs/migrations/v3.md
```

| Forma | Ejemplo | Nota |
|---|---|---|
| `!` tras el tipo | `feat!: drop Python 3.8 support` | Visible en una línea |
| Pie `BREAKING CHANGE:` | `BREAKING CHANGE: config.yml renamed` | Explica qué hacer |
| Ambos | Lo más claro | Recomendado en librerías públicas |

⚠️ Cuidado: el pie se escribe exactamente `BREAKING CHANGE:` (mayúsculas, con dos puntos). Herramientas como semantic-release lo buscan literal.

### 🤝 Co-authored-by y otros pies

| Pie | Para qué | Ejemplo |
|---|---|---|
| `Co-authored-by:` | Dar crédito a quien programó contigo | `Co-authored-by: Ana Pérez <ana@mail.com>` |
| `Closes #N` | Cierra el issue al fusionar | `Closes #42` |
| `Fixes #N` | Igual que Closes (para bugs) | `Fixes #108` |
| `Refs #N` | Relaciona sin cerrar | `Refs #90` |
| `Reviewed-by:` | Quién revisó (kernel, proyectos grandes) | `Reviewed-by: Bob <bob@mail.com>` |
| `Signed-off-by:` | Certificado de origen (DCO) | Se añade con `git commit -s` |

```text
feat(ui): add keyboard shortcuts to editor

Pair-programmed during the hackathon.

Co-authored-by: Ana Pérez <ana.perez@example.com>
Co-authored-by: Luis Rojas <luis.rojas@example.com>
```

💡 Consejo: `Co-authored-by` va al final, tras una línea en blanco, y el email debe ser el que la persona usa en GitHub para que aparezca su avatar.

📌 Resumen: **tipo + imperativo + qué concreto** en la primera línea; **porqué** en el cuerpo; **issues, breaking changes y coautores** en el pie.

## 🌿 Ramas, tags, releases y changelog

Los nombres de ramas y versiones son inglés "comprimido": pocas palabras, en minúsculas y con guiones. Un buen nombre evita preguntas como "¿qué es la rama `prueba2`?".

### 🌱 Nombres de ramas

| Prefijo | Para | Ejemplo |
|---|---|---|
| `feature/` o `feat/` | Funcionalidad nueva | `feature/google-sign-in` |
| `fix/` o `bugfix/` | Arreglar un bug | `fix/cart-total-rounding` |
| `hotfix/` | Arreglo urgente en producción | `hotfix/payment-timeout` |
| `refactor/` | Reestructurar | `refactor/split-user-service` |
| `docs/` | Documentación | `docs/api-examples` |
| `chore/` | Mantenimiento | `chore/upgrade-deps` |
| `release/` | Preparar versión | `release/2.4.0` |
| `experiment/` o `spike/` | Probar una idea | `spike/vector-db-benchmark` |
| Con ticket | Enlaza a Jira/Linear | `feat/PROJ-123-export-csv` |

| ❌ Rama mala | ✅ Rama buena |
|---|---|
| `prueba2` | `spike/redis-cache` |
| `yafer` | `feat/user-avatar-upload` |
| `nueva-rama` | `fix/login-redirect-loop` |
| `Fix_Login_Bug` | `fix/login-bug` (minúsculas, guiones) |
| `feature/arreglando-login-y-registro` | `fix/login-validation` (y otra rama para registro) |

🇬🇧 Al hablar: "I'll **branch off** main" (crearé una rama desde main), "I **rebased** onto main" (rebasé sobre main), "Can you **merge** it?", "This branch is **behind** main" (está desactualizada), "I'll **squash** the commits" (juntaré los commits).

### 🔖 Tags y versionado semántico (SemVer)

Formato **MAJOR.MINOR.PATCH** (ej. `2.4.1`).

| Parte | Sube cuando | Ejemplo | Se dice |
|---|---|---|---|
| MAJOR | Rompes compatibilidad | 1.9.3 → **2**.0.0 | "major release" |
| MINOR | Añades funciones compatibles | 2.0.0 → 2.**1**.0 | "minor release" |
| PATCH | Arreglas bugs compatibles | 2.1.0 → 2.1.**1** | "patch release" |
| Pre-release | Versión de prueba | `3.0.0-beta.1` | "beta", "release candidate (rc)" |

| Término | Significa |
|---|---|
| release | publicación de una versión |
| tag | etiqueta de Git sobre un commit (`v2.4.1`) |
| release notes | notas de la versión para usuarios |
| changelog | historial de cambios de todas las versiones |
| stable / LTS | estable / soporte a largo plazo |
| rollback / roll back | volver a la versión anterior |
| cut a release | sacar/preparar una versión |
| pin a version | fijar una versión exacta |

🇬🇧 "We're **cutting a release** on Friday." / "Let's **roll back** to 2.3.0 until we fix it." / "Please **pin** the version to avoid surprises."

### 📜 Changelog (formato Keep a Changelog)

| Sección | Para | Ejemplo de línea |
|---|---|---|
| Added | Funciones nuevas | Dark mode toggle in settings |
| Changed | Cambios en funciones existentes | Default page size is now 50 |
| Deprecated | Se eliminará pronto | `/v1/users` endpoint (use `/v2/accounts`) |
| Removed | Eliminado | Support for Python 3.8 |
| Fixed | Bugs corregidos | Crash when uploading empty files |
| Security | Vulnerabilidades | Upgrade `requests` to patch a TLS issue |

```markdown
# Changelog

## [Unreleased]
### Added
- Export notes as PDF (#120)

## [2.4.0] - 2026-10-01
### Added
- Dark mode toggle in settings (#42)
- Keyboard shortcuts for the editor

### Changed
- Default page size is now 50 instead of 20

### Deprecated
- The `/v1/users` endpoint. Use `/v2/accounts` instead.

### Removed
- Support for Python 3.8

### Fixed
- Crash when uploading files larger than 10 MB (#88)
- Wrong timezone in exported reports

### Security
- Upgrade `requests` to 2.32 to fix a certificate validation issue
```

💡 Consejo: el changelog es **para humanos**, no copies el `git log`. Escribe desde el punto de vista del usuario: "Fixed crash when..." en vez de "refactor handler".

⚠️ Cuidado: en el changelog se usa **pasado o sustantivo** ("Fixed crash", "Support for..."), a diferencia del commit (imperativo). Es un registro histórico, no una orden.

## 🐛 Issues: reportar bugs y pedir funciones

Un issue mal escrito se queda meses sin respuesta; uno bueno se arregla en horas. El mantenedor no ve tu pantalla: tu texto debe permitirle **reproducir** el problema sin preguntarte nada.

### 🧩 Las 6 piezas de un buen bug report

| Pieza | En inglés | Pregunta que responde | ❌ Mal | ✅ Bien |
|---|---|---|---|---|
| Título | Title | ¿Qué falla y dónde? | "Bug!!" | "Crash when uploading files > 10 MB" |
| Pasos | Steps to reproduce | ¿Cómo lo provoco? | "Use the app" | "1. Go to /upload 2. Select a 15 MB file" |
| Esperado | Expected behavior | ¿Qué debería pasar? | (falta) | "The file is uploaded" |
| Real | Actual behavior | ¿Qué pasa en realidad? | "Doesn't work" | "500 error, blank page" |
| Entorno | Environment | ¿Dónde? | (falta) | "Arch Linux, Firefox 131, v2.3.1" |
| Evidencia | Logs / screenshots | ¿Qué prueba hay? | "Error" | Traza completa en bloque de código |

### 🐞 Plantilla completa: bug report

```markdown
## Bug report

**Title:** Crash when uploading files larger than 10 MB

### Description
When I upload a file larger than 10 MB, the server returns a 500 error
and the page goes blank. Smaller files work fine.

### Steps to reproduce
1. Go to `/upload`
2. Select any file larger than 10 MB (I used a 15 MB PDF)
3. Click "Upload"
4. See the error

### Expected behavior
The file should be uploaded, or a clear message like
"File too large (max 10 MB)" should be shown.

### Actual behavior
The server returns `500 Internal Server Error` and the page goes blank.
No error message is shown to the user.

### Environment
- OS: Arch Linux (kernel 6.11)
- Browser: Firefox 131
- App version: v2.3.1 (commit `a1b2c3d`)
- Python: 3.12.4

### Logs
    Traceback (most recent call last):
      File "app/upload.py", line 42, in save_file
        data = request.files["file"].read()
    MemoryError

### What I've tried
- Increasing `MAX_CONTENT_LENGTH` to 50 MB (same error)
- Uploading from Chrome (same error)

### Additional context
This started after upgrading to v2.3.0. It worked in v2.2.5.
I'm happy to submit a PR if you can point me in the right direction.
```

📌 Clave: la última línea ("I'm happy to submit a PR...") convierte tu queja en una **oferta de ayuda**. Los mantenedores aman eso.

### 🔁 Cómo escribir pasos para reproducir

| Regla | ❌ | ✅ |
|---|---|---|
| Numera cada acción | "I go to settings and change stuff and it breaks" | "1. Open Settings 2. Change language to Spanish 3. Click Save" |
| Una acción por paso | "Login and upload and save" | Tres pasos separados |
| Datos concretos | "a big file" | "a 15 MB PDF (attached)" |
| Desde un estado limpio | (asume tu config) | "With a fresh install / new account" |
| Frecuencia | (no dices) | "Happens every time" / "About 1 in 5 tries" |
| Último paso = el fallo | "...and then something" | "4. The app freezes" |

| Frase | Traducción |
|---|---|
| It happens every time. | Pasa siempre. |
| It happens intermittently. | Pasa a veces. |
| I can consistently reproduce it. | Lo reproduzco siempre. |
| I can't reproduce it on my machine. | No lo reproduzco en mi máquina. |
| This is a regression. | Esto antes funcionaba (regresión). |
| It works in v2.2 but fails in v2.3. | Funciona en 2.2, falla en 2.3. |
| Here is a minimal repro. | Aquí un ejemplo mínimo que lo reproduce. |
| Workaround: ... | Solución temporal: ... |

### 🎯 Expected vs actual behavior

Es la pieza más importante: sin "expected", el mantenedor no sabe si es un bug o es tu expectativa.

| Expected behavior | Actual behavior |
|---|---|
| The page should redirect to `/dashboard`. | The page stays on `/login` with no error. |
| The total should be 10.50. | The total shows 10.499999. |
| The API should return 404 for unknown IDs. | The API returns 500. |
| The model should load on GPU. | It silently falls back to CPU. |
| Dates should use the user's timezone. | All dates are in UTC. |

⚠️ Cuidado: "It doesn't work" es la frase más inútil del mundo open source. Siempre di **qué** no funciona y **cómo** lo sabes.

### ✨ Plantilla completa: feature request

```markdown
## Feature request

**Title:** Allow exporting notes as PDF

### Problem
I often need to share my notes with classmates who don't use the app.
Right now I have to copy the text manually, and I lose the formatting.

### Proposed solution
Add an "Export as PDF" button in the note menu.
The PDF should keep headings, lists and code blocks.

### Alternatives considered
- Export as Markdown: useful, but my classmates can't open .md files easily.
- Browser "Print to PDF": works, but includes the sidebar and buttons.

### Use cases
- Students sharing class notes
- Sending meeting notes to a client

### Additional context
Obsidian and Notion both support this. I could work on it if the idea is accepted.
```

| Sección | Para qué |
|---|---|
| Problem | El dolor real (no empieces por la solución) |
| Proposed solution | Tu idea concreta |
| Alternatives considered | Muestra que pensaste otras opciones |
| Use cases | Quién se beneficia |
| Additional context | Referencias, mockups, disposición a ayudar |

🇬🇧 Frases útiles: "**It would be great if** the app could...", "**Would you be open to** a PR that adds...?", "**Is this something you'd consider?**", "**I'd be happy to work on this.**"

### 🏷️ Etiquetas (labels) comunes

| Label | Significa |
|---|---|
| `bug` | Algo está roto |
| `enhancement` | Mejora / función nueva |
| `good first issue` | Ideal para empezar a contribuir |
| `help wanted` | Buscan ayuda externa |
| `needs repro` | Falta un ejemplo para reproducir |
| `needs triage` | Aún nadie lo clasificó |
| `duplicate` | Ya existe otro issue igual |
| `wontfix` | No se arreglará (decisión) |
| `invalid` | No es un problema real |
| `stale` | Sin actividad hace tiempo |
| `breaking` | Rompería compatibilidad |

💡 Consejo: antes de abrir un issue, **busca** (incluye issues cerrados). Si existe, no escribas "+1": reacciona con 👍 o aporta información nueva ("I can reproduce this on macOS too").

## 🔀 Pull requests

Un PR es un pequeño documento de venta: convences al revisor de que tu cambio es correcto, necesario y seguro. Un buen PR se revisa rápido; uno confuso se queda abierto semanas.

### 📋 Plantilla completa de PR

```markdown
## Summary
One or two sentences: what this PR does and why.

## Related issue
Closes #___

## Changes
- ...
- ...

## Why
The problem this solves, or the context behind the decision.

## How to test
1. ...
2. ...
3. Expected result: ...

## Screenshots / recordings
(before / after, if the UI changed)

## Checklist
- [ ] Tests added or updated
- [ ] Docs updated
- [ ] No breaking changes (or documented below)
- [ ] I ran the linter and the test suite locally

## Notes for reviewers
Anything you want feedback on, or parts you're unsure about.
```

### ✅ Ejemplo resuelto: PR realista

```markdown
Title: fix(auth): keep users logged in after token refresh

## Summary
Users were logged out every 15 minutes because the refresh token
was not saved after renewal. This PR stores the new refresh token
and retries the original request.

## Related issue
Closes #214

## Changes
- Save the new refresh token in `AuthStore` after `/token/refresh`
- Retry the failed request once after a successful refresh
- Add a mutex so parallel requests don't trigger multiple refreshes
- Add tests for expired, refreshed and invalid tokens

## Why
Support received 30+ complaints last week about random logouts.
The root cause was in `refreshSession()`: we discarded the new token.

## How to test
1. Set `ACCESS_TOKEN_TTL=60` in `.env` to make tokens expire in 1 minute
2. Log in and wait 2 minutes
3. Navigate to /profile
4. Expected: you stay logged in, and the network tab shows one refresh call

## Screenshots
N/A (no UI changes)

## Checklist
- [x] Tests added
- [x] Docs updated (`docs/auth.md`)
- [x] No breaking changes

## Notes for reviewers
I'm not 100% sure the mutex is the best approach.
If you know a cleaner pattern for this, I'm open to suggestions.
```

📌 Por qué funciona: el título usa Conventional Commits; el **Summary** cuenta el problema en lenguaje humano; **Why** da contexto de negocio ("30+ complaints"); **How to test** permite verificarlo en 2 minutos; **Notes** pide ayuda sobre la parte dudosa.

```flujo
dir: abajo
Rama -> Commits : pequeños
Commits -> Push
Push -> Abrir PR : plantilla completa
Abrir PR -> Review : PTAL
Review -> Cambios : comentarios
Cambios --> Review : otra vuelta
Review -> Merge : LGTM
```

### 📏 PR buenos vs malos

| ❌ PR malo | Riesgo | ✅ PR bueno |
|---|---|---|
| 3.000 líneas, 40 archivos | Nadie lo revisa de verdad | ≤ 400 líneas, una sola idea |
| Descripción vacía | El revisor adivina | Summary + Why + How to test |
| "Fixes stuff" | Sin contexto | Título en Conventional Commits |
| Mezcla refactor + feature | Difícil encontrar el cambio real | Un PR de refactor y otro de feature |
| Sin tests | Miedo a fusionar | Tests del caso feliz y bordes |
| Abierto sin avisar | Nadie lo ve | Pide review explícitamente |
| Cambios de formato en todo el archivo | Diff ilegible | Formatea en un PR aparte |

### 🙏 Cómo pedir review

| Situación | Frase | Más formal |
|---|---|---|
| Pedir revisión | Could you take a look at this PR? | Would you mind reviewing this PR when you have a moment? |
| Por chat | PTAL when you get a chance 🙏 | I'd appreciate your review when you have time. |
| Con urgencia real | This is blocking the release, could you review it today? | This is time-sensitive: would it be possible to review it today? |
| Parte concreta | I'd especially like feedback on `retry.py`. | I'd particularly value your input on the retry logic. |
| Aún no listo | Opening as a draft to get early feedback. | This is a draft; I'd welcome early feedback on the approach. |
| Recordar | Friendly ping on this PR 🙂 | Just following up on this PR. |
| Listo de nuevo | I've addressed all comments, ready for another look. | All feedback has been addressed; ready for re-review. |

### 💬 Responder a comentarios de review

| Situación | Frase |
|---|---|
| Aceptar | Good catch, fixed in `a1b2c3d`. |
| Aceptar y agradecer | Thanks, that's much cleaner. Done. |
| Ya lo hiciste | Done 👍 |
| Lo harás después | Good idea. I'll do it in a follow-up PR to keep this one small. |
| No entiendes | Could you clarify what you mean by...? |
| Discrepar con respeto | I see your point. I went with X because Y. What do you think? |
| Pedir opinión a otro | @maria, what's your take on this? |
| Propones alternativa | Would it work if we did X instead? |
| Necesitas tiempo | Let me look into this and get back to you. |
| Fue tu error | You're right, I missed that. Thanks for catching it! |
| Cerrar el hilo | Resolved. Thanks for the review! |

💡 Consejo: responde **cada** comentario (aunque sea "Done"). Así el revisor sabe que lo viste. Y marca el hilo como "Resolved" solo cuando lo arreglaste.

⚠️ Cuidado: no hagas `force push` sin avisar durante una review: el revisor pierde la referencia de qué cambió. Mejor commits nuevos ("address review comments") y squash al final.

## 🔍 Code review con tacto

En code review se juzga el **código**, no a la persona. Muchos latinos traducen literal desde el español y suenan bruscos ("Change this", "This is wrong"). En inglés profesional se suaviza con preguntas, "we" y "could".

### 🏷️ Prefijos de comentarios (Conventional Comments)

| Prefijo | Significa | ¿Bloquea? | Ejemplo |
|---|---|---|---|
| `nit:` | Detalle menor, de estilo | No | `nit: extra blank line here` |
| `suggestion:` | Propuesta de mejora | No | `suggestion: we could use a set for O(1) lookups` |
| `question:` | Duda real | No | `question: why do we need the sleep here?` |
| `issue:` | Problema concreto | Normalmente sí | `issue: this breaks when the list is empty` |
| `blocking:` | Debe cambiarse antes de fusionar | Sí | `blocking: this exposes the API key in logs` |
| `praise:` | Elogio sincero | No | `praise: really clean abstraction!` |
| `thought:` | Idea para el futuro | No | `thought: this could become a shared util later` |
| `todo:` | Tarea pequeña necesaria | Sí | `todo: add a test for this branch` |
| `chore:` | Tarea de proceso | A veces | `chore: please update the changelog` |
| `(non-blocking)` | Aclaración extra | No | `suggestion (non-blocking): rename to userCount` |
| `FYI:` | Información, sin pedir nada | No | `FYI: there's a helper for this in utils/date.py` |

### 😬 Suena brusco ❌ → suena profesional ✅

| ❌ Suena brusco | ✅ Suena profesional | Por qué funciona |
|---|---|---|
| This is wrong. | I think this might fail when `items` is empty. | Concreto y con "might" |
| Change this. | Could we change this to...? | Pregunta + "we" |
| Why did you do this? | What was the reasoning behind this approach? | Curiosidad, no acusación |
| This is bad code. | This part is a bit hard to follow. Could we split it? | Habla del efecto |
| You forgot the tests. | Could you add a test for this case? | Petición, no reproche |
| Use a dictionary. | Have you considered using a dict here? It'd make lookups O(1). | Sugiere y justifica |
| No. | I'm not sure this is the right approach because... | Razón explícita |
| Obviously this is slow. | This loop might be slow for large inputs (O(n²)). | Sin "obviously" |
| Just do X. | One option could be X. | Sin "just" (minimiza el esfuerzo) |
| You should know this. | Here's a link to our style guide on this. | Ayuda, no humilla |
| Fix it. | Could you take another look at this? | Respeta al autor |
| This makes no sense. | I'm having trouble understanding this part. Could you explain? | Asumes tu parte |
| Wrong name. | nit: maybe `userCount` would be clearer than `n`? | Prefijo + sugerencia |
| Did you even test this? | I ran it locally and got X. Am I missing a step? | Datos + humildad |

🇬🇧 Palabras suavizadoras: **could, might, maybe, perhaps, I think, I wonder if, what do you think?, consider, a bit, slightly**. Palabras peligrosas: **just, obviously, simply, clearly, always, never, you should**.

### 👍 Elogiar también es review

| Frase | Traducción |
|---|---|
| Nice! This is much cleaner. | ¡Bien! Mucho más limpio. |
| Great test coverage. | Muy buena cobertura de tests. |
| TIL, thanks for this! | ¡Hoy aprendí algo, gracias! |
| Love this refactor. | Me encanta este refactor. |
| Clever solution. | Solución ingeniosa. |
| LGTM 🚀 | Me parece bien, aprobado. |

### 🛡️ Cómo aceptar críticas sin sufrir

| Si sientes... | No escribas | Escribe |
|---|---|---|
| Que te atacan | "My code is fine." | "Thanks for the feedback. Could you help me understand the concern?" |
| Que no tienen razón | "You're wrong." | "I see it differently: X. Happy to change it if you still think Y is better." |
| Vergüenza por un bug | "Sorry sorry, I'm so bad." | "Good catch, thanks! Fixed." |
| Que son demasiados comentarios | (silencio) | "Thanks for the thorough review! I'll go through them one by one." |
| Que no entiendes el comentario | (cambias algo al azar) | "Could you give me an example of what you mean?" |
| Desacuerdo largo | (20 respuestas escritas) | "Maybe a quick call would be faster? I'm free at 3 pm." |

💡 Consejo: separa tu identidad de tu código. Un comentario sobre tu PR no dice que eres mal programador; es parte normal del proceso. Los seniors reciben comentarios **todos los días**.

⚠️ Cuidado: "Sorry" en exceso suena inseguro. Cambia "Sorry, I'm sorry, sorry for my bad code" por **"Thanks for catching that!"**. Agradecer > disculparse.

## ❓ Preguntar en Stack Overflow, GitHub Discussions y Discord

La gente ayuda gratis a quien **facilita** ayudar. Una pregunta bien hecha a menudo te lleva a la respuesta mientras la escribes (rubber duck debugging).

### 🏗️ Estructura de una buena pregunta

| Paso | Qué escribir | Frase modelo |
|---|---|---|
| 1. Título | Síntoma concreto + tecnología | "FastAPI returns 422 when sending JSON from fetch()" |
| 2. Contexto | Qué construyes, versiones | "I'm building a small API with FastAPI 0.115 and React 18." |
| 3. Objetivo | Qué esperabas | "I expected a 201 response with the new user." |
| 4. Problema | Qué pasa, error exacto | "Instead, I get 422 with `field required`." |
| 5. Código | MRE (ver abajo) | "Here is a minimal example:" |
| 6. Intentos | Qué probaste | "What I've tried: ..." |
| 7. Pregunta | Una pregunta clara | "Am I missing something in the request body?" |
| 8. Cierre | Agradecer | "Thanks in advance!" |

### 🔬 MRE: minimal reproducible example

| Propiedad | Significa | Cómo lograrlo |
|---|---|---|
| Minimal | Lo mínimo para ver el error | Borra todo lo que no influye |
| Complete | Se puede copiar y ejecutar | Incluye imports y datos de ejemplo |
| Reproducible | Muestra el mismo error | Pruébalo tú en un archivo limpio |
| Sin secretos | Nada de claves ni datos reales | Usa `API_KEY = "xxx"` y datos falsos |

```python
# MRE: 12 líneas en vez de tu proyecto entero
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str

@app.post("/users")
def create_user(user: User):
    return {"name": user.name}

# curl -X POST localhost:8000/users -d '{"name": "Ana"}'
# → 422: falta el header Content-Type: application/json
```

### ❌ Pregunta mala vs ✅ pregunta buena

```text
❌ MALA
Title: HELP!!! python not working urgent

hello sir, my code not work, i have error. please send me the code
for fix. i need for tomorrow. thanks

(captura de pantalla borrosa del error)
```

```text
✅ BUENA
Title: pandas read_csv raises UnicodeDecodeError on files from Excel

I'm reading a CSV exported from Excel (Windows) with pandas 2.2 on Linux.

    import pandas as pd
    df = pd.read_csv("ventas.csv")

I get:

    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1
    in position 128: invalid continuation byte

The file contains Spanish characters like "ñ" and "á".

What I've tried:
- encoding="utf-8" (same error)
- Opening the file in VS Code: the characters look fine

How can I find the right encoding, and what's the best way
to read this file? Thanks in advance!
```

| Error de la mala | Por qué molesta | Corrección |
|---|---|---|
| "HELP!!! urgent" | Presiona a voluntarios | Título descriptivo |
| "sir" | Asume género, suena raro | Sin saludo, ve al grano |
| "send me the code" | Pide que te hagan el trabajo | Pregunta qué está mal |
| Captura de pantalla | No se puede copiar ni buscar | Texto en bloque de código |
| Sin versión ni código | Imposible ayudar | MRE + versiones |

### 🎮 Discord y comunidades en vivo

| Hazlo ✅ | No lo hagas ❌ |
|---|---|
| Pregunta en el canal correcto (#help, #python) | Mandar DM a moderadores sin permiso |
| Usa hilos (threads) | Repetir la pregunta en 5 canales (cross-posting) |
| Pega el código en bloques de código (triple comilla) | Fotos del monitor con el celular |
| "Don't ask to ask, just ask" | "Can anyone help me?" y esperar |
| Di cuando lo resolviste y cómo | Desaparecer tras la respuesta |
| Agradece: "That worked, thanks!" | Exigir rapidez |

🇬🇧 Frases: "**Has anyone run into this before?**" (¿a alguien le pasó?), "**Any pointers would be appreciated.**" (cualquier pista se agradece), "**Solved it! The issue was...**" (lo resolví, el problema era...), "**Sorry if this is a dumb question**" (perdón si es tonta; úsala poco).

⚠️ Cuidado: "**Don't ask to ask**": en Discord, "Can I ask a question?" o "Anyone knows Python?" hace perder tiempo. Escribe la pregunta completa directamente.

💡 Consejo: cuando resuelvas un problema difícil, **responde tu propia pregunta** en Stack Overflow. Es bien visto y suma reputación (y practicas escribir inglés técnico).

## 💬 Chat de trabajo: Slack, Discord y Teams

En remoto, el chat **es** la oficina. La mayoría de los malentendidos en equipos distribuidos nacen de mensajes cortos y ambiguos. Escribe pensando que el otro está en otra zona horaria y leerá tu mensaje 8 horas después.

### 🔠 Abreviaturas de chat

| Sigla | Significa | Cuándo usarla | Registro |
|---|---|---|---|
| LGTM | Looks good to me | Aprobar un PR o propuesta | Neutro |
| PTAL | Please take a look | Pedir revisión | Neutro |
| WIP | Work in progress | Algo sin terminar (PR draft) | Neutro |
| TL;DR | Too long; didn't read | Resumen al inicio de un texto largo | Neutro |
| AFAIK | As far as I know | Dar info con cautela | Informal |
| IIRC | If I recall correctly | Info de memoria | Informal |
| IMO / IMHO | In my (humble) opinion | Opinar | Informal |
| FYI | For your information | Compartir sin pedir acción | Neutro (vale en email) |
| ETA | Estimated time of arrival | Preguntar/decir cuándo estará | Neutro |
| EOD | End of day | Plazo "hoy al final del día" | Neutro |
| EOW | End of week | Plazo "fin de semana laboral" | Neutro |
| COB | Close of business | Igual que EOD (más corporativo) | Formal |
| OOO | Out of office | Ausente (vacaciones, enfermo) | Neutro |
| PTO | Paid time off | Vacaciones pagadas | Neutro |
| AFK | Away from keyboard | Me alejo un rato | Informal |
| BRB | Be right back | Vuelvo enseguida | Informal |
| TBD | To be determined | Aún por decidir | Neutro |
| TBH | To be honest | Sinceramente | Informal |
| ACK | Acknowledged | Recibido, enterado | Neutro (técnico) |
| NVM | Never mind | Olvídalo, ya lo resolví | Informal |
| +1 | Estoy de acuerdo / me pasa igual | Apoyar algo | Informal |
| DM | Direct message | Mensaje privado | Neutro |
| ASAP | As soon as possible | Urgencia (úsala poco) | Neutro, puede sonar exigente |
| WFH | Working from home | Trabajo desde casa | Neutro |
| ICYMI | In case you missed it | Recordar algo publicado | Informal |
| QQ | Quick question | Pregunta rápida | Informal |
| LMK | Let me know | Avísame | Informal |
| WDYT | What do you think? | Pedir opinión | Informal |
| IDK | I don't know | No sé | Muy informal (evítala con jefes) |
| NP | No problem | De nada | Informal |
| TY / TYSM | Thank you (so much) | Gracias | Informal |
| SGTM | Sounds good to me | Aceptar un plan | Informal |
| EOM | End of message | Todo está en el asunto (email) | Neutro |
| 1:1 | One-on-one | Reunión a solas con tu manager | Neutro |
| RCA | Root cause analysis | Análisis de causa raíz | Formal / técnico |

⚠️ Cuidado: con clientes, managers nuevos o en emails formales **escribe las palabras completas**. "Pls fix ASAP thx" a un cliente suena grosero. Las siglas son para el equipo de confianza.

### 👋 "No hello": no mandes solo "hi"

Mandar "Hi" y esperar respuesta obliga al otro a parar, contestar y esperarte. En remoto, con zonas horarias, puede costar **un día entero**.

```text
❌
09:00  Yafer: Hi
09:00  Yafer: Are you there?
(Ana responde 3 horas después: "Hi! What's up?")
(Yafer ya está almorzando... Ana se va a dormir...)

✅
09:00  Yafer: Hi Ana! Quick question about the deploy script:
              should I run the migrations before or after
              restarting the API? I'm deploying v2.4 today at 3 pm.
(Ana responde cuando puede, con todo el contexto: "Before 👍")
```

📌 Traducción del bueno: "¡Hola Ana! Pregunta rápida sobre el script de deploy: ¿corro las migraciones antes o después de reiniciar la API? Despliego la v2.4 hoy a las 3 pm."

### 📨 Mensajes asíncronos efectivos

| Elemento | Por qué | Ejemplo |
|---|---|---|
| Saludo + pregunta en el mismo mensaje | No hacer esperar | "Hi Ana! Quick question: ..." |
| Contexto mínimo | El otro no está en tu cabeza | "I'm working on the CSV export (#120)." |
| Pregunta concreta | Respuesta rápida | "Should the dates be in UTC or local time?" |
| Lo que ya probaste | Evita respuestas obvias | "I checked the docs but couldn't find it." |
| Plazo o urgencia real | Ayuda a priorizar | "No rush, sometime this week is fine." |
| Opción por defecto | Desbloquea aunque no respondan | "If I don't hear back by Thursday, I'll go with UTC." |

```text
Hi team! 👋 TL;DR: the staging database will be down tomorrow
from 10:00 to 10:30 UTC for the Postgres upgrade.

What this means for you:
- Staging API will return 503 during that window
- Production is NOT affected

If you have a demo or tests scheduled then, let me know and
I can move the maintenance window. Thanks!
```

📌 Estructura: **TL;DR → qué significa para ti → qué hacer si te afecta**. Usa negritas o mayúsculas solo para lo crítico ("NOT affected").

### 🧵 Frases típicas de chat

| Situación | Frase | Variante más formal |
|---|---|---|
| Pregunta rápida | Quick question: ... | I have a quick question about ... |
| Avisar ausencia | Heads up: I'll be offline from 2 to 4 pm. | Just a heads-up that I'll be unavailable from 2 to 4 pm. |
| Seguir un hilo | Following up on this 👆 | Just following up on my previous message. |
| Leíste y lo harás | On it! | I'm working on it now. |
| Ya lo hiciste | Done ✅ | This has been completed. |
| Lo revisarás | I'll take a look. | I'll look into it and get back to you. |
| Agradecer | Thanks, that helps a lot! | Thank you, that's very helpful. |
| No entiendes | Sorry, not sure I follow. Could you elaborate? | Could you provide a bit more context? |
| Mover a privado | Let's move this to a DM / thread. | Let's continue this in a thread. |
| Pasar a llamada | Want to hop on a quick call? | Would a short call be easier? |
| Confirmar | Got it, thanks! | Understood, thank you. |
| Avisar que te equivocaste | My bad, I posted the wrong link. Here's the right one: ... | Apologies, I shared the wrong link. |
| Estás saturado | I'm swamped today; can it wait until tomorrow? | I have limited capacity today. Would tomorrow work? |
| Celebrar | Congrats on the launch! 🎉 | Congratulations on the release! |

### 😀 Reacciones con emoji (código no escrito)

| Emoji | Significado habitual |
|---|---|
| 👀 | Lo estoy mirando |
| ✅ | Hecho / resuelto |
| 👍 | Visto, de acuerdo |
| 🙏 | Gracias / por favor |
| 🎉 | Celebración |
| ➕ | Yo también / +1 |
| 🚀 | Desplegado / genial |
| 🔥 | Incidente (o algo excelente, según el contexto) |

💡 Consejo: reaccionar con 👀 cuando empiezas a revisar algo y ✅ cuando terminas es un hábito muy valorado en equipos remotos: nadie se queda preguntando "¿alguien vio esto?".

## 📧 Emails profesionales

El email sigue siendo el canal con clientes, reclutadores y empresas extranjeras. Un email claro transmite seriedad; uno largo y confuso hace que te ignoren.

### 🏗️ Estructura de un email

| Parte | Qué va | Ejemplo |
|---|---|---|
| Subject | Resumen + acción | "Request: access to staging server" |
| Greeting | Saludo según formalidad | "Hi Sarah," |
| Opening | Contexto en una línea | "I'm following up on yesterday's call." |
| Body | Una petición o idea principal | "Could you share the API docs?" |
| Call to action | Qué necesitas y cuándo | "Ideally by Thursday." |
| Closing | Despedida | "Best regards," |
| Signature | Nombre, rol, contacto | "Yafer Torrez · Backend Developer" |

### 👋 Saludos y despedidas por formalidad

| Formalidad | Saludo | Despedida | Cuándo |
|---|---|---|---|
| Muy formal | Dear Mr. Smith, / Dear Hiring Manager, | Sincerely, / Yours faithfully, | Primera carta, legal, aplicación formal |
| Formal | Dear Sarah, / Hello Sarah, | Kind regards, / Best regards, | Reclutadores, clientes nuevos |
| Neutro | Hi Sarah, | Best, / Thanks, | Clientes habituales, colegas |
| Informal | Hey Sarah! / Hi! | Cheers, / Thanks! | Equipo cercano |
| Grupo | Hi all, / Hi team, / Hello everyone, | Thanks, everyone! | Varios destinatarios |

⚠️ Cuidado: evita **"Dear Sir"** (asume género), **"Hello Mr. Sarah"** (Mr./Ms. van con apellido) y **"Greetings"** (suena a spam). Si no sabes el nombre: "Hi [Company] team," o "Dear Hiring Team,".

### 🙋 Frases para pedir algo

| Nivel | Frase |
|---|---|
| Directo (equipo) | Can you send me the logs? |
| Cortés | Could you send me the logs, please? |
| Más cortés | Would you mind sending me the logs? |
| Formal | I would appreciate it if you could send me the logs. |
| Muy formal | Would it be possible to share the logs at your earliest convenience? |
| Con plazo | Could you send them by Friday, if possible? |
| Con razón | I need them to finish the analysis before the release. |

### 🔁 Hacer seguimiento (follow-up)

| Situación | Frase |
|---|---|
| Primer recordatorio | Just following up on my email below. |
| Suave | I wanted to check in on this. |
| Con contexto | Following up on my message from last Tuesday about the invoice. |
| Reconociendo que están ocupados | I know you're busy, so I'll keep this short. |
| Segundo recordatorio | Bumping this to the top of your inbox. |
| Ofrecer alternativa | If now isn't a good time, I'm happy to revisit this next week. |
| Cerrar el bucle | Any update on this would be greatly appreciated. |

### ⏰ Disculparse por un retraso

| Nivel | Frase |
|---|---|
| Leve | Sorry for the late reply! |
| Profesional | Apologies for the delayed response. |
| Formal | Thank you for your patience. |
| Con causa | I was out of office last week, so I'm just catching up now. |
| Retraso de entrega | Unfortunately, the feature will be delayed by two days due to an issue with the payment API. |
| Con plan | Here's the new timeline: ... |

💡 Consejo: "**Thank you for your patience**" es mejor que "Sorry, sorry, sorry". Agradece la paciencia y da un **plan concreto**.

### 🚫 Rechazar con cortesía

| Situación | Frase |
|---|---|
| Rechazar tarea | Unfortunately, I won't be able to take this on this week. |
| Ofrecer alternativa | I can't do it by Friday, but I could have it ready by Tuesday. |
| Fuera de alcance | That's outside the scope of our current agreement, but I'd be happy to send a quote. |
| Rechazar oferta laboral | Thank you for the offer. After careful consideration, I've decided to pursue another opportunity. |
| Rechazar reunión | I'm not available at that time. Would Thursday at 10 am work instead? |
| Decir que no a una idea | I appreciate the suggestion, but I don't think it fits our current priorities. |

::: columnas
### ❌ Email flojo
- Subject: "Hi"
- "Hello sir, I need access urgent."
- Cinco preguntas en un párrafo
::: siguiente
### ✅ Email claro
- Subject: "Request: access to staging"
- Saludo con nombre y contexto en una línea
- Una petición y un plazo
:::

### ✅ Ejemplo 1: pedir acceso (cliente nuevo)

```text
Subject: Request: access to the staging environment

Hi Sarah,

I hope you're doing well. I'm starting work on the payment
integration this week, and I'll need access to the staging
environment to test it.

Could you please add my account (yafer.torrez@example.com)
to the staging project? Read-only access to the database
would also be helpful.

Ideally I'd like to start testing on Wednesday, so
anytime before then would be great.

Thanks in advance!

Best regards,
Yafer Torrez
Backend Developer
```

📌 Traducción breve: pide acceso al entorno de staging para la integración de pagos, da el email exacto, especifica el nivel de acceso y el plazo (miércoles). **Una petición, todo el contexto, plazo claro.**

### ✅ Ejemplo 2: avisar un retraso

```text
Subject: Update on the CSV export feature (new ETA: Tuesday)

Hi Mark,

I wanted to give you a quick update on the CSV export feature.

While testing with real data, I found that some files have
more than 1 million rows, which caused the server to run out
of memory. To fix this, I'm changing the export to stream the
data in chunks.

As a result, the feature will be ready on Tuesday instead of
Friday. The rest of the sprint is on track.

Please let me know if this affects any plans on your side.

Thank you for your patience,
Yafer
```

📌 Fórmula del mal aviso bien dado: **qué pasó → por qué → qué haces → nueva fecha → impacto**. Avisar **antes** de la fecha límite, nunca después.

### ✅ Ejemplo 3: seguimiento a un reclutador

```text
Subject: Following up: Backend Developer interview

Hi Emily,

Thank you again for taking the time to speak with me on Monday.
I really enjoyed learning about the team's work on the
recommendation engine.

I wanted to follow up and see if there are any updates on the
next steps. I'm still very interested in the role and happy
to provide any additional information.

Best regards,
Yafer Torrez
```

### ✅ Ejemplo 4: rechazar con cortesía un trabajo extra

```text
Subject: Re: Small change to the dashboard

Hi Mark,

Thanks for thinking of me for this. Unfortunately, I won't be
able to add the new charts this sprint without delaying the
CSV export, which we agreed is the priority.

Two options:
1. I add the charts next sprint (starting Oct 28).
2. We swap them for the export and move the export to next sprint.

Which one works better for you?

Best,
Yafer
```

💡 Consejo: dar **opciones numeradas** en lugar de un "no" seco convierte el rechazo en una decisión del cliente. Es la técnica más útil para controlar el scope creep.

⚠️ Cuidado: un email = **una petición principal**. Si mandas 5 preguntas en un párrafo, te responderán 2. Si son varias, numéralas.

## ☀️ Daily standup

La reunión diaria (10–15 min) donde cada uno responde: **qué hice ayer, qué haré hoy, qué me bloquea**. No es para resolver problemas, es para sincronizar. Habla 30–60 segundos.

### 🧱 Estructura

| Parte | Frase de inicio | Ejemplo |
|---|---|---|
| Yesterday | Yesterday I worked on / finished ... | Yesterday I finished the login page. |
| Today | Today I'm going to / I'll ... | Today I'll write tests for the auth service. |
| Blockers | I'm blocked by ... / No blockers. | I'm blocked by the missing API keys. |
| Extra (opcional) | Heads up: ... / I need ... | Heads up: I'll be out on Friday afternoon. |

### 🗣️ Cinco standups modelo

```text
1) Normal
Yesterday I finished the user registration form and opened a PR.
Today I'll address the review comments and start on password reset.
No blockers.

2) Con bloqueo
Yesterday I worked on the payment integration.
Today I'll keep working on it, but I'm blocked: I still don't have
the sandbox API keys. @Carlos, could you help me with that after the call?

3) Retrasado
Yesterday I kept debugging the memory leak in the worker.
It's taking longer than expected. I think it's related to the image cache.
Today I'll try profiling it with memray. If I can't find it by noon,
I'll ask for a second pair of eyes.

4) Proyecto de IA/ML
Yesterday I cleaned the dataset and removed about 2,000 duplicates.
Today I'm going to train the baseline model and log the metrics in W&B.
One question for later: should we use accuracy or F1 as the main metric?

5) Día de reuniones / poco avance
Yesterday was mostly meetings, so I didn't make much progress on the ticket.
Today I'll focus on finishing the API endpoint.
No blockers, but I might need help with the database schema tomorrow.
```

📌 Fíjate: el 2) **nombra a la persona** que puede desbloquearlo; el 3) **avisa antes** y pone un límite ("if I can't find it by noon"); el 4) deja preguntas largas "for later" para no alargar la reunión.

```secuencia
actores: Líder, Ana, Yafer
Líder -> Ana : ¿Ayer, hoy, bloqueos?
Ana --> Líder : Ayer terminé el login. Hoy, tests. Sin bloqueos.
Líder -> Yafer : ¿Y tú?
Yafer --> Líder : Sigo con pagos, bloqueado: faltan las API keys.
nota Líder : se resuelve después del standup
```

### 📋 Frases de standup

| Situación | Frase | Más formal |
|---|---|---|
| Trabajando | I'm working on the search feature. | I'm currently focused on the search feature. |
| Casi listo | I'm almost done with it; just need to add tests. | It's nearly complete; tests are pending. |
| Terminado | I wrapped up the migration. | I completed the migration. |
| Esperando | I'm waiting on the design team for the mockups. | I'm pending the mockups from design. |
| Atascado | I'm stuck on a weird CORS issue. | I've run into a CORS issue I haven't resolved yet. |
| Tarda más | It's taking longer than I expected. | It's turned out to be more complex than estimated. |
| Necesitas ayuda | Could someone pair with me on this? | I'd appreciate some support on this. |
| Pospones discusión | Let's discuss it after standup. | Let's take this offline. |
| Ausencia | I'll be OOO tomorrow. | I'll be out of office tomorrow. |
| Sin bloqueos | Nothing blocking me. | No blockers at the moment. |

⚠️ Cuidado: el error más común es dar una **lista de tareas sin resultado** ("I worked on things"). Di qué **terminaste** o qué **cambió**: "I fixed the bug in X" > "I was looking at X".

## 👥 Reuniones: planning, retro, demo y 1:1

Cada reunión tiene su vocabulario. Saber qué se espera de ti en cada una te permite participar en vez de solo escuchar.

### 🗓️ Tipos de reunión

| Reunión | Para qué | Qué se espera de ti | Frase típica |
|---|---|---|---|
| Daily standup | Sincronizar | Ayer, hoy, bloqueos | "No blockers." |
| Sprint planning | Elegir trabajo del sprint | Estimar y comprometerte | "I think that's about 3 points." |
| Backlog refinement / grooming | Aclarar y dividir tickets | Preguntar dudas | "What are the acceptance criteria?" |
| Sprint review / demo | Mostrar lo hecho | Demostrar tu trabajo | "Let me share my screen and walk you through it." |
| Retrospective | Mejorar el proceso | Qué fue bien, qué mejorar | "One thing that went well was..." |
| 1:1 (one-on-one) | Hablar con tu manager | Tus objetivos, problemas | "I'd like to get more experience with..." |
| Kickoff | Empezar proyecto | Entender objetivos | "What does success look like?" |
| Postmortem | Analizar un incidente | Hechos, sin culpar | "The root cause was..." |
| All-hands / town hall | Toda la empresa | Escuchar, preguntar | "I have a question about the roadmap." |

### 🧮 Sprint planning: estimar

| Situación | Frase | Más formal |
|---|---|---|
| Estimar | It'll take about two days. | I'd estimate roughly two days of work. |
| Rango | Somewhere between two and four days. | My estimate is two to four days, depending on X. |
| Con condición | Two days, assuming the API is ready. | That's contingent on the API being available. |
| Incertidumbre | Hard to say; I'd need to look at the code first. | I'd like to investigate before committing to an estimate. |
| Proponer spike | Can we do a time-boxed spike first? | I suggest a one-day spike to reduce uncertainty. |
| Es grande | This feels too big for one sprint. Can we split it? | We may want to break this into smaller stories. |
| Puntos | I'd say it's a 5. | I'd estimate it at 5 story points. |
| Capacidad | I only have about 60% capacity this sprint. | My availability is limited this sprint due to... |

💡 Consejo: añade **siempre** un supuesto a tu estimación ("assuming..."). Si el supuesto falla, tienes una razón clara y no parece que estimaste mal.

### 🔁 Retrospective

| Formato | Preguntas |
|---|---|
| Start / Stop / Continue | What should we start, stop and continue doing? |
| Went well / To improve / Actions | What went well? What could be improved? Action items? |
| Mad / Sad / Glad | What frustrated, disappointed or pleased us? |

| Situación | Frase |
|---|---|
| Algo bueno | One thing that went well was the pairing sessions. |
| Algo a mejorar | Something we could improve is how we hand off tickets. |
| Propuesta | I suggest we add a checklist to the PR template. |
| Crítica sin culpar | I noticed that requirements changed late a few times. |
| Acción concreta | Can we make that an action item? Who owns it? |
| Reconocer a alguien | Shout-out to Ana for helping me with the deploy. |

### 🖥️ Demo / sprint review

```text
Hi everyone! I'll quickly show the new CSV export.
Let me share my screen... Can you all see it?

So, here's the reports page. When I click "Export",
the file is generated in the background, and I get a
notification when it's ready. For large reports, this used
to time out; now it streams the data, so it works with
over a million rows.

That's it! Any questions or feedback?
```

| Frase | Traducción |
|---|---|
| Can you see my screen? | ¿Ven mi pantalla? |
| Let me walk you through it. | Les muestro paso a paso. |
| As you can see here, ... | Como ven aquí, ... |
| This is still a work in progress. | Aún está en progreso. |
| This used to ... ; now it ... | Antes ...; ahora ... |
| That's it from my side. | Eso es todo por mi parte. |
| Any questions or feedback? | ¿Preguntas o comentarios? |

### 🤝 1:1 con tu manager

| Objetivo | Frase |
|---|---|
| Pedir feedback | Is there anything I could be doing better? |
| Crecer | I'd like to take on more responsibility in the backend. |
| Aprender | Would it be possible to pair with a senior on system design? |
| Sobrecarga | I'm feeling a bit overloaded. Can we review my priorities? |
| Problema con alguien | I'd like your advice on a situation with a teammate. |
| Aumento | I'd like to discuss my compensation. Is now a good time? |

## 🗣️ Frases para hablar en reuniones

Lo difícil al hablar no es la gramática, es **tener la frase lista** en el momento. Memoriza 2–3 por situación.

### ✋ Interrumpir y tomar la palabra

| Situación | Frase | Más formal |
|---|---|---|
| Interrumpir | Sorry to interrupt, but ... | If I may add something ... |
| Pedir turno | Can I jump in here? | May I add a point? |
| Retomar | As I was saying, ... | To return to my earlier point, ... |
| Ceder | Go ahead. / Sorry, you first. | Please, go ahead. |
| Te interrumpen | Can I just finish my point? | If I could just finish this thought ... |
| Hablaron a la vez | Sorry, we talked over each other. Go ahead. | Apologies, please continue. |

### 🔁 Pedir que repitan o aclaren

| Situación | Frase | Más formal |
|---|---|---|
| No oíste | Sorry, could you repeat that? | I'm sorry, I didn't catch that. Could you repeat it? |
| Muy rápido | Could you slow down a bit, please? | Would you mind speaking a little more slowly? |
| Mala conexión | You're breaking up. Could you say that again? | The connection is unstable; could you repeat the last part? |
| Palabra desconocida | What do you mean by "X"? | Could you clarify what you mean by "X"? |
| Por escrito | Could you type that in the chat? | Would you mind sharing that in writing? |
| Ejemplo | Could you give me an example? | Could you illustrate that with an example? |

### ✅ Confirmar que entendiste

| Situación | Frase |
|---|---|
| Parafrasear | Just to make sure I understand: you want X, right? |
| Resumir | So, to sum up: I'll do X, and Ana will do Y. |
| Confirmar plazo | So the deadline is Friday EOD, correct? |
| Siguiente paso | What's the next step on my side? |
| Cerrar | Got it. I'll send a summary in Slack after the call. |

💡 Consejo: **envía un resumen escrito** después de cada reunión importante ("Quick recap of today's call: ..."). Protege de malentendidos por idioma y demuestra profesionalismo.

### 🙅 No estar de acuerdo con respeto

| Fuerza | Frase |
|---|---|
| Suave | I see your point, but I'm not sure that ... |
| Pregunta | Have we considered ...? |
| Alternativa | What if we tried X instead? |
| Datos | In my experience, X tends to cause Y. |
| Firme | I have some concerns about this approach. |
| Muy firme | I strongly disagree, because ... |
| Aceptar la decisión | I disagree, but I'm happy to go with the team's decision. (disagree and commit) |

### 💡 Proponer ideas

| Frase | Traducción |
|---|---|
| What if we ...? | ¿Y si ...? |
| How about ...? | ¿Qué tal si ...? |
| I'd suggest ... | Sugeriría ... |
| One option could be ... | Una opción podría ser ... |
| Would it make sense to ...? | ¿Tendría sentido ...? |
| I have an idea; bear with me. | Tengo una idea; denme un momento. |
| Pros and cons: ... | Ventajas y desventajas: ... |
| The trade-off is ... | El compromiso / costo es ... |

### 🤷 Decir "no sé" con elegancia

| ❌ Evita | ✅ Mejor | Qué comunica |
|---|---|---|
| I don't know. | I'm not sure, but I'll find out and get back to you. | Compromiso |
| No idea. | That's a good question. Let me check and follow up. | Seriedad |
| (silencio) | Let me think about that for a second. | Calma |
| (inventar) | I don't want to give you wrong information. I'll confirm. | Honestidad |
| I never used it. | I haven't worked with it yet, but it seems similar to X, which I know well. | Transferencia |
| It's not my area. | That's outside my area, but I think Ana would know. | Ayuda igual |

### ⏳ Ganar tiempo al hablar (fillers)

| Filler | Uso |
|---|---|
| Let me think ... | Pensar |
| That's a good question. | Ganar 3 segundos |
| How can I put it ... | Buscar palabras |
| What I mean is ... | Reformular |
| In other words, ... | Explicar de otro modo |
| The way I see it, ... | Dar opinión |
| Basically, ... | Simplificar (no abuses) |

⚠️ Cuidado: los falsos "fillers" del español traducidos ("eh", "este", "o sea", "¿no?") distraen mucho en inglés. Sustitúyelos por una **pausa** en silencio: suena más seguro.

### 🔚 Cerrar reuniones

| Frase | Traducción |
|---|---|
| I think we're out of time. | Creo que se acabó el tiempo. |
| Let's wrap up. | Cerremos. |
| Let's take this offline. | Lo vemos aparte. |
| Let's circle back to this next week. | Retomemos esto la próxima semana. |
| Action items: ... | Tareas acordadas: ... |
| I'll send a recap. | Enviaré un resumen. |
| Thanks, everyone! | ¡Gracias a todos! |

## 🏃 Agile, Scrum y Kanban en inglés

Casi todas las empresas extranjeras usan Agile. Si no conoces estas palabras, las reuniones parecen otro idioma aunque entiendas inglés.

### 📚 Vocabulario Agile

| Término | Significa | Ejemplo en frase |
|---|---|---|
| backlog | lista priorizada de trabajo pendiente | "Let's add it to the backlog." |
| sprint | periodo fijo (1–4 semanas) de trabajo | "We have two days left in the sprint." |
| sprint goal | objetivo principal del sprint | "The sprint goal is to launch payments." |
| user story | requisito desde la vista del usuario | "Can you write a user story for that?" |
| epic | historia grande que agrupa varias | "This epic covers the whole checkout." |
| story points | tamaño relativo de una tarea | "I'd give it 3 points." |
| acceptance criteria | condiciones para darla por buena | "What are the acceptance criteria?" |
| definition of done (DoD) | qué significa "terminado" para el equipo | "Tests are part of our DoD." |
| definition of ready | cuándo un ticket se puede empezar | "This ticket isn't ready yet." |
| velocity | puntos completados por sprint | "Our velocity is around 30 points." |
| burndown chart | gráfico de trabajo restante | "The burndown looks good." |
| capacity | horas disponibles del equipo | "We have less capacity due to holidays." |
| Product Owner (PO) | dueño del producto, prioriza | "Let's ask the PO." |
| Scrum Master | facilita el proceso | "The Scrum Master will run the retro." |
| stakeholder | interesado (cliente, jefe) | "We need to update the stakeholders." |
| ticket / issue / card | unidad de trabajo | "I'll create a ticket for it." |
| spike | investigación con tiempo limitado | "Let's do a spike on vector databases." |
| carry over | pasar al siguiente sprint | "This will carry over to next sprint." |
| scope | alcance | "That's out of scope." |
| blocker | algo que impide avanzar | "That's a blocker for the release." |
| WIP limit | máximo de tareas en curso (Kanban) | "We've hit our WIP limit." |
| lead time / cycle time | tiempo total / tiempo trabajando | "Our cycle time is about 3 days." |
| roadmap | plan a largo plazo | "Is it on the roadmap?" |
| MVP | producto mínimo viable | "Let's ship the MVP first." |

### 🃏 Columnas de un tablero Kanban

| Columna | Significa |
|---|---|
| Backlog | Pendiente, sin priorizar |
| To Do | Listo para empezar |
| In Progress | En curso |
| In Review / Code Review | Esperando revisión |
| QA / Testing | Probándose |
| Done | Terminado (según la DoD) |
| Blocked | Bloqueado |

### 📝 User story y acceptance criteria

Formato: **As a** [tipo de usuario], **I want** [algo], **so that** [beneficio].

```text
User story:
As a student, I want to export my notes as PDF,
so that I can share them with classmates who don't use the app.

Acceptance criteria:
- Given I'm viewing a note,
  when I click "Export as PDF",
  then a PDF file is downloaded.
- The PDF keeps headings, lists and code blocks.
- Notes longer than 50 pages show a progress indicator.
- If the export fails, a clear error message is shown.
```

| Parte | Traducción | Función |
|---|---|---|
| As a ... | Como ... | Quién |
| I want ... | Quiero ... | Qué |
| so that ... | para que ... | Por qué (el valor) |
| Given ... | Dado que ... | Estado inicial |
| When ... | Cuando ... | Acción |
| Then ... | Entonces ... | Resultado esperado |

⚠️ Cuidado: si el ticket no tiene acceptance criteria, **pregunta antes de empezar**: "What does done look like for this ticket?". Programar lo que "creías" que querían es el error más caro.

### 🎲 Story points (Fibonacci)

| Puntos | Sensación | Ejemplo |
|---|---|---|
| 1 | Trivial | Cambiar un texto |
| 2 | Pequeño | Añadir un campo a un formulario |
| 3 | Normal | Nuevo endpoint simple con tests |
| 5 | Mediano | Integrar una API externa |
| 8 | Grande | Nueva funcionalidad con varias partes |
| 13 | Muy grande | Probablemente hay que dividirla |
| ? | No se sabe | Necesita un spike |

📌 Los puntos miden **complejidad e incertidumbre**, no horas. "3 points" no significa "3 horas".

## 🗯️ Jerga hablada de la industria

Estas expresiones aparecen en reuniones, podcasts y Slack todos los días. Nadie te las explica: se asume que las sabes.

### 💬 Jerga general

| Jerga | Significa | Ejemplo |
|---|---|---|
| ship it | publícalo, está listo | "Tests pass. Ship it! 🚀" |
| bikeshedding | discutir detalles triviales | "We spent an hour bikeshedding the button color." |
| yak shaving | cadena de tareas antes de la real | "I wanted to fix a typo and ended up upgrading Node. Classic yak shaving." |
| rabbit hole | perderse investigando algo | "Don't go down that rabbit hole; it's not a priority." |
| low-hanging fruit | lo fácil con buen resultado | "Let's start with the low-hanging fruit." |
| tech debt | deuda técnica | "This shortcut will add tech debt." |
| footgun | algo fácil de usar mal | "Mutable default args are a footgun in Python." |
| happy path | caso normal sin errores | "It works on the happy path, but what about errors?" |
| edge case / corner case | caso límite | "Empty input is an edge case." |
| dogfooding | usar tu propio producto | "We're dogfooding the new editor internally." |
| bus factor | cuántos se van y el proyecto muere | "Our bus factor is one: only Ana knows the billing code." |
| hotfix | arreglo urgente en producción | "We need a hotfix for the login bug." |
| firefighting | apagar incendios constantes | "I spent the whole week firefighting." |
| scope creep | el alcance crece sin control | "Adding reports now is scope creep." |
| on call | de guardia para incidentes | "I'm on call this weekend." |
| postmortem | análisis tras un incidente | "We'll write a postmortem for the outage." |
| blameless | sin buscar culpables | "Our postmortems are blameless." |
| boilerplate | código repetitivo de plantilla | "The framework generates the boilerplate." |
| spaghetti code | código enredado | "This module is spaghetti code." |
| it works on my machine | funciona solo en mi PC | "It works on my machine" (y por eso existe Docker) |
| rubber duck debugging | explicar el código para hallar el bug | "I solved it by rubber-ducking it." |
| greenfield / brownfield | proyecto desde cero / sobre algo existente | "It's a greenfield project." |
| legacy code | código antiguo heredado | "We're migrating the legacy code." |
| sanity check | verificación rápida de cordura | "Can you sanity-check my query?" |
| second pair of eyes | otra persona que revise | "I need a second pair of eyes on this." |
| deep dive | análisis profundo | "Let's do a deep dive on performance." |
| move fast and break things | priorizar velocidad | "We're not in move-fast-and-break-things mode anymore." |
| bandwidth | capacidad/tiempo disponible | "I don't have the bandwidth this week." |
| ping someone | escribirle a alguien | "Ping me if you need help." |
| loop someone in | incluir en la conversación | "Let me loop in the designer." |
| heads-up | aviso previo | "Just a heads-up: the API will change." |
| ballpark (figure) | estimación aproximada | "Can you give me a ballpark?" |
| hand-wavy | vago, poco concreto | "That explanation is a bit hand-wavy." |
| nitpick | detalle menor | "Just a nitpick: rename this variable." |
| blast radius | alcance del daño si algo falla | "Use a feature flag to reduce the blast radius." |
| golden path / paved road | camino recomendado | "Use the golden path for new services." |
| flaky | que falla a veces sin razón | "That test is flaky." |
| gold-plating | añadir más de lo pedido | "Don't gold-plate it; ship the MVP." |
| 10x engineer | programador "10 veces mejor" (mito) | Úsalo con ironía |

### 🚒 Incidentes, on-call y postmortems

| Término | Significa |
|---|---|
| incident | incidente en producción |
| outage | caída del servicio |
| downtime / uptime | tiempo caído / en línea |
| degraded performance | funciona pero lento |
| SEV1 / SEV2 | severidad (1 = la peor) |
| page / get paged | alerta que despierta al de guardia |
| mitigate | reducir el impacto |
| root cause | causa raíz |
| rollback / roll forward | volver atrás / arreglar hacia adelante |
| post-incident review | revisión tras el incidente |
| action items | tareas para que no se repita |
| SLA / SLO | acuerdo / objetivo de nivel de servicio |

```text
#incident-payments
10:02  🔥 Ana: We're seeing 500s on /checkout. Investigating.
10:05  Yafer: ACK. I'm checking the logs. Looks related to the 9:50 deploy.
10:07  Ana: Rolling back to v2.3.1.
10:12  Ana: Rollback done. Error rate back to normal. ✅
10:15  Yafer: I'll start the postmortem doc. Root cause TBD.
```

📌 Así suena un incidente bien comunicado: **corto, con hora, con estado** (Investigating → Mitigating → Resolved) y sin culpar a nadie.

🇬🇧 Frase blameless: "**The deploy process allowed** an untested migration to reach production" en vez de "**Yafer broke** production". Se culpa al **proceso**, no a la persona.

## 🎤 Entrevistas técnicas: tipos y preparación

Una entrevista en inglés evalúa tres cosas a la vez: si sabes programar, si **sabes explicar lo que piensas** y si serías fácil de tener en el equipo. El inglés perfecto no es requisito; la **claridad** sí.

### 🗂️ Tipos de entrevista

| Tipo | Duración | Qué evalúan | Cómo prepararte |
|---|---|---|---|
| Recruiter screening | 15–30 min | Inglés, interés, salario, disponibilidad | "Tell me about yourself" + tu rango salarial |
| Technical screening | 45–60 min | Fundamentos, preguntas rápidas | Repasa estructuras de datos y tu stack |
| Live coding | 45–60 min | Resolver un problema hablando | LeetCode Easy/Medium en voz alta |
| Take-home assignment | 2–8 h | Código real, calidad, README | Tests, README claro, commits limpios |
| System design | 45–60 min | Diseñar sistemas grandes | Escalabilidad, caché, colas, bases de datos |
| Behavioral | 30–60 min | Trabajo en equipo, conflictos | 5–6 historias STAR preparadas |
| Pair programming | 60 min | Colaboración real | Pregunta, escucha, acepta sugerencias |
| Hiring manager / culture fit | 30–45 min | Motivación, encaje | Investiga la empresa, prepara preguntas |
| Final / onsite loop | 3–5 h | Todo lo anterior junto | Descansa; lleva agua y notas |

### 🧩 El proceso típico (pipeline)

| Etapa | En inglés | Qué pasa |
|---|---|---|
| 1 | Application | Mandas CV (resume) y a veces cover letter |
| 2 | Recruiter call / phone screen | Charla corta con RR. HH. |
| 3 | Technical interview(s) | Coding, take-home o system design |
| 4 | Behavioral / team interview | Conocer al equipo |
| 5 | Reference check | Llaman a tus referencias |
| 6 | Offer | Oferta formal (offer letter) |
| 7 | Negotiation | Negocias salario y condiciones |
| 8 | Onboarding | Primeras semanas |

```flujo
Application -> Recruiter call -> Technical -> Team interview -> Offer -> Onboarding
Technical --> Application : rejected
```

🇬🇧 Vocabulario: "**I'm moving forward** in the process" (avanzo), "**They rejected me** / **I didn't get the offer**", "**I got ghosted**" (no respondieron más), "**next steps**" (siguientes pasos), "**hiring freeze**" (congelación de contrataciones).

## 🙂 "Tell me about yourself" y método STAR

Son las dos preguntas que **seguro** te harán. Prepáralas por escrito, grábalas en voz alta y ensáyalas hasta que suenen naturales (no recitadas).

### 🧱 Estructura: presente → pasado → futuro

| Parte | Qué decir | Duración |
|---|---|---|
| Present | Quién eres hoy, qué estudias/haces | 20 s |
| Past | 1–2 proyectos o logros concretos | 40 s |
| Future | Qué buscas y por qué esta empresa | 20 s |

### 🎓 Respuesta modelo para estudiante

```text
Hi, I'm Yafer. I'm a Computer Science student from Bolivia,
and I'm especially interested in AI and backend development.

Over the last two years I've built several projects on my own.
For example, I built a tool that records my online classes,
transcribes them with Whisper on the GPU, and turns them into
study notes automatically. That project taught me a lot about
Python, audio processing and working with large models locally.

I use Linux every day, I automate most of my workflow with
scripts, and I'm comfortable with Git, SQL and JavaScript.

Right now I'm looking for a remote internship or junior role
where I can contribute to real AI or backend products and
learn from experienced engineers. That's why I was excited
to see this position: your team works on exactly that.
```

📌 Por qué funciona: dice **de dónde eres** (zona horaria implícita), da **un proyecto concreto** con tecnologías, muestra **autonomía** y conecta con **esta empresa**. Dura ~1 min 15 s.

| ❌ Error | ✅ Mejor |
|---|---|
| Contar tu vida desde el colegio | Empezar por el presente profesional |
| Repetir el CV línea por línea | Elegir 1–2 historias |
| "I'm a hard worker and responsible" | Demostrarlo con un ejemplo |
| Hablar 5 minutos | 60–90 segundos |
| Terminar con "...and that's it" | Terminar conectando con el puesto |

### ⭐ Método STAR

| Letra | En inglés | Qué cuentas | % del tiempo |
|---|---|---|---|
| S | Situation | Contexto breve | 10 % |
| T | Task | Tu responsabilidad | 10 % |
| A | Action | Lo que **tú** hiciste (usa "I") | 60 % |
| R | Result | Resultado medible + qué aprendiste | 20 % |

⚠️ Cuidado: los latinos solemos decir "**we** did..." por modestia. En entrevistas en EE. UU. eso oculta tu aporte. Usa "**I** designed...", "**I** proposed..." y luego reconoce al equipo.

### ✅ STAR 1: "Tell me about a challenging technical problem"

```text
Situation: In my transcription project, processing a two-hour class
took almost 40 minutes, which made the tool almost useless.

Task: I wanted to make it fast enough to have the notes ready
right after class.

Action: First, I profiled the pipeline and found that the model
was running on the CPU. I configured it to use the GPU with CUDA,
switched to a smaller Whisper model with similar accuracy for
Spanish, and split the audio into chunks processed in parallel.

Result: Processing time went from 40 minutes to about 4 minutes,
a 10x improvement. I also learned to always measure before
optimizing, instead of guessing.
```

### ✅ STAR 2: "Tell me about a time you disagreed with a teammate"

```text
Situation: In a university group project, a teammate wanted to
store all the data in a single JSON file to save time.

Task: I was responsible for the backend, and I was worried it
wouldn't scale when several users edited data at the same time.

Action: Instead of just saying no, I built a small test that
simulated ten users writing at once, and showed the team that the
file got corrupted. Then I proposed SQLite as a simple middle ground:
almost as easy to set up, but safe for concurrent writes.

Result: The team agreed, and we finished on time without data loss.
My teammate later said the test convinced him more than any argument.
I learned that data is more persuasive than opinions.
```

### ✅ STAR 3: "Tell me about a mistake you made"

```text
Situation: While working on a script that synced my config files
between two computers, I ran it without a dry run.

Task: It was supposed to copy only new files.

Action: Because of a wrong path, it overwrote several files on the
second machine. I stopped the script, restored the files from a
backup, and then added a --dry-run option, a confirmation prompt
and automatic backups before every sync.

Result: I didn't lose any important work, and the tool has been
safe since then. Now I always test destructive operations with a
dry run first, and I apply the same habit at work.
```

📌 La pregunta del error es una trampa positiva: quieren ver que **reconoces**, **arreglas** y **previenes**. Nunca digas "I've never made a mistake".

### 🗃️ Historias que debes tener listas

| Pregunta | Prepara una historia de |
|---|---|
| Tell me about a challenging project. | Un problema técnico difícil |
| Tell me about a time you failed. | Un error y lo que cambiaste |
| Tell me about a conflict with a teammate. | Un desacuerdo resuelto con datos |
| Tell me about a time you learned something quickly. | Aprender una tecnología nueva |
| Tell me about a time you went above and beyond. | Algo extra que hiciste |
| Tell me about a time you had a tight deadline. | Priorizar bajo presión |
| Describe a time you received critical feedback. | Aceptar y mejorar |

💡 Consejo: una misma historia puede servir para 2–3 preguntas cambiando el enfoque. Con **5 buenas historias** cubres casi cualquier entrevista conductual.

## 🧠 Live coding y system design en voz alta

En live coding valoran **cómo piensas** tanto como el resultado. El silencio es tu enemigo: el entrevistador no puede ayudarte ni darte puntos si no sabe qué piensas.

### 🗣️ Frases por fase

| Fase | Qué haces | Frase |
|---|---|---|
| 1. Aclarar | Repetir el problema | "Let me make sure I understand: I need to return the indices of two numbers that add up to the target, right?" |
| 1. Aclarar | Preguntar restricciones | "Can I assume the input fits in memory?" / "Are there duplicate values?" |
| 1. Aclarar | Casos borde | "What should I return if there's no solution?" |
| 2. Ejemplo | Probar a mano | "Let me try a small example: [2, 7, 11] with target 9." |
| 3. Proponer | Fuerza bruta | "The brute-force approach is to check every pair, which is O(n²)." |
| 3. Proponer | Mejora | "We can do better with a hash map, trading space for time." |
| 3. Proponer | Pedir permiso | "Does this approach sound good before I start coding?" |
| 4. Codificar | Narrar | "I'll iterate through the array and, for each number, compute the complement." |
| 4. Codificar | Simplificar | "I'll write a helper function for this to keep it clean." |
| 4. Codificar | Duda de sintaxis | "I don't remember the exact method name; I'll assume it's `sorted()`." |
| 5. Analizar | Big O tiempo | "The time complexity is O(n) because we visit each element once." |
| 5. Analizar | Big O espacio | "The space complexity is O(n) for the hash map." |
| 6. Probar | Recorrer | "Let me walk through the code with the example." |
| 6. Probar | Bordes | "Let me check the edge cases: empty array, one element, negative numbers." |
| 6. Probar | Encontrar bug | "Oh, I see a bug here: I should check before inserting. Let me fix that." |
| 7. Optimizar | Mejoras | "If the array were sorted, we could use two pointers and O(1) space." |
| 7. Optimizar | Trade-off | "The trade-off is readability versus memory usage." |

### 🔤 Cómo se lee la notación Big O

| Notación | Se dice | Ejemplo |
|---|---|---|
| O(1) | "O of one" / "constant time" | Acceso a un dict |
| O(log n) | "O of log n" / "logarithmic" | Búsqueda binaria |
| O(n) | "O of n" / "linear" | Recorrer una lista |
| O(n log n) | "O of n log n" | Ordenar (merge sort) |
| O(n²) | "O of n squared" / "quadratic" | Dos bucles anidados |
| O(2ⁿ) | "O of two to the n" / "exponential" | Subconjuntos |

### 🆘 Cuando te atascas

| Situación | Frase |
|---|---|
| Necesitas pensar | "Let me think about this for a moment." |
| Pedir pista | "Could you give me a small hint?" |
| Cambiar de plan | "This approach is getting complicated. Let me step back." |
| Reconocer límite | "I'm not sure how to optimize this further, but here's what I'd explore." |
| Se acaba el tiempo | "Given the time, I'll write the brute force first and then optimize." |
| No conoces algo | "I haven't used that before, but I'd approach it like this..." |

💡 Consejo: pedir una pista **no** te descalifica. Quedarte 10 minutos callado, sí. Los entrevistadores esperan que preguntes.

### 🏗️ System design: frases y estructura

| Paso | Qué haces | Frase |
|---|---|---|
| 1. Requisitos | Funcionales y no funcionales | "What are the main features? How many users do we expect?" |
| 2. Estimar | Tráfico y datos | "Let's assume 10 million daily users and 100 requests per second." |
| 3. API | Endpoints principales | "We'd need a POST /urls endpoint and a GET /{code} endpoint." |
| 4. Alto nivel | Dibujar componentes | "At a high level, we have a load balancer, API servers and a database." |
| 5. Datos | Elegir base de datos | "Since reads are much more frequent than writes, I'd add a cache." |
| 6. Profundizar | Cuellos de botella | "The bottleneck here would be the database writes." |
| 7. Escalar | Soluciones | "We could shard the database by user ID." |
| 8. Trade-offs | Justificar | "I'm choosing availability over consistency here because..." |

| Vocabulario | Significa |
|---|---|
| scalability | capacidad de crecer |
| load balancer | balanceador de carga |
| bottleneck | cuello de botella |
| throughput / latency | rendimiento / latencia |
| sharding / replication | partir / copiar la base de datos |
| cache hit / miss | acierto / fallo de caché |
| single point of failure | punto único de fallo |
| eventual consistency | consistencia eventual |
| horizontal / vertical scaling | más máquinas / máquina más potente |
| message queue | cola de mensajes |
| rate limiting | limitar peticiones |

## ❓ Preguntas de entrevista con respuestas modelo

Aquí están las preguntas que más se repiten. No memorices palabra por palabra: entiende la **estructura** y adáptala a tu historia.

### 🧑‍💼 Preguntas conductuales y de motivación

| Pregunta | Qué buscan | Respuesta modelo (resumen) |
|---|---|---|
| Why do you want to work here? | Que investigaste | "I've been following your work on X, and I like that your team uses Y. I want to grow in exactly that area." |
| Why should we hire you? | Valor concreto | "I learn fast, I already work with your stack daily, and I've shipped projects end to end on my own." |
| What's your biggest strength? | Autoconocimiento | "Debugging. I enjoy finding root causes, like when I reduced my pipeline time 10x by profiling it." |
| What's your biggest weakness? | Honestidad + mejora | "I used to spend too long trying alone before asking for help. Now I give myself a 30-minute limit." |
| Where do you see yourself in five years? | Ambición realista | "Working as a solid mid-level engineer in ML systems, mentoring juniors." |
| Why are you leaving your job? | Sin quejas | "I'm looking for more challenging problems and an international team." |
| How do you handle pressure? | Organización | "I break the work into small tasks, communicate early, and focus on the highest priority first." |
| How do you keep learning? | Curiosidad | "I read docs and release notes, build side projects, and follow engineering blogs." |
| What are your salary expectations? | Rango | "Based on my research for this role, I'm looking for a range of X to Y USD per month." |
| When can you start? | Disponibilidad | "I can start in two weeks." |

### 🧑‍💻 Preguntas técnicas frecuentes (para junior)

| Pregunta | Idea clave para responder |
|---|---|
| What's the difference between a list and a tuple in Python? | Mutable vs inmutable; tuplas como claves de dict |
| What happens when you type a URL in the browser? | DNS → TCP/TLS → HTTP request → server → response → render |
| Explain REST. | Recursos, verbos HTTP, sin estado (stateless) |
| SQL vs NoSQL? | Esquema y relaciones vs flexibilidad y escala horizontal |
| What is an index in a database? | Estructura (B-tree) que acelera búsquedas a costa de escrituras |
| Explain overfitting. | Memoriza el entrenamiento, generaliza mal; regularización, más datos, validación |
| What is a race condition? | Dos hilos acceden a lo mismo y el resultado depende del orden |
| Process vs thread? | Memoria separada vs compartida |
| What is Big O? | Cómo crece el costo con el tamaño de la entrada |
| How does Git merge differ from rebase? | Merge conserva historia con commit de unión; rebase reescribe en línea |
| What is a REST API status code 401 vs 403? | 401 no autenticado; 403 autenticado pero sin permiso |
| What's the difference between precision and recall? | Falsos positivos vs falsos negativos |

🇬🇧 Plantilla para explicar un concepto: "**In simple terms,** X is... **For example,** ... **The main advantage is** ..., **but the trade-off is** ..."

### 🙋 Preguntas para hacerle a la empresa

| Tema | Pregunta |
|---|---|
| Día a día | What does a typical day look like for this role? |
| Equipo | How big is the team, and how is it structured? |
| Stack | What does your tech stack look like? |
| Proceso | How do you handle code reviews and deployments? |
| Crecimiento | How do you support the growth of junior developers? |
| Éxito | What would success look like in the first 90 days? |
| Retos | What's the biggest challenge the team is facing right now? |
| Remoto | How do you collaborate across time zones? |
| Cultura | How does the team handle disagreements on technical decisions? |
| Siguientes pasos | What are the next steps in the process? |

⚠️ Cuidado: decir "**No, I don't have any questions**" da la impresión de poco interés. Lleva siempre **2–3 preguntas** preparadas. No preguntes por vacaciones o salario en la primera entrevista técnica (eso va con el recruiter).

### 🇧🇴 Errores frecuentes de candidatos latinos

| Error | Por qué perjudica | Cómo evitarlo |
|---|---|---|
| Disculparse por el inglés al inicio ("Sorry for my bad English") | Te posiciona como débil antes de empezar | Habla y ya; si no entiendes, pide que repitan |
| Usar "we" para todo | No se ve tu aporte | "I built / I proposed / I led" |
| Respuestas demasiado largas | Pierden el hilo | Responde en 1–2 min y pregunta "Would you like more detail?" |
| Quedarse callado en live coding | No pueden evaluarte | Narra todo lo que piensas |
| Traducir literal ("I have 22 years", "I have a doubt") | Suena raro | "I'm 22", "I have a question" |
| Pedir un salario demasiado bajo | Pareces inexperto y te pagan menos | Investiga rangos para remoto LATAM |
| No preparar el entorno | Mala impresión técnica | Prueba cámara, micro, internet y luz antes |
| No confirmar la zona horaria | Llegas tarde o temprano | "Is that 10 am Eastern Time?" |
| Ser demasiado formal ("Dear sir, I am honored...") | Distancia en startups | Tono amable y directo |
| No hacer preguntas | Parece desinterés | 2–3 preguntas preparadas |
| No hacer seguimiento | Te olvidan | Email de agradecimiento en 24 h |
| Decir "yes" sin entender | Respuestas equivocadas | "Just to clarify, do you mean...?" |

💡 Consejo: antes de cada entrevista, ten en una nota: tu "tell me about yourself", 5 historias STAR, tu rango salarial, 3 preguntas y la hora en **tu** zona (Bolivia es UTC−4, sin horario de verano).

## 🌎 Trabajo remoto para empresas extranjeras

Trabajar para afuera desde Bolivia es realista, pero hay un vocabulario de contratos y pagos que, si no entiendes, te puede costar dinero. Lee **todo** antes de firmar.

### 📄 Vocabulario de contrato

| Término | Significa | Ojo con |
|---|---|---|
| employee | empleado en planilla | Raro desde el extranjero; suele ir por un EOR |
| contractor / independent contractor | trabajador independiente | Tú pagas tus impuestos y no tienes beneficios |
| freelancer | por proyecto, varios clientes | Ingreso variable |
| EOR (Employer of Record) | empresa que te contrata en nombre de otra (Deel, Remote.com) | Revisa qué beneficios incluye |
| full-time / part-time | jornada completa / parcial | Cuántas horas exactamente |
| contract-to-hire | contrato temporal con opción a planta | Plazo de evaluación |
| probation period | periodo de prueba | Pueden despedirte con poco aviso |
| notice period | preaviso para renunciar o despedir | "Two weeks' notice" es lo común en EE. UU. |
| NDA | acuerdo de confidencialidad | No publiques código del cliente |
| non-compete | prohibición de trabajar con la competencia | Lee el plazo y el alcance |
| IP assignment | el código que haces es de la empresa | ¿Incluye tus proyectos personales? |
| scope of work (SOW) | qué tareas exactas incluye | Lo que no está, se cobra aparte |
| deliverables | entregables | Fechas y criterios de aceptación |
| termination | rescisión del contrato | Causas y aviso |
| at-will employment | se puede terminar en cualquier momento (EE. UU.) | Sin indemnización |

### 💵 Vocabulario de pago

| Término | Significa | Ejemplo |
|---|---|---|
| rate | tarifa | "My rate is 25 USD per hour." |
| hourly / monthly / fixed price | por hora / mensual / precio cerrado | "It's a fixed-price project." |
| invoice | factura que tú envías | "I'll send the invoice on the 1st." |
| billable hours | horas cobrables | "I logged 160 billable hours." |
| net 15 / net 30 | pagan 15 / 30 días después de la factura | "Payment terms are net 30." |
| gross / net | bruto / neto | "Is that gross or net?" |
| wire transfer | transferencia bancaria internacional | Comisiones del banco intermediario |
| payment platform | Deel, Payoneer, Wise, etc. | Verifica disponibilidad en Bolivia |
| overtime | horas extra | ¿Se pagan? ¿a qué tarifa? |
| raise | aumento | "I'd like to discuss a raise." |
| bonus / equity / stock options | bono / participación / opciones | Las opciones pueden valer 0 |
| W-8BEN | formulario de EE. UU. para no residentes | Lo piden a contractors extranjeros |

### 🕐 Vocabulario de horario y ausencias

| Término | Significa |
|---|---|
| timezone overlap | horas en que coinciden ambas zonas |
| core hours | horas en que todos deben estar disponibles |
| async-first | se prioriza la comunicación escrita |
| PTO (paid time off) | días libres pagados |
| sick leave | baja por enfermedad |
| public holidays | feriados (¿los tuyos o los suyos?) |
| flexible hours | horario flexible |
| on-call rotation | guardias rotativas |

| Zona | Diferencia con Bolivia (UTC−4), verano / invierno de ellos | Overlap típico |
|---|---|---|
| US Eastern (New York) | 0 h (su verano) / −1 h (su invierno) | Casi total |
| US Pacific (San Francisco) | −3 / −4 h | Su mañana = tu mediodía |
| Europe (Madrid, Berlín) | +6 / +5 h | Tu mañana = su tarde |
| UK (Londres) | +5 / +4 h | Tu mañana |

🇬🇧 "What are the **core hours**?", "How much **timezone overlap** do you need?", "I'm in **GMT−4**; I can overlap with **Eastern Time** almost entirely."

### 🤝 Negociar salario con frases

| Momento | Frase |
|---|---|
| Te preguntan expectativas | "Based on my research for similar remote roles, I'm looking for 2,500 to 3,000 USD per month." |
| Devolver la pregunta | "I'd love to hear the budgeted range for this role first." |
| Recibes la oferta | "Thank you so much! I'm very excited about the role. Could I have a couple of days to review it?" |
| Pedir más | "Is there any flexibility on the base salary? I was hoping for something closer to X." |
| Justificar | "Given my experience with X and Y, which are core to this role, I think X is fair." |
| Si no suben el salario | "If the base is fixed, could we discuss a signing bonus, more PTO, or a review in six months?" |
| Pedirlo por escrito | "Could you send me the offer in writing?" |
| Aceptar | "I'm happy to accept the offer. Looking forward to starting!" |

⚠️ Cuidado: nunca digas **la primera cifra demasiado baja** "para asegurar el trabajo". En remoto, las empresas tienen un presupuesto; si pides poco, te dan poco y además pareces junior. Investiga en Glassdoor, Levels.fyi o pregunta en comunidades.

💡 Consejo: como contractor, pide **más** que como empleado: tú pagas impuestos, equipo, internet, salud y no tienes vacaciones pagadas (salvo que se negocien). Algunos freelancers usan un recargo de +20–40 % (orientativo).

### 🚩 Señales de alerta (red flags)

| Red flag | Por qué es peligroso |
|---|---|
| Te piden pagar algo para empezar | Estafa clásica |
| Sin contrato escrito | No puedes reclamar nada |
| "Unpaid trial" de semanas | Trabajo gratis |
| Te piden datos bancarios por chat antes de firmar | Riesgo de fraude |
| Pagos "en cuanto el cliente nos pague" | Te usan como financiamiento |
| Prisa extrema para firmar | Presión para que no leas |
| Te piden instalar software o enviar documentos por Telegram/WhatsApp | Posible phishing |

## 💼 CV y LinkedIn en inglés

En el extranjero el CV (allá "**resume**") es corto: **1 página** para estudiantes y juniors, sin foto, sin edad, sin estado civil. Cada línea debe mostrar **un logro**, no una tarea.

### 🧱 Estructura del resume

| Sección | Qué va |
|---|---|
| Header | Nombre, ciudad/país, email, GitHub, LinkedIn (sin foto) |
| Summary (opcional) | 2 líneas: quién eres y qué buscas |
| Experience | Trabajos, pasantías, freelance (lo más reciente primero) |
| Projects | Proyectos personales con impacto (clave para estudiantes) |
| Education | Universidad, carrera, fecha esperada de graduación |
| Skills | Lenguajes, frameworks, herramientas |
| Languages | Spanish (native), English (B2 / professional working proficiency) |

### 🏆 Fórmula de un bullet de logro

**Verbo de acción + qué hiciste + con qué + resultado medible.** (Fórmula XYZ de Google: "Accomplished X, as measured by Y, by doing Z".)

| ❌ Tarea | ✅ Logro |
|---|---|
| Responsible for the backend. | Built a REST API with FastAPI serving 2,000 daily requests. |
| Worked on the database. | Reduced query time by 60% by adding indexes and rewriting 3 slow queries. |
| Helped with testing. | Increased test coverage from 40% to 85% using pytest. |
| Made a transcription tool. | Built a GPU-accelerated transcription tool with Whisper, cutting processing time 10x. |
| I did the deployment. | Automated deployments with GitHub Actions, reducing release time from 1 hour to 10 minutes. |
| Was part of a team. | Led a team of 4 students to deliver a web app used by 300+ classmates. |
| Knowledge of Linux. | Maintain a fully scripted Linux setup synced across 2 machines with chezmoi. |
| Fixed bugs. | Fixed 25+ bugs reported by users, reducing support tickets by 30%. |

### ⚡ Verbos de logro

| Categoría | Verbos |
|---|---|
| Crear | built, developed, designed, created, implemented, launched, shipped |
| Mejorar | improved, optimized, reduced, increased, accelerated, streamlined |
| Liderar | led, mentored, coordinated, managed, drove, owned |
| Automatizar | automated, integrated, migrated, deployed, scaled |
| Analizar | analyzed, investigated, measured, evaluated, benchmarked |
| Colaborar | collaborated, partnered, contributed, supported |

⚠️ Cuidado: evita **"responsible for"**, **"helped with"**, **"worked on"**, **"participated in"**: describen presencia, no impacto. Y nunca inventes cifras: si no tienes números exactos, usa aproximados honestos ("about", "over").

### 🔗 LinkedIn en inglés

| Campo | ❌ Débil | ✅ Fuerte |
|---|---|---|
| Headline | Estudiante | Computer Science Student · Python & AI · Open to Remote Internships |
| About | "Soy responsable y trabajador" | 3–4 líneas: qué haces, con qué, qué buscas |
| Experience | Solo nombre del puesto | 2–3 bullets de logro |
| Featured | Vacío | Repos de GitHub, demos, artículos |
| Open to work | Desactivado | Activado para "Remote" y roles concretos |

🇬🇧 Mensaje para contactar a un reclutador: "**Hi Emily, I came across the Junior Backend role at Acme and I think my experience with Python and FastAPI could be a good fit. Would you be open to a quick chat? Thanks!**"

## ⚠️ Riesgos y errores de comunicación (aprende de otros)

La mayoría de los programadores que pierden un trabajo remoto no lo pierden por el código, sino por la **comunicación**. Estos son los errores que más se repiten en historias reales de equipos distribuidos.

### 🚨 Problema → consecuencia → cómo mitigarlo

| Problema | Consecuencia | Cómo mitigarlo |
|---|---|---|
| Asumir sin preguntar | Programas lo que no pedían | "Just to confirm, the expected behavior is...?" antes de empezar |
| No avisar bloqueos | Pierdes días; parece que no trabajas | Regla de los 30 min: si sigues atascado, pregunta |
| Mensajes ambiguos ("it's broken") | Ida y vuelta eterna | Qué, dónde, desde cuándo, qué probaste |
| Sobre-prometer plazos | Pierdes confianza | Estima con margen y supuestos ("assuming...") |
| Avisar el retraso tarde | El cliente se entera el día de la entrega | Avisa apenas lo sepas, con nueva fecha |
| Decir "yes" sin entender | Haces otra cosa | Parafrasea: "So you want me to..." |
| No documentar decisiones | Nadie recuerda por qué | Resumen escrito tras reuniones; ADRs |
| Desaparecer sin avisar | Parece abandono | Estado en Slack, aviso de OOO |
| Mensaje solo "hi" | Pierdes horas por zona horaria | Todo en un mensaje |
| Comentarios bruscos en review | Conflictos en el equipo | Prefijos y suavizadores |
| No pedir feedback | No sabes si vas bien | 1:1 regular: "How am I doing?" |
| Trabajar en silencio una semana | PR gigante rechazado | PRs pequeños y drafts tempranos |
| No leer el contrato | Problemas de pago o de IP | Lee todo; pregunta lo que no entiendas |
| Copiar código del cliente a repos públicos | Violación de NDA, despido | Nunca publiques código de trabajo |
| Pegar secretos en Slack o ChatGPT | Fuga de seguridad | Usa gestores de secretos; nunca pegues claves |
| Culpar a otros en incidentes | Ambiente tóxico | Lenguaje blameless: el proceso, no la persona |
| No confirmar zonas horarias | Faltas a reuniones | Escribe siempre la zona: "3 pm ET (UTC−5) / 4 pm Bolivia (UTC−4)" |
| Decir "it's done" sin probar | Bugs en producción | Define "done": probado, revisado, desplegado |
| Responder emocionalmente | Daño a la relación | Espera 1 hora antes de responder en caliente |
| Aceptar todo el scope creep | Trabajo gratis y retrasos | Ofrece opciones: "We can add X if we move Y" |

### 📖 Historias típicas (para no repetirlas)

| Lo que pasó | Lección |
|---|---|
| Un dev pasó 3 días atascado por miedo a "molestar"; un senior lo resolvía en 10 min. | Preguntar es parte del trabajo. |
| Un freelancer entregó "exactamente lo que entendió", pero el cliente quería otra cosa. | Escribe los acceptance criteria y que el cliente los confirme. |
| Un contractor publicó su trabajo en GitHub como portfolio y violó el NDA. | Pide permiso por escrito o haz proyectos propios. |
| Un equipo perdió un día porque "Friday" para uno era el viernes de otro país. | Fechas con zona horaria o en UTC. |
| Un junior respondió "LGTM" a un PR que no leyó; rompió producción. | Aprueba solo lo que realmente revisaste. |
| Un dev dijo "I'll have it tomorrow" sin mirar el código y tardó una semana. | "Let me take a look first and I'll give you an estimate." |

📌 Resumen: **pregunta pronto, avisa pronto, escribe claro, confirma por escrito**. Comunicar en exceso (over-communicate) en remoto nunca es un error.

## 🗓️ Plan de práctica de 30 y 90 días

La fluidez profesional viene de **usar** el inglés en tareas reales, no de estudiar listas. Este plan usa 20–40 minutos al día y se apoya en lo que ya haces: programar.

### 📅 Plan de 30 días

| Días | Objetivo | Actividad | Tiempo |
|---|---|---|---|
| 1 | Entorno en inglés | Sistema, navegador, editor y GitHub en inglés | 15 min |
| 2–3 | Commits | Reescribe en Conventional Commits los últimos 10 commits de un repo (en una rama de práctica) | 20 min |
| 4–5 | Commits con cuerpo | Cada commit del día con cuerpo que explique el porqué | 15 min |
| 6–7 | Issues | Escribe 1 bug report y 1 feature request para un proyecto tuyo | 30 min |
| 8–9 | Pull requests | Abre un PR en tu repo con la plantilla completa | 30 min |
| 10 | Code review | Lee 3 PRs de un proyecto open source grande y anota frases de review | 30 min |
| 11–12 | Preguntar | Redacta una pregunta estilo Stack Overflow con MRE de un bug real | 30 min |
| 13–14 | Chat | Únete a un Discord técnico en inglés y responde o pregunta algo | 20 min |
| 15–16 | Emails | Escribe 3 emails modelo: pedir, seguimiento, rechazar | 30 min |
| 17–18 | Standup | Grábate un standup de 45 s cada día sobre tus tareas reales | 10 min |
| 19–20 | Reuniones | Practica en voz alta las tablas de interrumpir, aclarar y discrepar | 20 min |
| 21 | Jerga | Escucha un podcast técnico y anota 10 expresiones de la jerga | 40 min |
| 22–23 | Tell me about yourself | Escríbelo, grábalo 3 veces, ajusta a 75 s | 30 min |
| 24–25 | STAR | Escribe 3 historias STAR y grábalas | 40 min |
| 26–27 | Live coding | 1 problema LeetCode Easy al día pensando en voz alta (grabado) | 40 min |
| 28 | Resume | Reescribe tu CV en inglés con verbos de logro | 60 min |
| 29 | LinkedIn | Headline, About y 2 proyectos en inglés | 40 min |
| 30 | Simulacro | Entrevista simulada con un amigo, Exponent o un LLM con voz | 60 min |

```tiempo
Días 1-5 : Entorno en inglés y commits
Días 6-14 : Issues, PRs, preguntas y chat
Días 15-21 : Emails, standup, reuniones, jerga
Días 22-27 : Tell me about yourself, STAR, live coding
Días 28-30 : Resume, LinkedIn y simulacro
```

### 🗺️ Plan de 90 días

| Mes | Meta | Hábitos semanales | Entregable al final |
|---|---|---|---|
| 1 | Escribir como en un equipo | Commits, issues y PRs siempre en inglés; 1 pregunta pública | Repo con historial limpio y PR modelo |
| 2 | Hablar con soltura | 3 standups grabados; 2 problemas en voz alta; 1 conversación con nativo (italki, Cambly o comunidad) | 5 historias STAR grabadas y pulidas |
| 3 | Salir al mercado | 1 contribución open source; 5 aplicaciones a puestos remotos; 1 simulacro por semana | Resume + LinkedIn + primera entrevista real |

| Semana del mes 3 | Acción concreta |
|---|---|
| 9 | Busca un `good first issue` y comenta "I'd like to work on this" |
| 10 | Abre tu primer PR en un proyecto ajeno |
| 11 | Aplica a 5 roles remotos con resume adaptado a cada uno |
| 12 | Simulacro final de entrevista técnica + conductual |

💡 Consejo: lleva una **libreta de frases** (o un mazo de Anki) con cada frase nueva que escuches en un podcast, PR o reunión. Repasar 5 minutos al día vale más que una hora el domingo.

### 📚 Recursos reales

| Recurso | Tipo | Nivel | Para qué |
|---|---|---|---|
| Conventional Commits (conventionalcommits.org) | Especificación | Todos | Formato oficial de commits |
| Keep a Changelog (keepachangelog.com) | Guía | Todos | Formato de changelog |
| Conventional Comments (conventionalcomments.org) | Guía | Todos | Prefijos de code review |
| Google Engineering Practices (Code Review) | Guía | Intermedio | Cómo revisar y ser revisado |
| Stack Overflow: "How do I ask a good question?" | Guía | Básico | Preguntar bien y MRE |
| Syntax | Podcast | Intermedio | Web dev, jerga natural |
| The Changelog | Podcast | Intermedio | Open source y carrera |
| Software Engineering Daily | Podcast | Avanzado | Arquitectura y sistemas |
| Latent Space | Podcast | Avanzado | IA aplicada e ingeniería de LLMs |
| Lex Fridman Podcast | Podcast | Avanzado | Entrevistas largas sobre IA |
| Fireship | YouTube | Intermedio | Inglés técnico rápido y moderno |
| NeetCode | YouTube | Intermedio | Problemas de entrevista explicados en voz alta |
| ByteByteGo | YouTube / newsletter | Intermedio | System design visual |
| Andrej Karpathy | YouTube | Avanzado | Deep learning explicado claro |
| freeCodeCamp | Web / YouTube | Básico | Cursos completos en inglés |
| Cracking the Coding Interview (G. L. McDowell) | Libro | Intermedio | Entrevistas técnicas |
| System Design Interview (Alex Xu) | Libro | Intermedio | System design paso a paso |
| The Pragmatic Programmer (Hunt y Thomas) | Libro | Intermedio | Cultura y vocabulario profesional |
| Never Split the Difference (Chris Voss) | Libro | Intermedio | Negociación (salario, clientes) |
| LeetCode / NeetCode.io | Práctica | Intermedio | Problemas de entrevista |
| Exercism | Práctica | Básico | Ejercicios con mentoría en inglés |
| Exponent (adquirió Pramp) | Simulacros | Intermedio | Entrevistas simuladas entre pares |
| interviewing.io | Simulacros | Avanzado | Entrevistas anónimas con ingenieros |
| italki / Cambly / Preply | Tutores | Todos | Conversación con nativos |
| Tandem / HelloTalk | Intercambio | Básico | Practicar a cambio de enseñar español |
| YouGlish | Pronunciación | Todos | Oír cómo dicen una frase en videos reales |
| LanguageTool / Grammarly | Corrector | Todos | Revisar emails y PRs |
| DeepL | Traductor | Todos | Verificar traducciones (no para todo) |
| Anki | Repetición espaciada | Todos | Memorizar frases |
| We Work Remotely / Remote OK / Wellfound | Bolsa de trabajo | Intermedio | Empleos remotos |
| Levels.fyi / Glassdoor | Salarios | Todos | Investigar rangos antes de negociar |

💡 Consejo: usa un LLM como **revisor**, no como escritor: escribe tú primero y luego pide "Correct my English and explain each mistake". Aprendes de tus errores en vez de copiar.

⚠️ Cuidado: no pegues código ni datos de tu empresa o cliente en herramientas externas sin permiso. Revisa la política de la empresa sobre IA.

📌 Resumen final: **escribe en inglés todo lo de Git, habla en voz alta cada día, prepara tus historias STAR, comunica pronto y por escrito**. En remoto, quien comunica bien parece (y es) mejor programador.
