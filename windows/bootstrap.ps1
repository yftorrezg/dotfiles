# bootstrap.ps1: deja la ThinkPad (Windows 11) como en el repo. Sin permisos de administrador.
# Uso:  pwsh -File bootstrap.ps1  [-SinInstalar]
# Es idempotente: se puede correr las veces que haga falta.
# Lo que necesita administrador está en bootstrap-admin.ps1.
param([switch]$SinInstalar)
$ErrorActionPreference = 'Stop'
$AQUI = $PSScriptRoot
function Paso($m) { Write-Host "`n==> $m" -ForegroundColor Cyan }

# 1. Programas
if (-not $SinInstalar) {
    Paso 'Instalando programas (winget configure)'
    winget configure --file "$AQUI\winget\thinkpad.dsc.yaml" --accept-configuration-agreements --disable-interactivity
}
Paso 'Módulos de Python y PowerShell'
python -m pip install --user --upgrade --quiet edge-tts pillow
if (-not (Get-Module -ListAvailable PSFzf)) { Install-Module PSFzf -Scope CurrentUser -Force -AcceptLicense }

# 2. Variables
[Environment]::SetEnvironmentVariable('PYTHONUTF8', '1', 'User')

# 3. Perfil de PowerShell 7 (una línea que carga el del repo)
Paso 'Perfil de pwsh'
$perfil = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'PowerShell\Microsoft.PowerShell_profile.ps1'
New-Item -ItemType Directory -Force (Split-Path $perfil) | Out-Null
Set-Content $perfil ". `"$AQUI\pwsh\profile.ps1`"" -Encoding utf8

# 4. Windows Terminal: mezcla terminal\wt-ajustes.json sobre settings.json (guarda backup)
Paso 'Windows Terminal'
$wt = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
if (Test-Path $wt) {
    Copy-Item $wt "$wt.bak" -Force
    $s = Get-Content $wt -Raw | ConvertFrom-Json
    $a = Get-Content "$AQUI\terminal\wt-ajustes.json" -Raw | ConvertFrom-Json
    $pwsh = $s.profiles.list | Where-Object { $_.source -eq 'Windows.Terminal.PowershellCore' -or $_.commandline -match 'pwsh' } | Select-Object -First 1
    if ($pwsh) { $s.defaultProfile = $pwsh.guid }
    foreach ($p in $a.globales.PSObject.Properties) { $s | Add-Member -NotePropertyName $p.Name -NotePropertyValue $p.Value -Force }
    $s.profiles | Add-Member -NotePropertyName defaults -NotePropertyValue $a.defaults -Force
    $ids = @($a.actions | ForEach-Object { $_.id })
    $s | Add-Member -NotePropertyName actions -NotePropertyValue (@($s.actions | Where-Object { $_.id -notin $ids }) + $a.actions) -Force
    $s | Add-Member -NotePropertyName keybindings -NotePropertyValue (@($s.keybindings | Where-Object { $_.id -notin $ids }) + $a.keybindings) -Force
    $s | ConvertTo-Json -Depth 20 | Set-Content $wt -Encoding utf8
} else { Write-Warning 'Abre Windows Terminal una vez y vuelve a correr este script.' }

# 5. mpv: unión de directorio (no necesita admin) %APPDATA%\mpv -> repo
Paso 'mpv'
$mpvDst = "$env:APPDATA\mpv"
if ((Test-Path $mpvDst) -and -not ((Get-Item $mpvDst).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
    Rename-Item $mpvDst "mpv.bak-$(Get-Date -Format yyyyMMddHHmmss)"
}
if ((Test-Path $mpvDst) -and (Get-Item $mpvDst).Target -ne "$AQUI\mpv") { (Get-Item $mpvDst).Delete() }   # unión vieja a otra ruta
if (-not (Test-Path $mpvDst)) { New-Item -ItemType Junction -Path $mpvDst -Target "$AQUI\mpv" | Out-Null }
# uosc necesita su binario ziggy para el explorador de archivos; no va en git (pesa ~6 MB).
$ziggy = "$AQUI\mpv\scripts\uosc\bin\ziggy-windows.exe"
if (-not (Test-Path $ziggy)) {
    $zip = Join-Path $env:TEMP 'uosc.zip'
    Invoke-WebRequest 'https://github.com/tomasklaen/uosc/releases/latest/download/uosc.zip' -OutFile $zip
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $z = [IO.Compression.ZipFile]::OpenRead($zip)
    try {
        $e = $z.Entries | Where-Object FullName -like '*uosc/bin/ziggy-windows.exe' | Select-Object -First 1
        New-Item -ItemType Directory -Force (Split-Path $ziggy) | Out-Null
        [IO.Compression.ZipFileExtensions]::ExtractToFile($e, $ziggy, $true)
    } finally { $z.Dispose() }
}

# 5b. ImageGlass: instalar el MSI oficial (la MSIX de winget no se registra como visor), registrarlo y cargar los atajos
Paso 'ImageGlass'
$igExe = "$env:LOCALAPPDATA\Programs\ImageGlass\ImageGlass.exe"
if (-not (Test-Path $igExe)) {
    $ver = '10.0.6.906'
    $msi = Join-Path $env:TEMP "ImageGlass_${ver}_win-x64.msi"
    Invoke-WebRequest "https://github.com/d2phap/ImageGlass/releases/download/$ver/ImageGlass_${ver}_win-x64.msi" -OutFile $msi
    $firma = Get-AuthenticodeSignature $msi
    if ($firma.Status -eq 'Valid' -and $firma.SignerCertificate.Subject -match 'Duong Dieu Phap') {
        Start-Process msiexec.exe -ArgumentList "/i `"$msi`" /passive /norestart" -Wait
    } else { Write-Warning "Firma del MSI no válida ($($firma.Status)): no se instala." }
}
if (Test-Path $igExe) {
    $app = 'HKCU:\Software\Classes\Applications\ImageGlass.exe'
    New-Item -Force "$app\shell\open\command", "$app\SupportedTypes" | Out-Null
    Set-ItemProperty $app -Name FriendlyAppName -Value 'ImageGlass'
    Set-ItemProperty "$app\shell\open\command" -Name '(default)' -Value "`"$igExe`" `"%1`""
    foreach ($e in '.png','.jpg','.jpeg','.webp','.gif','.bmp','.avif','.heic','.tif','.tiff','.ico','.svg') {
        Set-ItemProperty "$app\SupportedTypes" -Name $e -Value ''
        New-Item -Force "HKCU:\Software\Classes\$e\OpenWithList\ImageGlass.exe" | Out-Null
    }
    $cfg = "$env:LOCALAPPDATA\ImageGlass\igconfig.json"
    if ((Test-Path $cfg) -and -not (Get-Process ImageGlass -ErrorAction SilentlyContinue)) {
        $t = [IO.File]::ReadAllText($cfg)
        if ($t.Contains('"MenuHotkeys": {},')) {
            $bloque = (Get-Content "$AQUI\imageglass\menu-hotkeys.json" -Raw).TrimEnd()
            [IO.File]::WriteAllText($cfg, $t.Replace('"MenuHotkeys": {},', '"MenuHotkeys": ' + $bloque + ','), (New-Object Text.UTF8Encoding($false)))
        }
    } else { Write-Warning 'Abre ImageGlass una vez (y ciérralo) y vuelve a correr este script para cargar los atajos.' }
} else { Write-Warning 'ImageGlass (MSI) no está instalado: ver imageglass/README.md' }

# 6. AutoHotkey al iniciar sesión
Paso 'AutoHotkey (inicio)'
$lnk = Join-Path ([Environment]::GetFolderPath('Startup')) 'yafer.ahk.lnk'
$sh = New-Object -ComObject WScript.Shell
$l = $sh.CreateShortcut($lnk); $l.TargetPath = "$AQUI\ahk\yafer.ahk"; $l.WorkingDirectory = "$AQUI\ahk"; $l.Save()

# 7. Arranque más liviano: desactiva (reversible, como el Administrador de tareas) entradas de inicio
Paso 'Aplicaciones de inicio'
$aprob = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run'
$run = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
$desactivar = $run.PSObject.Properties.Name | Where-Object { $_ -match '^(MicrosoftEdgeAutoLaunch|Microsoft\.Lists|OneDrive)' }
New-Item -Force $aprob -ErrorAction SilentlyContinue | Out-Null
foreach ($n in $desactivar) {
    Set-ItemProperty $aprob -Name $n -Value ([byte[]](3,0,0,0,0,0,0,0,0,0,0,0)) -Type Binary
    Write-Host "  desactivado: $n"
}

# 8. Game Bar fuera (libera Win+G para VS Code)
Paso 'Game Bar'
New-Item -Force 'HKCU:\Software\Microsoft\GameBar' -ErrorAction SilentlyContinue | Out-Null
Set-ItemProperty 'HKCU:\Software\Microsoft\GameBar' -Name UseNexusForGameBarEnabled -Value 0 -Type DWord
Set-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\GameDVR' -Name AppCaptureEnabled -Value 0 -Type DWord -ErrorAction SilentlyContinue

# 9. Carpetas de trabajo
New-Item -ItemType Directory -Force "$HOME\Pictures\Capturas", "$HOME\Pictures\Capturas-mpv", "$HOME\Videos\Descargas" | Out-Null

Paso 'Listo. Pasos manuales: ver ATAJOS-WINDOWS.md, sección "Después del bootstrap".'
