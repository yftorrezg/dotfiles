; yafer.ahk: equivalente de binds.lua (Hyprland) para Windows 11 en la ThinkPad E14 Gen4.
; Un solo dueño de las teclas: Stream Deck, MX Master 4 y Mirabox mandan ESTOS atajos.
; Leyenda AHK: # = Win (SUPER), ! = Alt, ^ = Ctrl, + = Shift.
; Cheat sheet: ..\ATAJOS-WINDOWS.md
#Requires AutoHotkey v2.0
#SingleInstance Force
#Include lib\VD.ah2
SetTitleMatchMode 2
A_MenuMaskKey := "vkE8"   ; evita que soltar Win abra Inicio tras un combo

; ---------- Rutas ----------
LOCALDATA    := EnvGet("LOCALAPPDATA")
BRAVE    := FirstExisting(["C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", "C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe", LOCALDATA "\BraveSoftware\Brave-Browser\Application\brave.exe"])
OBSIDIAN := LOCALDATA "\Programs\Obsidian\Obsidian.exe"
VSCODE   := LOCALDATA "\Programs\Microsoft VS Code\Code.exe"
STREAMDECK := "C:\Program Files\Elgato\StreamDeck\StreamDeck.exe"
SCRIPTS  := A_ScriptDir "\..\scripts"
ESTADO   := EnvGet("APPDATA") "\yafer"          ; carpeta-capturas, curso.ini, voz.ini
DirCreate ESTADO
INI      := ESTADO "\yafer.ini"

; ---------- Escritorios (= workspaces 1..5 de Hyprland, una sola pantalla) ----------
; 1 Redes · 2 Facultad · 3 Estudio · 4 Código · 5 Chats
NOMBRES := ["Redes", "Facultad", "Estudio", "Código", "Chats"]
VD.createUntil(5)
for i, n in NOMBRES
    try VD.setNameToDesktopNum(n, i)

FirstExisting(lista) {
    for p in lista
        if FileExist(p)
            return p
    return lista[1]
}

; Enfocar si existe; si no, ir al escritorio fijo (0 = el actual) y abrir.
EnfocarOAbrir(criterio, cmd, escritorio := 0) {
    if hwnd := WinExist(criterio) {
        VD.goToDesktopOfWindow("ahk_id " hwnd)
        WinActivate "ahk_id " hwnd
        return
    }
    if escritorio
        VD.goToDesktopNum(escritorio)
    Run cmd
}

; = app-web.sh: ventanas brave --app=URL (PWA sin pestañas)
AppWeb(titulo, url, escritorio := 0) {
    EnfocarOAbrir(titulo " ahk_exe brave.exe", '"' BRAVE '" --app=' url, escritorio)
}

EsVentanaCerrable() {
    cls := WinGetClass("A")
    return !(cls = "Progman" || cls = "WorkerW" || cls = "Shell_TrayWnd" || cls = "Shell_SecondaryTrayWnd")
}

; ===================== 2.1 Ventanas =====================
#q:: (EsVentanaCerrable() && WinClose("A"))
#d:: (WinGetMinMax("A") = 1 ? WinRestore("A") : WinMaximize("A"))   ; SUPER+D maximizar
#f:: Send "{F11}"                                                     ; SUPER+F pantalla completa
#!Space:: WinSetAlwaysOnTop(-1, "A")                                  ; flotar → "siempre encima" (PiP)

; ===================== 2.2 Lanzadores y apps =====================
#Enter:: Run "wt.exe"
#s:: Send "#``"                                       ; scratchpad = terminal quake de Windows Terminal
#Space:: Send "#!{Space}"                             ; lanzador = PowerToys Command Palette (su atajo por defecto)
#w:: EnfocarOAbrir("ahk_exe brave.exe ahk_class Chrome_WidgetWin_1", '"' BRAVE '"')
#n:: EnfocarOAbrir("ahk_exe Obsidian.exe", '"' OBSIDIAN '"')
#g:: EnfocarOAbrir("ahk_exe Code.exe", '"' VSCODE '"', 4)
#k:: EnfocarOAbrir("ahk_exe StreamDeck.exe", '"' STREAMDECK '"')
#t::  AppWeb("TikTok",    "https://www.tiktok.com", 1)
#!q:: AppWeb("YouTube",   "https://www.youtube.com")
#!w:: AppWeb("WhatsApp",  "https://web.whatsapp.com", 5)
#!t:: AppWeb("Telegram",  "https://web.telegram.org", 5)
#!f:: AppWeb("Facebook",  "https://www.facebook.com", 1)
#!i:: AppWeb("Instagram", "https://www.instagram.com", 1)
#!d:: AppWeb("Drive",     "https://drive.google.com")
; Solo para Stream Deck / Actions Ring (sin tecla física asignada en Hyprland):
#^!g:: AppWeb("Gemini",     "https://gemini.google.com")
#^!c:: AppWeb("Claude",     "https://claude.ai")
#^!n:: AppWeb("NotebookLM", "https://notebooklm.google.com")
#^!d:: AppWeb("DeepSeek",   "https://chat.deepseek.com")

; ===================== 2.6 Escritorios =====================
#1:: VD.goToDesktopNum(1)
#2:: VD.goToDesktopNum(2)
#3:: VD.goToDesktopNum(3)
#4:: VD.goToDesktopNum(4)
#5:: VD.goToDesktopNum(5)
#^1:: VD.MoveWindowToDesktopNum("A", 1)
#^2:: VD.MoveWindowToDesktopNum("A", 2)
#^3:: VD.MoveWindowToDesktopNum("A", 3)
#^4:: VD.MoveWindowToDesktopNum("A", 4)
#^5:: VD.MoveWindowToDesktopNum("A", 5)
#WheelDown:: VD.goToRelativeDesktopNum(-1)
#WheelUp::   VD.goToRelativeDesktopNum(+1)
#!e:: VD.goToDesktopNum(3)                            ; ir a "estudio"
; Win+Ctrl+←/→ (escritorio anterior/siguiente) es nativo: el Stream Deck lo usa.

; ===================== 2.5 Capturas y voz =====================
CarpetaCapturas() {
    c := IniRead(INI, "capturas", "carpeta", EnvGet("USERPROFILE") "\Pictures\Capturas")
    DirCreate c
    return c
}

; Las apps de la facultad conservan Ctrl+Shift+S / Ctrl+Shift+D (editar la lista acá).
GroupAdd "Facultad", "ahk_exe WINWORD.EXE"
GroupAdd "Facultad", "ahk_exe EXCEL.EXE"
GroupAdd "Facultad", "ahk_exe POWERPNT.EXE"
GroupAdd "Facultad", "ahk_exe Erstudio.exe"
#HotIf !WinActive("ahk_group Facultad")
^+s:: CapturaEstudio()
^+d:: ElegirCarpeta()
#HotIf

; Región → carpeta de estudio + portapapeles (usa Recortes nativo, Win+Shift+S).
CapturaEstudio() {
    A_Clipboard := ""
    Send "#+s"
    if !ClipWait(30, 1)
        return
    destino := CarpetaCapturas() "\" FormatTime(, "yyyy-MM-dd_HH-mm-ss") ".png"
    RunWait 'pythonw "' SCRIPTS '\guardar-captura.pyw" "' destino '"', , "Hide"
    if FileExist(destino)
        TrayTip "Captura guardada", destino, "Mute"
}

ElegirCarpeta() {
    if c := DirSelect("*" CarpetaCapturas(), 3, "Carpeta para las capturas de estudio (Ctrl+Shift+S)")
        IniWrite c, INI, "capturas", "carpeta"
}

; SUPER+R: leer selección en voz alta (apretar otra vez = cortar).
#r:: LeerSeleccion()
LeerSeleccion() {
    pidfile := A_Temp "\leer-seleccion.pid"
    if FileExist(pidfile) {
        pid := Trim(FileRead(pidfile))
        FileDelete pidfile
        if pid && ProcessExist(pid) {
            ProcessClose pid
            try ProcessClose "ffplay.exe"
            return
        }
    }
    guardado := ClipboardAll()
    A_Clipboard := ""
    ; En la terminal Ctrl+C corta el proceso: ahí se copia con Ctrl+Shift+C.
    Send WinActive("ahk_exe WindowsTerminal.exe") ? "^+c" : "^c"
    ok := ClipWait(0.4)
    texto := A_Clipboard
    A_Clipboard := guardado
    if !ok || Trim(texto) = ""
        return TrayTip("Leer", "No hay texto seleccionado", "Mute")
    archivo := A_Temp "\leer-seleccion.txt"
    try FileDelete archivo
    FileAppend texto, archivo, "UTF-8"
    Run 'pythonw "' SCRIPTS '\leer-seleccion.pyw" "' archivo '" "' INI '"', , "Hide", &pid
    FileAppend pid, pidfile
}

; SUPER+ALT+R: elegir voz y velocidad.
#!r:: ElegirVoz()
ElegirVoz() {
    voces := ["es-AR-ElenaNeural", "es-AR-TomasNeural", "es-MX-DaliaNeural", "es-MX-JorgeNeural", "es-ES-ElviraNeural", "es-US-PalomaNeural", "en-US-AriaNeural", "en-US-GuyNeural"]
    actual := IniRead(INI, "voz", "voz", "es-AR-ElenaNeural")
    vel := IniRead(INI, "voz", "velocidad", "40")
    g := Gui("+AlwaysOnTop", "Voz para SUPER+R")
    g.SetFont("s10")
    g.AddText(, "Voz (edge-tts):")
    dd := g.AddDropDownList("w260 Choose" Max(1, IndexOf(voces, actual)), voces)
    g.AddText(, "Velocidad (+%):")
    sl := g.AddSlider("w260 Range-20-100 TickInterval10 ToolTip", vel)
    g.AddButton("Default w120", "Guardar").OnEvent("Click", (*) => (IniWrite(dd.Text, INI, "voz", "voz"), IniWrite(sl.Value, INI, "voz", "velocidad"), g.Destroy()))
    g.Show()
}
IndexOf(arr, v) {
    for i, x in arr
        if x = v
            return i
    return 0
}

; ===================== Sesión de curso (SUPER+C / SUPER+ALT+C) =====================
#c:: CursoAbrir()
#!c:: CursoConfigurar()
CursoAbrir() {
    VD.goToDesktopNum(3)
    abierto := false
    loop 4 {
        v := Trim(IniRead(INI, "curso", "slot" A_Index, ""))
        if v = ""
            continue
        abierto := true
        if RegExMatch(v, "i)^https?://")
            Run '"' BRAVE '" --new-window ' v
        else
            Run v
    }
    if !abierto
        CursoConfigurar()
}
CursoConfigurar() {
    g := Gui("+AlwaysOnTop", "Curso actual (SUPER+C)")
    g.SetFont("s10")
    campos := []
    loop 4 {
        g.AddText(, "Slot " A_Index " (URL, archivo, carpeta o comando):")
        campos.Push(g.AddEdit("w520", IniRead(INI, "curso", "slot" A_Index, "")))
    }
    g.AddButton("Default w120", "Guardar").OnEvent("Click", Guardar)
    g.Show()
    Guardar(*) {
        for i, c in campos
            IniWrite c.Value, INI, "curso", "slot" i
        g.Destroy()
    }
}

; ===================== Utilidades =====================
#!F5:: Reload                                         ; recargar este script
