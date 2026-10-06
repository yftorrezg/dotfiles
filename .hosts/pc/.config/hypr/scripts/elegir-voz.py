#!/usr/bin/env python3
"""SUPER+ALT+R: elegir voz de lectura y velocidad en una sola ventanita.
Reemplaza los 2 diálogos de zenity por un popup GTK4/libadwaita.
Escribe ENGINE/VOICE/SPEED_MULT en voz.conf, igual que antes.
"""
import gi
import os
import subprocess

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, GLib

CONFIG = os.path.expanduser("~/.config/hypr/scripts/voz.conf")

VOICES = [
    {"label": "Argentina — Elena", "sub": "edge-tts · online · natural",
     "engine": "edge", "voice": "es-AR-ElenaNeural"},
    {"label": "México — Jorge", "sub": "edge-tts · online · natural",
     "engine": "edge", "voice": "es-MX-JorgeNeural"},
    {"label": "Argentina — Daniela", "sub": "Piper · offline · privado",
     "engine": "piper", "voice": "/usr/share/piper-voices/es/es_AR/daniela/high/es_AR-daniela-high.onnx"},
    {"label": "México — Claude", "sub": "Piper · offline · privado",
     "engine": "piper", "voice": "/usr/share/piper-voices/es/es_MX/claude/high/es_MX-claude-high.onnx"},
    {"label": "Privada — Chatterbox", "sub": "offline · máxima calidad · más lenta",
     "engine": "chatterbox", "voice": "es-mx-latam"},
]


def read_current():
    engine, voice, speed = "edge", "es-AR-ElenaNeural", 1.0
    if os.path.isfile(CONFIG):
        vals = {}
        with open(CONFIG) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    vals[k] = v
        engine = vals.get("ENGINE", engine)
        voice = vals.get("VOICE", voice)
        try:
            speed = float(vals.get("SPEED_MULT", speed))
        except ValueError:
            pass
    return engine, voice, speed


def current_index(engine, voice):
    for i, v in enumerate(VOICES):
        if v["engine"] == engine and v["voice"] == voice:
            return i
    return 0


class VoicePicker(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Voz de lectura")
        self.set_default_size(440, 0)
        self.set_resizable(False)
        self.set_modal(True)

        cur_engine, cur_voice, cur_speed = read_current()
        self.selected = current_index(cur_engine, cur_voice)

        toolbar = Adw.ToolbarView()
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        header.set_show_start_title_buttons(False)
        toolbar.add_top_bar(header)

        clamp = Adw.Clamp(maximum_size=440)
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        outer.set_margin_top(6)
        outer.set_margin_bottom(18)
        outer.set_margin_start(18)
        outer.set_margin_end(18)
        clamp.set_child(outer)
        toolbar.set_content(clamp)
        self.set_content(toolbar)

        voice_group = Adw.PreferencesGroup(title="Voz")
        first_radio = None
        self.rows = []
        for i, v in enumerate(VOICES):
            row = Adw.ActionRow(title=v["label"], subtitle=v["sub"])
            radio = Gtk.CheckButton()
            if first_radio is None:
                first_radio = radio
            else:
                radio.set_group(first_radio)
            radio.set_active(i == self.selected)
            radio.set_valign(Gtk.Align.CENTER)
            row.add_prefix(radio)
            row.set_activatable_widget(radio)
            radio.connect("toggled", self._on_voice_toggled, i)
            voice_group.add(row)
            self.rows.append(radio)
        outer.append(voice_group)

        speed_group = Adw.PreferencesGroup(title="Velocidad")
        speed_row = Adw.ActionRow()
        speed_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        speed_box.set_margin_top(8)
        speed_box.set_margin_bottom(8)

        self.speed_value_label = Gtk.Label(label=f"{cur_speed:.1f}x")
        self.speed_value_label.add_css_class("title-4")
        self.speed_value_label.set_halign(Gtk.Align.CENTER)
        speed_box.append(self.speed_value_label)

        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1.0, 3.0, 0.1)
        self.scale.set_value(cur_speed)
        self.scale.set_draw_value(False)
        self.scale.set_hexpand(True)
        for mark in (1.0, 1.5, 2.0, 2.5, 3.0):
            self.scale.add_mark(mark, Gtk.PositionType.BOTTOM, f"{mark:g}x")
        self.scale.connect("value-changed", self._on_speed_changed)
        speed_box.append(self.scale)

        hint = Gtk.Label(
            label="1.0x normal para estudiar · 1.8x rápida para repasar",
            wrap=True,
        )
        hint.add_css_class("caption")
        hint.add_css_class("dim-label")
        hint.set_halign(Gtk.Align.CENTER)
        speed_box.append(hint)

        speed_row.set_child(speed_box)
        speed_group.add(speed_row)
        outer.append(speed_group)

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_box.set_halign(Gtk.Align.END)
        cancel_btn = Gtk.Button(label="Cancelar")
        cancel_btn.connect("clicked", lambda _b: self.close())
        apply_btn = Gtk.Button(label="Aplicar")
        apply_btn.add_css_class("suggested-action")
        apply_btn.connect("clicked", self._on_apply)
        btn_box.append(cancel_btn)
        btn_box.append(apply_btn)
        outer.append(btn_box)

        key_ctrl = Gtk.EventControllerKey()
        key_ctrl.connect("key-pressed", self._on_key)
        self.add_controller(key_ctrl)

        self.set_default_widget(apply_btn)

    def _on_voice_toggled(self, radio, index):
        if radio.get_active():
            self.selected = index

    def _on_speed_changed(self, scale):
        self.speed_value_label.set_label(f"{scale.get_value():.1f}x")

    def _on_key(self, _ctrl, keyval, _keycode, _state):
        if keyval == 65307:  # Escape
            self.close()
            return True
        return False

    def _on_apply(self, _btn):
        chosen = VOICES[self.selected]
        speed = round(self.scale.get_value(), 1)
        engine, voice, label = chosen["engine"], chosen["voice"], chosen["label"]

        with open(CONFIG, "w") as f:
            f.write(f"ENGINE={engine}\n")
            f.write(f"VOICE={voice}\n")
            f.write(f"SPEED_MULT={speed}\n")

        if engine == "chatterbox" and speed != 1.0:
            body = f"{label} — Chatterbox no soporta ajustar velocidad, se ignora ese valor"
        else:
            body = f"{label} — velocidad {speed}x"
        subprocess.run(
            ["notify-send", "-t", "2500", "Voz de lectura actualizada", body],
            check=False,
        )
        self.close()


class VoicePickerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="ar.hypr.elegirvoz")

    def do_activate(self):
        win = VoicePicker(self)
        win.present()


if __name__ == "__main__":
    app = VoicePickerApp()
    app.run(None)
