-- Hyprland default apps

TERMINAL     = "kitty"
FILE_MANAGER = "dolphin"
BROWSER      = "brave"
EDITOR       = "gnome-text-editor --new-window"
CALCULATOR   = "gnome-calculator"

-- Monitors
-- El nombre del puerto DisplayPort cambia segun el conector fisico (DP-2, DP-3...):
-- se detecta el que este conectado; si no se puede, cae a DP-3.
MONITOR1 = "DP-3"      -- yodoit 15.6" (horizontal, principal)
do
    local ok, mons = pcall(hl.get_monitors)
    if ok and mons then
        for _, m in ipairs(mons) do
            if m.name:match("^DP%-%d+$") then MONITOR1 = m.name break end
        end
    end
end
MONITOR2 = "HDMI-A-1"  -- yodoit 15.6" (vertical, secundario)
MONITOR3 = ""
PRIMARY_MONITOR = MONITOR1

-- Workspaces
NUM_WPM = 5 -- Number of workspaces per monitor (Max 10)
