# Perfil de PowerShell 7: lo mismo que cachyos-fish-config + mis funciones, en Windows.
# Lo enlaza bootstrap.ps1 a $PROFILE (Documents\PowerShell\Microsoft.PowerShell_profile.ps1).

$env:PYTHONUTF8 = '1'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

# --- Historial y predicción (como el autosuggest de fish) ---
if ((Get-Module -ListAvailable PSReadLine) -and -not [Console]::IsOutputRedirected) {
    Set-PSReadLineOption -HistoryNoDuplicates -EditMode Windows
    try { Set-PSReadLineOption -PredictionSource History -PredictionViewStyle InlineView } catch { }
    Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
    Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
    Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
    Set-PSReadLineKeyHandler -Key RightArrow -Function ForwardChar   # acepta la sugerencia
}

# --- Prompt y navegación ---
if (Get-Command starship -ErrorAction SilentlyContinue) { Invoke-Expression (& starship init powershell) }
if (Get-Command zoxide -ErrorAction SilentlyContinue)   { Invoke-Expression (& { (zoxide init powershell | Out-String) }) }

# fzf: Ctrl+R historial, Ctrl+T archivos (requiere el módulo PSFzf)
if ((Get-Command fzf -ErrorAction SilentlyContinue) -and (Get-Module -ListAvailable PSFzf)) {
    Import-Module PSFzf
    Set-PsFzfOption -PSReadlineChordProvider 'Ctrl+t' -PSReadlineChordReverseHistory 'Ctrl+r'
    $env:FZF_DEFAULT_COMMAND = 'fd --type f --hidden --exclude .git'
}

# --- Alias al estilo de fish ---
if (Get-Command eza -ErrorAction SilentlyContinue) {
    Remove-Item Alias:ls -Force -ErrorAction SilentlyContinue
    function ls  { eza --icons --group-directories-first @args }
    function ll  { eza -l --icons --git --group-directories-first @args }
    function la  { eza -la --icons --git --group-directories-first @args }
    function lt  { eza --tree --level=2 --icons @args }
}
if (Get-Command bat -ErrorAction SilentlyContinue) {
    Remove-Item Alias:cat -Force -ErrorAction SilentlyContinue
    function cat { bat --paging=never --style=plain @args }
}
function ..   { Set-Location .. }
function ...  { Set-Location ../.. }
function which($c) { (Get-Command $c).Source }
function touch($f) { if (Test-Path $f) { (Get-Item $f).LastWriteTime = Get-Date } else { New-Item -ItemType File $f | Out-Null } }
function mkcd($d) { New-Item -ItemType Directory -Force $d | Out-Null; Set-Location $d }
function recargar { . $PROFILE }

# --- descargar: videos, playlists y cursos (= ~/.local/bin/descargar de CachyOS) ---
#   descargar "url"                  mejor calidad (mp4) -> Videos\Descargas
#   descargar --mp3 "url"            solo audio en mp3   -> Music\Descargas
#   descargar -S "res:720" "url"     máximo 720p (cualquier opción de yt-dlp se pasa tal cual)
# Variables opcionales: $env:NAVEGADOR = 'brave'|'firefox'|'chrome' (usar su sesión, cierra el
# navegador antes: Chrome/Brave cifran las cookies en Windows y pueden fallar), $env:DESTINO = carpeta.
function descargar {
    if (-not $args) { Write-Host 'Uso: descargar <url> [url2 ...]   |   descargar --mp3 <url>'; return }
    $audio = $false; $extra = @()
    foreach ($a in $args) {
        if ($a -eq '--mp3') { $audio = $true }
        elseif ($a -in '-x', '--extract-audio') { $audio = $true; $extra += $a }
        else { $extra += $a }
    }
    $base = if ($audio) { [Environment]::GetFolderPath('MyMusic') } else { [Environment]::GetFolderPath('MyVideos') }
    $destino = if ($env:DESTINO) { $env:DESTINO } else { Join-Path $base 'Descargas' }
    New-Item -ItemType Directory -Force $destino | Out-Null
    $opts = @(
        '-P', $destino,
        '-o', '%(playlist_title|.)s/%(playlist_index&{:03d} - |)s%(title)s.%(ext)s',
        '--embed-metadata', '--embed-thumbnail',
        '--download-archive', (Join-Path $destino '.descargados.txt'),
        '--ignore-errors', '--no-overwrites', '--continue'
    )
    if ($audio) { $opts += '-f', 'ba/b', '-x', '--audio-format', 'mp3', '--audio-quality', '0' }
    else        { $opts += '-f', 'bv*+ba/b', '--merge-output-format', 'mp4', '--write-subs', '--sub-langs', 'es.*,en.*', '--embed-subs' }
    if ($env:NAVEGADOR) { $opts += '--cookies-from-browser', $env:NAVEGADOR }
    if (Get-Command aria2c -ErrorAction SilentlyContinue) { $opts += '--downloader', 'aria2c', '--downloader-args', 'aria2c:-x 8 -s 8 -k 1M' }
    yt-dlp @opts @extra
}
