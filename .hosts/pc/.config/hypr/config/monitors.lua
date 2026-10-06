-- Monitor wiki https://wiki.hypr.land/Configuring/Basics/Monitors/
-- Example: output can be found with hyprctl monitors. Edit variables.lua for the monitor outputs instead of here directly
-- hl.monitor({
--     output    = "MONITOR1",
--     mode      = "1920x1080@60",
--     position  = "0x0",
--     scale     = "1",
-- })

-- Puente con nwg-displays (launcher override en
-- ~/.local/share/applications/nwg-displays.desktop le pasa -m para que
-- escriba acá en vez de ~/.config/hypr/monitors.conf, que nadie lee).
-- Si existe, se usa esa config; si no, cae al fallback fijo de abajo.
local function parse_nwg_monitors(path)
    local f = io.open(path, "r")
    if not f then return nil end

    local specs, order = {}, {}
    for line in f:lines() do
        local rest = line:match("^%s*monitor%s*=%s*(.-)%s*$")
        if rest then
            local fields = {}
            for field in (rest .. ","):gmatch("(.-),") do
                fields[#fields + 1] = field
            end
            local name = fields[1]
            if not specs[name] then
                specs[name] = { output = name }
                order[#order + 1] = name
            end
            local spec = specs[name]
            if fields[2] == "transform" then
                spec.transform = tonumber(fields[3])
            elseif fields[2] == "disable" then
                spec.disabled = true
            else
                spec.mode = fields[2]
                spec.position = fields[3]
                spec.scale = tonumber(fields[4]) or fields[4]
                local i = 5
                while fields[i] do
                    local key, val = fields[i], fields[i + 1]
                    if key == "vrr" then spec.vrr = tonumber(val)
                    elseif key == "transform" then spec.transform = tonumber(val)
                    elseif key == "bitdepth" then spec.bitdepth = tonumber(val)
                    elseif key == "mirror" then spec.mirror = val
                    end
                    i = i + 2
                end
            end
        end
    end
    f:close()
    return specs, order
end

local nwg_path = os.getenv("HOME") .. "/.config/hypr/config/nwg-monitors.conf"
local specs, order = parse_nwg_monitors(nwg_path)

if specs then
    for _, name in ipairs(order) do
        hl.monitor(specs[name])
    end
else
    -- Fallback manual (primer arranque, antes de usar nwg-displays alguna vez)
    -- yodoit vertical (rotado 90°), a la izquierda
    hl.monitor({
        output    = "HDMI-A-1",
        mode      = "1920x1080@60",
        position  = "0x0",
        scale     = "1",
        transform = 1,
    })

    -- yodoit horizontal, a la derecha del vertical (alineado arriba con el vertical)
    hl.monitor({
        output    = "DP-3",
        mode      = "1920x1080@60",
        position  = "1080x0",
        scale     = "1",
    })
end

-- Fallback para cualquier otro monitor que se conecte (no HDMI-A-1 ni DP-2)
hl.monitor({
    output    = "",
    mode      = "preferred",
    position  = "auto",
    scale     = "auto",
})
