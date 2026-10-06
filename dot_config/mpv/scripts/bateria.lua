-- bateria.lua — en la laptop aplica el perfil [bateria] de mpv.conf cuando está
-- desenchufada y lo quita al enchufarla (revisa cada 30 s). Sin cargador conocido
-- (PC de escritorio) no hace nada.

local utils = require "mp.utils"

local function leer(ruta)
    local f = io.open(ruta, "r")
    if not f then return nil end
    local t = f:read("*l")
    f:close()
    return t
end

-- true = con batería, false = enchufada, nil = no hay cargador (PC de escritorio)
local function en_bateria()
    local base = "/sys/class/power_supply"
    local dirs = utils.readdir(base, "dirs") or utils.readdir(base) or {}
    local hay, conectado = false, false
    for _, d in ipairs(dirs) do
        local tipo = leer(base .. "/" .. d .. "/type")
        if tipo == "Mains" or tipo == "USB" then
            hay = true
            if leer(base .. "/" .. d .. "/online") == "1" then conectado = true end
        end
    end
    if not hay then return nil end
    return not conectado
end

local activo = false

local function revisar()
    local b = en_bateria()
    if b == nil then return end
    if b and not activo then
        mp.command("apply-profile bateria")
        activo = true
        mp.msg.info("con batería: perfil [bateria]")
    elseif not b and activo then
        mp.command("apply-profile bateria restore")
        activo = false
        mp.msg.info("enchufada: perfil normal")
    end
end

revisar()
mp.add_periodic_timer(30, revisar)
