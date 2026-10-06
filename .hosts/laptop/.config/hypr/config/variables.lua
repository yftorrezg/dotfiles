-- Hyprland default apps

TERMINAL     = "kitty"
FILE_MANAGER = "dolphin"
BROWSER      = "brave"
EDITOR       = "gnome-text-editor --new-window"
CALCULATOR   = "gnome-calculator"

-- Monitores (LAPTOP ThinkPad E14 Gen4)
-- MONITOR1 = pantalla interna (siempre). El monitor secundario (Arzopa por USB-C = DP-x,
-- o por HDMI = HDMI-A-1) NO se fija aquí: se resuelve en tiempo real con secondaryMonitor()
-- (ver config/escritorios.lua). MONITOR2 queda vacío a propósito.
MONITOR1 = "eDP-1"
MONITOR2 = ""
MONITOR3 = ""
PRIMARY_MONITOR = MONITOR1

-- Escala de la interna 14" 1920x1080 (~157 ppi): 1.25 -> 1536x864 lógicos (valor válido, divide exacto).
-- 1.0 = texto demasiado chico a 157 ppi; 1.5 (lo que elegía "auto") = solo 1280x720 de espacio útil.
INTERNAL_SCALE = 1

-- Si se cierra la tapa con la Arzopa conectada: apagar la interna (todo pasa a la Arzopa).
-- Sin Arzopa, cerrar la tapa suspende (logind) y Noctalia bloquea antes (lock_before_suspend).
TAPA_APAGA_INTERNA = true

-- Workspaces
NUM_WPM = 5 -- Escritorios virtuales (cara principal 1..5, cara secundaria 6..10)
