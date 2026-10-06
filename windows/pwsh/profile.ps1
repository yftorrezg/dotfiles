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
# descargar "url"              mejor calidad (mp4)
# descargar -S "res:720" "url"  máximo 720p
function descargar {
    $destino = Join-Path $HOME 'Videos\Descargas'
    New-Item -ItemType Directory -Force $destino | Out-Null
    yt-dlp -P $destino `
        -o '%(playlist_title&{} - |)s%(playlist_index&{:03d} - |)s%(title)s.%(ext)s' `
        -f 'bv*+ba/b' --merge-output-format mp4 `
        --embed-subs --sub-langs 'es.*,en.*' --embed-metadata `
        --no-overwrites --continue @args
}
