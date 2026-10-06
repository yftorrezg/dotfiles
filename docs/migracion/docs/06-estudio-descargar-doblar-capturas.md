---
tags: [sistema, estudio, migracion, multimedia]
fecha: 2026-09-26
actualizado: 2026-09-28
origen: PC i7-6700K + GTX 980 (CachyOS + Hyprland Lua)
destino: Surface Pro 6 (i7-8650U) y ThinkPad E14 G4 (i7-12ª), Intel sin NVIDIA, 16 GB
---

# 06 · Estudio: descargar, doblar, capturas + apuntes automáticos y sesión de curso

Complementa a `01` (atajos de Hyprland y scripts de captura básicos) y `04` (mpv, paquetes). Lo que ya está explicado ahí no se repite: acá están `descargar`, `doblar`, el **sistema de capturas + apuntes automáticos de cursos** (creado el 26/09 y rehecho casi entero el 27-28/09) y el flujo de estudio completo con sus dependencias.

> **Guía para el usuario** (la fuente de verdad, en lenguaje simple): [[Guia-Auto-captura-de-cursos]] → `guias-usuario/Guia-Auto-captura-de-cursos.md` (copia de `~/Documentos/Guia-Auto-captura-de-cursos.md` del 28/09 noche). Este doc es la versión técnica para replicarlo.

Archivos copiados en `dotfiles/` (rutas relativas a `$HOME`). Criterio del paquete: todo lo que sirve igual en la laptop va a `dotfiles/`; solo lo que depende del hardware de la PC va a `solo-esta-pc/`. Ningún script de capturas/apuntes es exclusivo de la PC (los valores de la PC, como el monitor `HDMI-A-1` de la barrita, se ajustan con variables: ver §3.9).

| Archivo | Qué es |
|---|---|
| `.local/bin/descargar` | Descargador (usa yt-dlp) |
| `.local/bin/doblar` | Lanzador del doblaje (llama al venv) |
| `.local/share/doblar/doblar.py` | Programa de doblaje inglés→español (**actualizado 28/09**: versión del 26/09 22:59, ver §2) |
| `.local/share/doblar/requirements.txt` | `pip freeze` exacto del venv (referencia) |
| `.local/share/doblar/tarea-karpathy.sh` | Tarea de **una sola vez** de esta PC. **No se instala**: queda solo como ejemplo de `doblar --seguir` + `systemd-run` |
| `.config/hypr/scripts/` — 18 scripts de capturas/apuntes + 7 de pruebas | Sistema de capturas y apuntes (lista completa en §3.8) |
| `.config/hypr/config/binds.lua` | **Actualizado 28/09**: SUPER+ALT+S, **SUPER+ALT+Y** y **SUPER+ALT+A** |
| `.config/hypr/scripts/voz.conf` | Actualizado (velocidad de lectura SUPER+R `SPEED_MULT=1.4` desde el 05-10; era 1.2 el 27/09) |
| `.local/share/applications/abrir-markdown.desktop` | App por defecto de `.md`: Obsidian si está en una bóveda, si no VS Code |
| `.config/mimeapps.list` | **Actualizado**: `text/markdown` y `text/x-markdown` → `abrir-markdown.desktop` (antes `vscode-markdown-preview.desktop`) |
| `.config/obsidian/obsidian.json` | Lista de bóvedas de Obsidian (`~/Documentos/Obsidian Vault` y **`~/Vídeos`**). Rutas con `/home/yafer` |
| `Vídeos/.obsidian/` | Config de la bóveda "Vídeos": `app.json`, `appearance.json`, `core-plugins.json`, `community-plugins.json` y el plugin **Spaced Repetition 1.15.4** (`plugins/obsidian-spaced-repetition/{main.js,manifest.json,styles.css,data.json}`; `data.json` = ajustes en español + agenda vacía). **Sin** `workspace.json` (estado de pestañas) |

Los demás scripts de estudio (`captura-*.sh`, `elegir-carpeta-capturas.sh`, `carpeta-capturas.conf`, `curso-*.sh`, `curso.conf`, `pomodoro-toggle.sh`, `auto-captura.conf`, `auto-captura-toggle.sh`) y todo `~/.config/mpv/` siguen iguales al original (verificado con `diff -rq` el 28/09).

**No se copió** (a propósito): `~/.local/share/doblar/venv` (455 MB), `nllb/` (2,4 GB), `whisper/` (835 MB), `~/.cache/doblar`, `~/.cache/huggingface`, `~/.cache/auto-captura/` (logs, cola, locks), `__pycache__`, cookies, y **ningún dato de estudio**: capturas, videos, `apuntes.md`, `resumen.md`, `tarjetas*.{md,txt}`, `INDICE.md`, `~/Vídeos/Mis cursos.md`, `.minutos.tsv`, `.youtube-id`. Tampoco `Vídeos/.obsidian/workspace.json` (qué notas estaban abiertas). No hay archivos de cookies: `descargar` y `video-a-capturas.sh` toman la sesión directo de Brave / no la necesitan.

---

## 1. `descargar`: videos, playlists y cursos completos

### Qué hace
Baja con **yt-dlp** un video, una playlist o un curso completo (YouTube, Platzi, Udemy sin DRM, Instagram, Facebook, X, Vimeo, Twitch, Hotmart…), usando la sesión que ya tengas abierta en **Brave** (para cursos pagos). Si lo cortás y lo volvés a lanzar, **sigue donde quedó** y no repite lo ya bajado.

### Cómo se usa (solo terminal; no hay atajo, ni `.desktop`, ni botón de OpenDeck, ni menú de Dolphin)
```bash
descargar "https://www.youtube.com/playlist?list=..."     # video, playlist o curso
descargar url1 url2 url3                                    # varios a la vez
descargar --mp3 "url"                                       # solo audio → ~/Música/Descargas
NAVEGADOR=firefox descargar "url"                           # tomar la sesión de otro navegador
DESTINO=~/Cursos descargar "url"                            # otra carpeta
SIN_COOKIES=1 descargar "url"                               # sin la sesión (contenido público)
descargar -s "url"                                          # cualquier opción extra va a yt-dlp (-s = simular)
```
- Destino: `$(xdg-user-dir VIDEOS)/Descargas` = **`~/Vídeos/Descargas`** (con tilde, carpeta del sistema en español).
- Las playlists/cursos quedan en su carpeta y numerados: `Nombre del curso/001 - Título.mp4`. Los videos sueltos van directo a `Descargas/`.
- Registro de lo ya bajado: `~/Vídeos/Descargas/.descargados.txt`.

### Cómo funciona por dentro
Arma una llamada a `yt-dlp` con: `-f "bv*+ba/b"` (mejor video + mejor audio) → `--merge-output-format mp4`; subtítulos `es.*,en.*` incrustados; metadatos y miniatura incrustados; `--download-archive`, `--ignore-errors --no-overwrites --continue`; `--cookies-from-browser brave`; si existe `aria2c`, lo usa con 8 conexiones (`-x 8 -s 8 -k 1M`). En modo `--mp3`: `-f ba/b -x --audio-format mp3 --audio-quality 0`.
- No hay config global de yt-dlp (`~/.config/yt-dlp/` y `/etc/yt-dlp.conf` **no existen**): todo está en el script.
- YouTube hoy exige resolver un reto JavaScript: por eso yt-dlp depende de `yt-dlp-ejs` → **`deno`** (se instalan solos como dependencias).

### Dependencias (versiones de esta PC)
| Paquete | Versión | Repo | Para qué |
|---|---|---|---|
| yt-dlp | 2026.08.19-1 | extra | descargador |
| yt-dlp-ejs + deno | 0.8.0-1 / 2.9.7 | extra / cachyos | retos JS de YouTube (dependencia automática) |
| ffmpeg | 2:9.0.2 | cachyos | unir video+audio, incrustar subs/miniatura |
| aria2 | 1.37.0 | extra | descarga en paralelo (opcional) |
| python-curl_cffi | 0.16.3 | extra/cachyos | hacerse pasar por un navegador (algunos sitios lo exigen) |
| xdg-user-dirs | — | extra | `xdg-user-dir VIDEOS` |

Recomendado agregar en la laptop (hoy **no** están y algunas plataformas de cursos los necesitan): `python-pycryptodomex` (videos HLS cifrados AES-128, típico de Hotmart/plataformas de cursos), `python-mutagen` (miniatura en algunos formatos), `python-secretstorage` (leer las cookies de Brave si usa gnome-keyring).

### Reinstalar en la laptop
```bash
sudo pacman -S --needed yt-dlp ffmpeg aria2 python-curl_cffi python-pycryptodomex python-mutagen python-secretstorage xdg-user-dirs
install -Dm755 ~/migracion-cachyos/dotfiles/.local/bin/descargar ~/.local/bin/descargar
xdg-user-dirs-update   # asegura ~/Vídeos y ~/Música
```
`~/.local/bin` ya está en el PATH (fish/uwsm, ver doc 04).

### Cómo probar
1. `descargar -s "https://www.youtube.com/watch?v=jNQXAC9IVRw"` → debe listar formatos/título sin error.
2. Iniciar sesión en Brave en el sitio del curso y probar `descargar -s "<url del curso>"`. Si sale `failed to decrypt cookies` o `could not find ... cookies`: cerrar Brave y reintentar, probar `NAVEGADOR=brave+gnomekeyring` o `brave+kwallet` (yt-dlp acepta `navegador+keyring`), o instalar `python-secretstorage`.

### Problemas detectados
- Quedó una carpeta vieja `~/Videos/Descargas` (sin tilde) de la primera versión del script; la tarea `tarea-karpathy.sh` la mueve a `~/Vídeos` cuando termina. En la laptop no hace falta.
- Udemy con DRM (Widevine) no se puede bajar: es una limitación, no un error.
- WhatsApp Web y Telegram privado no funcionan con yt-dlp (bajarlos desde sus apps).

---

## 2. `doblar`: doblar videos inglés → español

### Qué hace
Toma videos en inglés y genera `video.es.mp4` (o `.es.mkv`) con:
- **audio 1 (por defecto): voz en español** sincronizada con el profesor,
- **audio 2: el inglés original** (se cambia desde mpv con `#` o desde uosc),
- **subtítulos español e inglés** (desactivados por defecto).

Si el video ya está en español (u otro idioma) lo salta. Por defecto **borra el original** cuando el doblado salió bien (el `.es.mp4` ya contiene todo).

### Cómo se usa
```bash
doblar video.mp4                          # uno
doblar "~/Vídeos/Descargas/Curso X/"      # carpeta entera (recursiva; salta los ya doblados)
doblar --seguir "~/Vídeos/Descargas/Curso X/"   # dobla cada video apenas termina de bajarse
# Típico: en una terminal `descargar "url-del-curso"` y en otra `doblar --seguir "carpeta"`.
```
Variables:
| Variable | Por defecto | Efecto |
|---|---|---|
| `MODELO` | `small` | modelo de Whisper para la vía CPU (`tiny`, `base`, `small`, `medium`…) |
| `VOZ` | `es-MX-JorgeNeural` | voz de edge-tts (ej. `es-AR-ElenaNeural`, `es-MX-DaliaNeural`) |
| `VELOCIDAD` | `10` | % extra de velocidad de la voz |
| `FONDO` | `0` | volumen del inglés de fondo bajo la voz (ej. `0.15`) |
| `SOLO_SUBS` | — | `1` = solo genera `.es.srt`/`.en.srt`, sin voz |
| `BORRAR_ORIGINAL` | `1` | `0` = conserva el video original |

Para trabajos largos en segundo plano (como se hizo con Karpathy):
`systemd-run --user --unit=doblar-curso doblar --seguir "carpeta"` y `journalctl --user -u doblar-curso -f` para ver el progreso.

Se puede cortar con Ctrl+C: todo queda en caché (`~/.cache/doblar/<hash>/`: transcripción, traducción, audios) y al relanzar sigue.

### Cómo funciona por dentro (4 etapas)
| # | Etapa | Herramienta / modelo | Dónde corre | Tamaño |
|---|---|---|---|---|
| 1 | **Transcripción** en inglés con marcas de tiempo por palabra; detecta idioma (si no es inglés, no dobla) | **Vía A (GPU)**: `whisper-cli` (whisper.cpp, paquete `whisper-cpp` + `ggml-vulkan`) con `ggml-large-v3-turbo-q8_0.bin` (HF `ggerganov/whisper.cpp`) + VAD `ggml-silero-v5.1.2.bin` (HF `ggml-org/whisper-vad`). **Vía B (CPU)**: `faster-whisper` 1.2.1 (CTranslate2) modelo `small` int8 (HF `Systran/faster-whisper-small`, se baja solo a `~/.cache/huggingface` la primera vez) con `vad_filter` | A: GPU por **Vulkan** (la GTX 980 no sirve con CUDA de CTranslate2, pero sí con Vulkan). B: CPU, todos los hilos | 834 MB + 0,9 MB / ~480 MB |
| 2 | Agrupa palabras en frases y **traduce** | **NLLB-200 distilled 600M** de Meta convertido a CTranslate2 (HF `entai2965/nllb-200-distilled-600M-ctranslate2`, en `~/.local/share/doblar/nllb/`), `compute_type=int8`, beam 4, lotes de 32. 100% local | CPU | 2,4 GB en disco (float32) |
| 3 | **Voz** en español, frase por frase, y sincronización: si la frase no entra en el hueco, pide la voz más rápida (hasta ×1,3) y, si aún sobra, `atempo` de ffmpeg (hasta ×1,1); lo que no entra se corre un poco y se recupera en la siguiente pausa | **edge-tts** 7.2.8 (voces Neural de Microsoft), 6 pedidos en paralelo | **Internet** (servidores de Microsoft) | — |
| 4 | **Mezcla**: copia el video sin recodificar, audio AAC 160k, subs `mov_text` (mp4) o srt (mkv); verifica duración y 2 pistas; recién ahí reemplaza el original | ffmpeg / ffprobe | CPU | — |

Detalles:
- La vía A se usa **solo si** existen `whisper-cli` **y** `whisper/ggml-large-v3-turbo-q8_0.bin`. Si falla, cae sola a la vía B.
- Mientras un video se traduce y se le pone voz, **ya transcribe el siguiente** en otro hilo (`adelantar`). En la vía CPU eso significa dos trabajos pesados a la vez (ver laptop).
- Historia: primero se usó Google Translate, que bloqueó la conexión ("Sorry") → se cambió a NLLB local.
- Calidad medida aquí: la voz va en promedio 0,1 s (máx. 0,6 s) detrás del video.

### Dependencias exactas
Sistema (pacman): `ffmpeg` 2:9.0.2, `python` 3.14.7 (el venv usa `/usr/bin/python3.14`), y para la vía GPU `whisper-cpp` 1.9.3 + `ggml-vulkan` 0.25.2 (ambos existen en `extra` y en `cachyos-extra-v3`) + el driver Vulkan de la GPU.

venv (`~/.local/share/doblar/venv`), paquetes directos → versión:
`faster-whisper==1.2.1`, `ctranslate2==4.8.2`, `sentencepiece==0.2.2`, `edge-tts==7.2.8`, `numpy==2.5.3`, `soundfile==0.14.0`, `huggingface_hub==1.33.0` (el resto son dependencias; lista completa en `dotfiles/.local/share/doblar/requirements.txt`).

Nota: `edge-tts` también está instalado aparte con **pipx** (lo usa la lectura SUPER+R, doc 02). Son independientes.

### En las laptops (sin NVIDIA): qué usar y cuánto tarda
Referencia medida en esta PC con la **vía CPU** (i7-6700K, 4 núcleos/8 hilos, Whisper `small`): 2,5 min de video ≈ 80 s → **1 hora de video ≈ 30 min** (casi todo es la transcripción; la traducción NLLB suma unos minutos; la voz depende de internet).

| Laptop | Recomendación | Tiempo aprox. por 1 h de video |
|---|---|---|
| **Surface Pro 6** (i7-8650U, 4c/8t, 15 W, se calienta y baja frecuencia) | Vía CPU. `MODELO=small` (por defecto) si puede quedar enchufada trabajando; si es muy lento, `MODELO=base` (≈2× más rápido, algo menos preciso). **No** instalar el modelo turbo: por Vulkan en la UHD 620 sería más lento que la CPU. | small: **~45–70 min**; base: ~25–40 min |
| **ThinkPad E14 G4** (i7-1255U/1260P, 10–12 núcleos, Iris Xe) | Vía CPU con `small` funciona bien. Opcional: probar la vía Vulkan en la Iris Xe (instalar `whisper-cpp ggml-vulkan vulkan-intel` y bajar los 2 modelos a `whisper/`) y comparar el tiempo con un video de 5 min; quedarse con la más rápida. | small CPU: **~25–35 min**; Vulkan Iris Xe: probar |

Son estimaciones (no medidas en las laptops). Consejos para 16 GB y portátiles:
- Enchufada y con perfil de rendimiento; en la Surface, dejarla ventilar.
- El servicio de esta PC llegó a un **pico de 9 GB** de memoria (el número de systemd incluye la caché de archivos, el uso real es menor): no correr doblajes en paralelo, un solo `doblar` a la vez.
- Si molesta que la CPU haga dos cosas a la vez (transcribir el siguiente + traducir el actual), se puede comentar la línea `adelantar(siguiente)` en `doblar.py` (hoy la línea ~322).
- `SOLO_SUBS=1` es mucho más rápido (se salta la voz) si solo querés subtítulos en español.

### Reinstalar en la laptop, paso a paso
```bash
sudo pacman -S --needed ffmpeg python
install -Dm755 ~/migracion-cachyos/dotfiles/.local/bin/doblar ~/.local/bin/doblar
install -Dm644 ~/migracion-cachyos/dotfiles/.local/share/doblar/doblar.py ~/.local/share/doblar/doblar.py
cd ~/.local/share/doblar
python -m venv venv
venv/bin/pip install faster-whisper ctranslate2 sentencepiece edge-tts numpy soundfile huggingface_hub
# (para clonar versiones exactas: venv/bin/pip install -r ~/migracion-cachyos/dotfiles/.local/share/doblar/requirements.txt)
# Modelo de traducción (2,4 GB):
venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('entai2965/nllb-200-distilled-600M-ctranslate2', local_dir='nllb', allow_patterns=['model.bin','config.json','shared_vocabulary.json','sentencepiece.bpe.model'])"
# El modelo Whisper 'small' para CPU se baja solo en el primer uso.
```
Solo si se quiere la vía Vulkan (ThinkPad, opcional):
```bash
sudo pacman -S --needed whisper-cpp ggml-vulkan vulkan-intel vulkan-tools
vulkaninfo --summary | grep deviceName        # debe mostrar la Intel Iris Xe
mkdir -p ~/.local/share/doblar/whisper && cd ~/.local/share/doblar/whisper
../venv/bin/python -c "from huggingface_hub import hf_hub_download as d; d('ggerganov/whisper.cpp','ggml-large-v3-turbo-q8_0.bin',local_dir='.'); d('ggml-org/whisper-vad','ggml-silero-v5.1.2.bin',local_dir='.')"
```
(Para volver a la CPU, basta con borrar o renombrar `ggml-large-v3-turbo-q8_0.bin`.)

Alternativa si no hay tiempo: copiar `nllb/` (y `whisper/`) desde esta PC por disco externo en vez de bajarlos. **No** copiar el `venv` (depende de la versión exacta de Python).

### Cómo probar
```bash
yt-dlp -f "b[height<=480]" -o ~/prueba.mp4 --download-sections "*0:00-2:00" "https://www.youtube.com/watch?v=aircAruvnKk"
BORRAR_ORIGINAL=0 doblar ~/prueba.mp4        # debe decir "Transcribiendo inglés (CPU, Whisper small)..."
mpv ~/prueba.es.mp4                          # voz en español; tecla # (default de mpv) cambia al inglés; J cambia de subtítulo, v los muestra/oculta (j está remapeada a -10 s)
```

### Problemas detectados
- **`BORRAR_ORIGINAL=1` por defecto**: borra el video original si el doblado pasó la verificación. Es intencional, pero conviene saberlo.
- **Necesita internet** para la voz (edge-tts) y **manda el texto traducido a Microsoft**. Si edge-tts falla 4 veces en una frase, esa frase queda muda (no hay respaldo con Piper, a diferencia de SUPER+R).
- `whisper-cli` usa `-t 4` fijo (4 hilos), está pensado para la vía GPU.
- La copia de `doblar.py` es la versión del **26/09 22:59** (actualizada en el paquete el 28/09). Cambios respecto de la anterior: la caché `~/.cache/doblar/<hash>` ahora usa **nombre + tamaño** del video (no la ruta: mover la carpeta del curso no pierde lo hecho); si la voz va atrasada más de 1 s permite acelerar hasta ×1,45 (`MAX_ALCANCE`) para alcanzar al orador; avisa si el orador habla tan rápido que el doblaje quedó desfasado (>3 s de media: mejor inglés + subtítulos); un error en un video ya no corta la carpeta (sigue con el siguiente).
- En este momento corre en esta PC el servicio temporal `doblar-karpathy` (`systemd-run`, curso "Neural Networks: Zero to Hero"). No es parte de la configuración: no replicar.

---

## 3. Capturas y apuntes automáticos de cursos (estado al 28/09 noche)

### 3.1 Capturas manuales (sin cambios; ya documentadas en doc 01 §2.5 y doc 03)
| Atajo / botón | Qué hace |
|---|---|
| Impr / SUPER+Impr | Noctalia: zona / pantalla → abre **satty** para editar |
| SUPER+SHIFT+S · botón del pulgar del M720 | `captura-portapapeles.sh`: slurp → grim → `wl-copy` (solo portapapeles) |
| CTRL+SHIFT+S · clic de la rueda del M720 | `captura-guardar.sh`: zona → PNG `captura_AAAAMMDD_HHMMSS.png` en la carpeta de `carpeta-capturas.conf` + portapapeles |
| CTRL+SHIFT+D | `elegir-carpeta-capturas.sh`: zenity para elegir la carpeta (por materia/curso) |

Intención del usuario (de `~/Documentos/aprender/funciones.md`): **máximo 2 pasos** (atajo → arrastrar la zona), sin confirmar ni editar.

### 3.2 Qué es y los atajos
La compu saca capturas **solo cuando aparece algo nuevo** en el curso y arma, por cada clase, un **cuadernillo** (`apuntes.md`), un **repaso corto** (`resumen.md`) y **tarjetas de repaso** (`tarjetas.md`), más un índice por curso y un panel con todos los cursos. El usuario se concentra en entender y practicar.

| Atajo | Script | Qué hace |
|---|---|---|
| **SUPER+ALT+A** | `curso-apuntes-elegir.sh` | zenity para elegir la carpeta de un **curso descargado** → capturas + apuntes de todas las clases (pasa por la cola) |
| **SUPER+ALT+Y** | `youtube-capturas.sh` | Toma el **link de YouTube del portapapeles** (`wl-paste`). Si tiene `list=`, zenity pregunta "Solo este video" o "Playlist entera (N videos · H h)" (los mixes `RD…`, `WL`, `LL` se tratan como video suelto). Pasa por la cola |
| **SUPER+ALT+S** | `auto-captura-toggle.sh` → `auto-captura.py` | Captura **en vivo** del monitor con foco (Udemy, Platzi…); otra vez = parar. **No** arma cuadernillo (no tiene subtítulos) |
| CTRL+SHIFT+S | `captura-guardar.sh` | Captura manual de una zona |

Truco del usuario: **A** = Apuntes · **Y** = YouTube · **S** = Screen. Los tres binds están en `binds.lua` (líneas ~134-142).

### 3.3 Flujo completo
```
SUPER+ALT+Y  youtube-capturas.sh  ─┐   (link copiado; playlist → pregunta con zenity)
SUPER+ALT+A  curso-apuntes-elegir.sh ┤  (carpeta del curso)
                                     ▼
            cola-capturas.sh  — UN pedido a la vez, en orden, sin duplicados (flock)
      ┌──────────────────────┼───────────────────────────┐
video-a-capturas.sh   playlist-a-apuntes.sh        curso-a-apuntes.sh
(un video o link)     (yt-dlp --flat-playlist,     (cada video de la carpeta;
                       carpeta NNN - título,         prefiere el .es.mp4 doblado,
                       .youtube-id, MAX_VIDEOS)      ignora .part)
                              └── ambos llaman a video-a-capturas.sh por clase, con nice 19 + ionice idle
Por cada clase (video-a-capturas.sh):
 1. 📥 yt-dlp (solo links): video sin audio ≤1080p H.264 + subtítulos es/en (.srt)     barrita 0-25 %
 2. 📸 auto-captura.py --video: ffmpeg a 1 fps → 0001.webp, 0002.webp… + .minutos.tsv   25-85 %
 3. 🤖 cuadernillo.py: elige capturas + subtítulos + OCR (tesseract) + UNA llamada a
       claude -p --model sonnet → apuntes.md + resumen.md (+ .apuntes-ia.json/.resumen-ia.json)
       + capturas/INDICE.md del curso                                                  85-100 %
 4. 🃏 tarjetas.py → tarjetas.md (Obsidian Spaced Repetition) + tarjetas-anki.txt (sin IA)
 5. 📋 panel-cursos.py → ~/Vídeos/Mis cursos.md
 6. 🗑️ si era un link: borra el video (quedan capturas + subtítulos + apuntes)
 📊 progreso.py "seguir": barrita de progreso durante todo el proceso; 1 notificación al final
```
Salida:

| Cómo | Carpeta |
|---|---|
| Curso (SUPER+ALT+A) | `<curso>/capturas/<clase>/` + `<curso>/capturas/INDICE.md` |
| Link (SUPER+ALT+Y) | `~/Vídeos/Capturas de YouTube/<título>/` (si hay 2 títulos iguales: `<título> [id]`) |
| Playlist | `~/Vídeos/Capturas de YouTube/<playlist>/capturas/NNN - título/` + `INDICE.md` |
| Video local (`video-a-capturas.sh archivo`) | `<carpeta del video>/capturas/<clase>/` |
| En vivo (SUPER+ALT+S) | `<carpeta-capturas.conf>/auto_FECHA_HORA_<título>/` |

Logs: `~/.cache/auto-captura/*.log`. Cola: `~/.cache/auto-captura/{cola.txt,actual.txt,cola.lock,trabajador.lock,trabajador.pid}`.

### 3.4 Piezas y decisiones técnicas (qué cambió el 27-28/09)
| Tema | Estado actual | Por qué |
|---|---|---|
| **Descarga (yt-dlp)** | `-f "bv*[height<=1080]" -S "proto,vcodec:h264"` + `--write-subs --write-auto-subs --sub-langs "es,es-orig,en,en-orig" --convert-subs srt --sleep-subtitles 2` | Sin `-S` elegía el HLS m3u8: **6 GB en vez de 335 MB** para la misma resolución. Solo video (sin audio): las capturas no lo necesitan |
| **Formato de capturas** | **WebP sin pérdida** (`lossless=True, method=1, quality=50`): píxeles idénticos al PNG, ~57 % del tamaño (≈43 % menos). WebP *con* pérdida **no**: difumina el código chico y empeora el OCR | Elección del usuario (28/09) por espacio |
| **Nombres** | `0001.webp`, `0002.webp`… El minuto del video va en el oculto `.minutos.tsv` (`0001.webp<TAB>01-23-45`). `cuadernillo.py` también entiende los nombres viejos `0012_01-23-45.png` | Pedido del usuario (28/09) |
| **Scripts de conversión** | `capturas-a-webp.py <carpeta>` (PNG→WebP, verifica píxel por píxel antes de borrar, corrige links de los apuntes, nice 19, multiproceso) · `capturas-nombre-corto.py` (renombra viejas y escribe `.minutos.tsv`) | Para cursos procesados antes del 28/09 |
| **Algoritmo de captura** | Igual que el 26/09 (bloques de 32 px, 2 s de pantalla quieta, tope 6 s, guarda el frame anterior ante scroll ≥30 %, ignora cursor/mouse/parpadeos) **+ detecta la webcam del profe** (mancha compacta ≥10 bloques que cambia con el resto quieto) **+ historial exigente**: solo descarta si cada línea está entera e idéntica en una de las últimas 30 | Cursos de programación: "cada variable importa" |
| **Cuadernillo** (`cuadernillo.py`) | Elige capturas "importantes" (una queda superada si la siguiente la contiene y agrega bastante), junta subtítulos (a Claude le pasa los **originales en inglés**; para leer muestra los de español), OCR con tesseract cada ~4 min (código real), y **una sola llamada** a Claude. Lo que Claude agrega por su cuenta va marcado **(extra)**. Sin subtítulos, arma con el OCR | — |
| **Modelo de IA** | `claude -p --output-format json --tools "" --strict-mcp-config --no-session-persistence --system-prompt … --model sonnet`. Variable **`APUNTES_MODELO`** (por defecto `sonnet`; `opus` para un curso difícil; `""` = el de la cuenta). Busca un `claude` que funcione (primero `~/.local/bin/claude`, salteando el `/usr/bin/claude` roto de npm) | El usuario eligió Sonnet el 28/09 para ahorrar cuota |
| **resumen.md** | Sale en la **misma llamada** (campo `corto` del JSON). `resumen-corto.py` queda solo para clases viejas (`--todos <carpeta capturas/>`, ~1 min por clase, parte de `.apuntes-ia.json`) | No gasta una llamada extra |
| **Tarjetas** (`tarjetas.py`) | `tarjetas.md` (~20-30 tarjetas: preguntas del resumen, conceptos "¿Qué es…?", chuleta "¿Cómo…?") con el formato del plugin Spaced Repetition; conserva los `<!--SR:` al regenerar y la sección "✍️ Mis tarjetas". `tarjetas-anki.txt` para importar en Anki. **No llama a Claude** | Repaso a largo plazo |
| **Panel** (`panel-cursos.py`) | `~/Vídeos/Mis cursos.md`: cursos, clases, horas, casilla por clase + links a apuntes/resumen/tarjetas. Conserva las casillas (por ruta de clase) y la sección "📝 Mis notas". Se regenera al terminar cada video/curso | — |
| **Cola** (`cola-capturas.sh`) | `encolar <video|playlist|curso> <arg> [etiqueta]`, `estado`, `vaciar`, `cancelar` (mata el grupo del trabajador; se retoma después), `trabajar` (interno). Las variables `SIN_IA`, `SIN_APUNTES`, `MAX_VIDEOS` viajan con cada pedido | Que no compitan por la CPU |
| **Playlists** (`playlist-a-apuntes.sh`) | Lista sin bajar (`--flat-playlist`, `lang=es`), una carpeta por video con `.youtube-id` → **se puede cortar y retomar**; saltea privados/eliminados; ante el anti-bot de YouTube ("no sos un robot"/429) espera 10 min y reintenta, y si sigue, corta y avisa | — |
| **Barrita** (`progreso.py`) | Ventana **GTK4 + gtk4-layer-shell** de 420×26 px, capa OVERLAY, sin foco de teclado, los clics pasan, abajo a la derecha del monitor **`HDMI-A-1`** (el vertical de la PC). Azul trabajando / verde listo / rojo falló; varias se apilan. Se relanza a sí misma con `LD_PRELOAD=/usr/lib/libgtk4-layer-shell.so`. Si no puede (sin Wayland/layer-shell) cae a una notificación con caracteres ▰▱. `PROGRESO_MODO=notificacion` fuerza la notificación; `PROGRESO_MONITOR=<conector>` cambia el monitor | Noctalia no dibuja barras gráficas en notificaciones |
| **Markdown por defecto** | `abrir-markdown.desktop` → `abrir-markdown.py`: si el `.md` está en una bóveda de `~/.config/obsidian/obsidian.json` abre `obsidian://open?path=…`, si no `code --open-url vscode://file…`. `~/Vídeos` registrada como bóveda "Vídeos" | Obsidian dibuja los bloques plegables (callouts) que VS Code muestra como texto |

### 3.5 Tiempos y costos medidos (PC i7-6700K)
| Qué | Tiempo |
|---|---|
| **Playlist / curso con IA** | **~10,5 min por hora de video** (medido el 28/09): 15 h ≈ 3 h (una noche), 70 h ≈ 12-15 h |
| Video de YouTube de 23 min | 2,5 min en total |
| Capturas de un video 4K de 2,5 h | ~30 min (1080p: bastante menos) |
| Cuadernillo de una clase de 2 h | ~5 min (elegir capturas + OCR + Claude) |
| En vivo | nada extra |

Capturas: diapositivas ~3/min, código intenso (Karpathy) ~7-8/min; en el cuadernillo se ven 3-4 por tema.

**Costos:** no hay API key ni cobro por uso: `claude -p` usa la **suscripción de Claude del usuario** (la misma sesión de Claude Code) y consume **cuota del plan**. Lo que gasta depende de las **horas de video** (largo de la transcripción + OCR), no de la cantidad de videos. Sonnet gasta bastante menos cuota que Opus. **Cuota agotada (cambio del 28/09 noche):** si Claude contesta que se alcanzó el límite ("You've hit your session limit · resets …"), `cuadernillo.py` (`llamar_claude`) **no sigue sin IA**: espera 10 min y reintenta, hasta `APUNTES_ESPERA_MAX_H` horas (por defecto 6; la cuota se renueva cada ~5 h). `resumen-corto.py` usa la misma función. Si igual queda alguna clase sin IA (Claude no respondió), al final de un curso/playlist `rehacer-sin-ia.py` rehace las clases que tienen `apuntes.md` pero no `.apuntes-ia.json` (sin volver a bajar el video: usa los subtítulos guardados y el OCR de las capturas) y luego tarjetas, `INDICE.md` y panel; las hechas a propósito con `SIN_IA=1` llevan el archivo `.sin-ia` y se saltean. A mano: `python3 rehacer-sin-ia.py <carpeta capturas/>` o `cuadernillo.py … --forzar`. Con playlists enormes (la de 166 videos que corre hoy) igual conviene repartir en varias noches.

### 3.6 Ajustes y comandos útiles
- Capturas: `~/.config/hypr/scripts/auto-captura.conf` (sin cambios: `INTERVALO=1`, `ESTABLE=2`, `TOPE=6`, `GRANDE=0.30`, `RUIDO=28`, `MIN_PIXELES=6`, `MASCARA_ABAJO=0`, `HISTORIAL=30`). Repetidas → subir `RUIDO`; se pierde algo → bajarlo.
- Variables: `SIN_IA=1` (apuntes sin Claude) · `SIN_APUNTES=1` (solo capturas) · `APUNTES_MODELO=opus` · `APUNTES_ESPERA_MAX_H=6` (horas máximas esperando cuota) · `MAX_VIDEOS=2` (probar una playlist) · `PROGRESO_MODO=notificacion` · `PROGRESO_MONITOR=eDP-1`.
```bash
~/.config/hypr/scripts/video-a-capturas.sh "<link o video.mp4>"
~/.config/hypr/scripts/curso-a-apuntes.sh "<carpeta del curso>"
MAX_VIDEOS=2 ~/.config/hypr/scripts/playlist-a-apuntes.sh "<link de playlist>"
~/.config/hypr/scripts/cola-capturas.sh estado | vaciar | cancelar
python3 ~/.config/hypr/scripts/cuadernillo.py "<carpeta de capturas>" --video video.mp4 --forzar
python3 ~/.config/hypr/scripts/resumen-corto.py --todos "<carpeta capturas/ del curso>"
python3 ~/.config/hypr/scripts/capturas-a-webp.py "<carpeta>"
```
Regla para Claude: **no editar un `.sh` mientras un curso se está procesando** (bash lo lee a medida que lo ejecuta); escribirlo aparte y hacer `mv`.

### 3.7 Pruebas
```bash
python3 ~/.config/hypr/scripts/auto-captura-tests.py     # 10 casos → TODO OK
python3 ~/.config/hypr/scripts/auto-captura-estres.py    # 200 cambios de 1 carácter → 0 perdidos
python3 ~/.config/hypr/scripts/cuadernillo-tests.py      # 8 + 2 de cuota agotada → TODO OK
python3 ~/.config/hypr/scripts/resumen-corto-tests.py    # 4/4
python3 ~/.config/hypr/scripts/tarjetas-panel-tests.py   # 11/11
bash ~/.config/hypr/scripts/cola-capturas-tests.sh       # 14 → OK
bash ~/.config/hypr/scripts/playlist-a-apuntes-tests.sh  # 19 → OK
```
(Corridas en la PC el 28/09 por la sesión que hizo los cambios; **no** se volvieron a correr al armar este paquete para no cargar la PC mientras procesa una playlist de 166 videos.)

### 3.8 Archivos (todos en `dotfiles/.config/hypr/scripts/`)
| Archivo | Rol |
|---|---|
| `auto-captura.py` | Motor de capturas (en vivo `--monitor X` o `--video archivo`) |
| `auto-captura-toggle.sh` | SUPER+ALT+S |
| `auto-captura.conf` | Ajustes |
| `video-a-capturas.sh` | Un video o link → capturas + apuntes (+ tarjetas + panel) |
| `youtube-capturas.sh` | SUPER+ALT+Y |
| `curso-apuntes-elegir.sh` | SUPER+ALT+A |
| `curso-a-apuntes.sh` | Curso entero (lock, reanudable, nice, prefiere `.es.mp4`) |
| `playlist-a-apuntes.sh` | Playlist → curso |
| `cola-capturas.sh` | Cola |
| `cuadernillo.py` | `apuntes.md` + `resumen.md` + `INDICE.md` |
| `resumen-corto.py` | `resumen.md` para clases viejas |
| `tarjetas.py` | `tarjetas.md` + `tarjetas-anki.txt` |
| `panel-cursos.py` | `~/Vídeos/Mis cursos.md` |
| `progreso.py` | Barrita / notificación de progreso |
| `capturas-a-webp.py`, `capturas-nombre-corto.py` | Conversión de capturas viejas |
| `rehacer-sin-ia.py` | Rehace con IA las clases que quedaron sin resumen (lo llaman `curso-a-apuntes.sh` y `playlist-a-apuntes.sh` al final) |
| `abrir-markdown.py` | `.md` → Obsidian o VS Code |
| `auto-captura-tests.py`, `auto-captura-estres.py`, `cuadernillo-tests.py`, `resumen-corto-tests.py`, `tarjetas-panel-tests.py`, `cola-capturas-tests.sh`, `playlist-a-apuntes-tests.sh` | Pruebas |

### 3.9 Adaptaciones para la laptop
| Tema | En la PC | En la laptop |
|---|---|---|
| **Barrita de progreso** | `progreso.py` busca el monitor **`HDMI-A-1`** (el vertical) | En la laptop no hay monitor vertical. Si `HDMI-A-1` no existe, `Capa.set_monitor(None)` deja que Hyprland la ponga en el **monitor enfocado** (la interna): funciona sin tocar nada. Ojo: la **Arzopa por HDMI también se llama `HDMI-A-1`** → con la Arzopa conectada la barrita irá ahí (puede estar bien). Para fijarla en la interna: `export PROGRESO_MONITOR=eDP-1` en `~/.config/uwsm/env` (o cambiar el valor por defecto en `progreso.py` línea 33). Preguntar al usuario |
| **GPU** | El sistema de capturas/apuntes **no usa la GPU** (ffmpeg decodifica por CPU a 1 fps; OCR y numpy por CPU; Claude es remoto) | Funciona igual sin NVIDIA. Lo que sí cambia es `doblar` (§2): sin NVIDIA va por **CPU** (o Vulkan en la Iris Xe) y es mucho más lento; doblar y procesar apuntes a la vez en una laptop satura la CPU → usar la cola y dejarlo de noche, enchufada |
| **Tiempos** | ~10,5 min por hora de video | Estimado (no medido): ThinkPad (i7-12ª) parecido o algo mejor; **Surface Pro 6** (4 núcleos, 15 W, se calienta) ~1,5-2× más lento → ~15-20 min por hora de video. La parte de Claude no depende de la laptop |
| **Rutas** | `~/Vídeos` (con tilde, XDG en español), `~/Vídeos/Capturas de YouTube`, `~/Vídeos/Mis cursos.md`, `~/Vídeos/Descargas` | Instalar CachyOS en español para que `xdg-user-dir VIDEOS` = `~/Vídeos` (`xdg-user-dirs-update`). `panel-cursos.py` usa `~/Vídeos` fijo por defecto (`--base`) |
| **Usuario `yafer`** | `abrir-markdown.desktop` tiene `Exec=/home/yafer/...`; `obsidian.json` tiene `/home/yafer/Vídeos` y `/home/yafer/Documentos/Obsidian Vault` | Si el usuario de la laptop se llama distinto, corregir esas rutas. Si `~/Documentos/Obsidian Vault` no existe, sacarla de `obsidian.json` (o dejarla: Obsidian solo la muestra como faltante) |
| **Obsidian** | Bóveda `~/Vídeos` registrada, plugin Spaced Repetition instalado | Copiar `dotfiles/Vídeos/.obsidian/` a `~/Vídeos/.obsidian/` y `obsidian.json` **con Obsidian cerrado** (lo lee solo al arrancar; `pgrep -f obsidian/app.asar`, `pgrep -x obsidian` no lo encuentra). La primera vez: "Confiar en el autor y habilitar plugins" |
| **Carpeta de capturas en vivo** | `carpeta-capturas.conf` → disco externo SuperYafer | Poner `~/Imágenes/Capturas` (ver §3.10) |
| **claude** | `~/.local/bin/claude` con sesión iniciada | Instalar Claude Code con el instalador oficial e **iniciar sesión** con la misma cuenta antes de usar SUPER+ALT+Y/A; si no, los apuntes salen "sin resumen de IA" |
| **Surface** | — | Pantalla 2736×1824: la captura **en vivo** mira toda la pantalla cada segundo → algo de CPU/batería; si va pesado, `INTERVALO=2` |

### 3.10 Reinstalar en la laptop
```bash
sudo pacman -S --needed grim slurp wl-clipboard satty zenity libnotify python-numpy python-pillow \
  python-gobject gtk4 gtk4-layer-shell tesseract tesseract-data-spa tesseract-data-eng ffmpeg yt-dlp obsidian xdg-user-dirs
D=~/migracion-cachyos/dotfiles
cp -a $D/.config/hypr/scripts/. ~/.config/hypr/scripts/        # (o solo los de §3.8 + captura-*.sh)
echo "$HOME/Imágenes/Capturas" > ~/.config/hypr/scripts/carpeta-capturas.conf   # NO la del disco externo
cp -a $D/.config/hypr/config/binds.lua ~/.config/hypr/config/            # SUPER+ALT+S/Y/A
install -Dm644 $D/.local/share/applications/abrir-markdown.desktop ~/.local/share/applications/abrir-markdown.desktop
xdg-mime default abrir-markdown.desktop text/markdown text/x-markdown   # o copiar mimeapps.list
mkdir -p ~/Vídeos && cp -a "$D/Vídeos/.obsidian" ~/Vídeos/                # con Obsidian cerrado
install -Dm644 $D/.config/obsidian/obsidian.json ~/.config/obsidian/obsidian.json   # si Obsidian nunca se abrió; si no, agregar la bóveda desde Obsidian
# Laptop sin monitor vertical (opcional): echo 'export PROGRESO_MONITOR=eDP-1' >> ~/.config/uwsm/env
# Luego correr las pruebas de §3.7 (todas OK)
```
Notas de paquetes:
- **`python-numpy`, `python-pillow`, `python-gobject`**: en la PC están solo como dependencias (de hyprwhspr/piper/etc.). En la laptop instalarlas **explícitamente** o la auto-captura / la barrita no arrancan.
- **`gtk4-layer-shell`**: sin él, la barrita cae a la notificación (sigue funcionando).
- **`tesseract-data-eng`**: en la PC **no está** (solo `spa`); `cuadernillo.py` usa `eng+spa` si están. Como el código de los cursos está en inglés, se recomienda agregarlo en la laptop (mejora opcional; no probado en la PC).
- Probar a mano: SUPER+ALT+S un minuto sobre un video de código; `Ctrl+C` a un link corto de YouTube + SUPER+ALT+Y (debe aparecer la barrita y terminar en "Listo"); doble clic en un `apuntes.md` → se abre en Obsidian; un README fuera de `~/Vídeos` → VS Code.

### Problemas detectados (capturas)
- `carpeta-capturas.conf` apunta a `/run/media/yafer/SuperYafer/paola_v` (disco externo). La auto-captura cae a `~/Imágenes/Capturas` si no se puede escribir, pero **`captura-guardar.sh` no**: si el disco no está montado, **no guarda ni avisa**. En la laptop: resetear el `.conf` (arriba).
- YouTube frena con **HTTP 429** / "no sos un robot" en playlists largas (visto el 28/09 en la de 166 videos): el script espera y reintenta; si persiste, corta y se retoma otro día con el mismo link. Los subtítulos a veces no bajan (429): igual se arman capturas y apuntes con OCR.
- Udemy/Platzi pueden salir en **negro** en la captura en vivo (DRM). No resuelto.
- SUPER+ALT+S/Y/A no chocan con otros atajos en `config/*.lua` (verificado con grep el 28/09).

---

## 4. Sesión de curso, mpv y pomodoro

| Qué | Cómo se lanza | Nota |
|---|---|---|
| Abrir sesión de estudio (`curso-abrir.sh`): hasta 4 "slots" (URL → Brave ventana nueva; ruta → xdg-open; otra cosa → se ejecuta como comando) en el workspace `name:estudio` | **SUPER+C** y tecla 11 del Stream Dock (perfil `Default` de `d6-…AMPGD6`) | Ver doc 01. **Roto a medias**: usa `hyprctl dispatch workspace name:estudio` (sintaxis vieja) → no cambia de workspace con Hyprland Lua. Arreglo: `hyprctl dispatch 'hl.dsp.focus({ workspace = "name:estudio" })'`. SUPER+ALT+E sí va a `estudio`. |
| Configurar slots (`curso-configurar.sh`, zenity) → `curso.conf` | **SUPER+ALT+C** | `curso.conf` hoy tiene un video de YouTube + un Google Doc de apuntes (datos personales de uso; en la laptop se puede reconfigurar) |
| mpv de estudio (`curso.lua`: Alt+c arma la lista con todo el curso y sus módulos; `marcadores.lua`; `velocidad.lua`) | abrir un video | Documentado en doc 04 §5 y `~/.config/mpv/GUIA-MPV.md`. Los `.es.mp4` de `doblar` traen 2 audios: `#` alterna español/inglés |
| Pomodoro (`pomodoro-toggle.sh`): 25 min, notificación al terminar; otro toque cancela | **Solo** tecla 9 del Stream Dock (perfil `IA y Redes` de `99-…293S`); **no tiene atajo de teclado** | En la laptop sin Stream Dock no hay forma de lanzarlo salvo `bash ~/.config/hypr/scripts/pomodoro-toggle.sh`. Si se quiere, agregar un bind (p. ej. `SUPER+ALT+P`, verificar que esté libre). Dep.: `libnotify` |

---

## 5. Otras herramientas de estudio encontradas

- **Lectura en voz alta (SUPER+R) y dictado**: ver doc 02. (El `ResembleAI/chatterbox` de `~/.cache/huggingface` es de la lectura, no del doblaje.)
- **tesseract + tesseract-data-spa** (OCR): desde el 27/09 **los usa `cuadernillo.py`** para leer el código de la pantalla (ver §3). Ya no es opcional si se quieren los apuntes con código real.
- **xournalpp** 1.3.8: instalado, sin uso registrado; interesante para el **lápiz de la Surface** (anotar PDFs/apuntes a mano).
- **Carpetas de trabajo** (texto, se sincronizan como el resto de Documentos; no forman parte de la config):
  - `~/Documentos/aprender/`: notas Markdown del usuario (`funciones.md` = pedidos de funcionalidades y su estado, `lectura.md` = doc técnico de SUPER+R, `Plan-Aprendizaje.md`, `BaseDatos3-Oracle.md`, `Robotica2.md`, `dev/react`…).
  - `~/Documentos/claude_curso/`: el usuario aprende Claude Code; `CURSO_CLAUDE.md` es un cuaderno vivo (su `CLAUDE.md` pide explicar el concepto de Claude Code usado en cada tarea) + proyecto `portafolio/` (Next.js; reinstalar `node_modules` con `npm install`, no copiarlos).
  - `~/Documentos/lectura/lectura.md`: textos para leer con SUPER+R.
- Contexto del usuario (memorias de Claude): estudia cursos de programación (Udemy/YouTube/Platzi) y la carrera; material disperso entre Drive, Obsidian y web; quiere **aprender**, no solo recibir soluciones; los apuntes se basan en capturas.

---

## 6. Resumen de paquetes para esta área (agregar al comando de doc 04)
```bash
sudo pacman -S --needed yt-dlp aria2 ffmpeg python-curl_cffi python-pycryptodomex python-mutagen python-secretstorage \
  python-numpy python-pillow python-gobject gtk4 gtk4-layer-shell grim slurp wl-clipboard satty zenity libnotify \
  tesseract tesseract-data-spa tesseract-data-eng obsidian xdg-user-dirs
# Opcional (ThinkPad, doblar por GPU):  whisper-cpp ggml-vulkan vulkan-intel vulkan-tools
# Opcional:  xournalpp
```
Más el venv de `doblar` (sección 2), el modelo NLLB (2,4 GB) y **Claude Code con sesión iniciada** (lo usan los apuntes).

## 7. Checklist de prueba en la laptop
- [ ] `descargar -s <url youtube>` sin error; `descargar -s <url curso pago>` toma la sesión de Brave.
- [ ] `BORRAR_ORIGINAL=0 doblar prueba.mp4` → `prueba.es.mp4` con 2 audios y 2 subtítulos; anotar cuánto tardó.
- [ ] Las 7 pruebas de §3.7 dan OK.
- [ ] SUPER+ALT+S ON/OFF genera `0001.webp`… + `.minutos.tsv` en `~/Imágenes/Capturas/auto_…`.
- [ ] `Ctrl+C` a un video corto de YouTube + SUPER+ALT+Y → barrita visible (interna o la que diga `PROGRESO_MONITOR`) → "Listo"; en `~/Vídeos/Capturas de YouTube/<título>/` hay `apuntes.md`, `resumen.md`, `tarjetas.md`; `~/Vídeos/Mis cursos.md` lo lista. Anotar minutos por hora de video.
- [ ] Un link de playlist con `MAX_VIDEOS=2` → pregunta "Solo este / Playlist entera"; `cola-capturas.sh estado` muestra la cola.
- [ ] Doble clic en `apuntes.md` → Obsidian (bóveda "Vídeos"); Ctrl+P → "Revisar tarjetas" funciona.
- [ ] CTRL+SHIFT+S guarda en `~/Imágenes/Capturas`; SUPER+SHIFT+S copia; CTRL+SHIFT+D cambia la carpeta.
- [ ] SUPER+C abre los slots **y** cambia al workspace `estudio` (tras el arreglo).
- [ ] mpv: Alt+c arma el curso; `#` cambia de audio en un `.es.mp4`.

## 3.11 Actualización 29-09: Centro de estudio, práctica con tests y subtítulos del idioma original
- **`estudiar.py`** (SUPER+I —antes SUPER+ALT+Z, chocaba con el dictado—, ventana GTK4 `estudiar.centro`, regla flotante en `windowrules.lua`): pre-test de 3 preguntas (3/3 → "ya la sé" `[s]` en `Mis cursos.md`), idea + mapa, ver clase / resumen / apuntes, **práctica** y **tests**, Ctrl+Enter = terminé. CLI `--tests` (SUPER+ALT+V), `--terminar`, `--repasar`, `--estado`, `--siguiente`. Pruebas: `estudiar-tests.py`.
- **`practica.py`**: 3-5 ejercicios (JS con `node:test` / Python con `unittest`), con los tests **verificados** (la solución pasa y el arranque falla). 1 llamada a Claude por clase, solo al pedirla. Pruebas: `practica-tests.py`. En la laptop hace falta `node` ≥ 18.
- **Stream Deck** (Mirabox HSV293S, perfil "Cursos y Dev", teclas 6-9): Estudiar / Tests / Terminé / Repasar (`custom-icons/estudio-*.png`).
- **Subtítulos**: `video-a-capturas.sh` anota el idioma original (`.idioma`) y pide solo esos subtítulos; `cuadernillo.subs_para_claude` le pasa a Claude el idioma original y ya no la traducción automática.
- **yt-dlp**: `~/.config/yt-dlp/config` usa las cookies de Brave (`brave+gnomekeyring`, requiere `python-secretstorage`).
