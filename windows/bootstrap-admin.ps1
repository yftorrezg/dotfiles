# bootstrap-admin.ps1: lo que necesita administrador. Correr UNA vez desde una terminal elevada:
#   Start-Process pwsh -Verb RunAs -ArgumentList '-File', "$PWD\bootstrap-admin.ps1"
# Antes: si el disco tiene BitLocker, respalda la clave de recuperación tú mismo
# (Panel de control → Cifrado de unidad BitLocker → Hacer copia de seguridad de la clave).
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'
function Paso($m) { Write-Host "`n==> $m" -ForegroundColor Cyan }

# 1. Punto de restauración ANTES de tocar nada más
Paso 'Punto de restauración'
Enable-ComputerRestore -Drive 'C:\'
Checkpoint-Computer -Description 'Antes de yafer bootstrap' -RestorePointType MODIFY_SETTINGS

# 1b. Habilitar `winget configure` (lo usa bootstrap.ps1 para instalar desde thinkpad.dsc.yaml)
winget configure --enable

# 2. Dev Drive: se crea con el asistente (no requiere Hyper-V):
#    Configuración → Sistema → Almacenamiento → Discos y volúmenes → Crear unidad de desarrollo
#    → Nuevo VHD, 60 GB, dinámico, letra D:, etiqueta "Proyectos". Windows lo vuelve a montar solo.
Paso 'Dev Drive'
if (Test-Path 'D:\') { fsutil devdrv query D: } else { Write-Warning 'Todavía no hay D:. Créalo con el asistente (ver comentario).' ; Start-Process 'ms-settings:disksandvolumes' }

# 3. Energía: "Mejor rendimiento" para el modo actual (enchufado); con batería se elige en Configuración
Paso 'Energía'
powercfg /overlaysetactive OVERLAY_SCHEME_MAX

Write-Host "`nListo. Ahora corre bootstrap.ps1 SIN administrador." -ForegroundColor Green
