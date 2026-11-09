#!/usr/bin/env python3
"""Regenera apuntes de un curso completo con el modelo Free de OpenCode (sin gastar cuota).

Por clase: transcripción + OCR de capturas + recursos → prompt v5 → JSON validado →
.apuntes-ia.json, .resumen-ia.json, apuntes.md, resumen.md y tarjetas (conserva progreso SR).
Respaldos en .antes-regeneracion/. Cero imágenes en los apuntes.

    regenerar-curso.py <carpeta-del-curso> [--limite N] [--solo "texto"] [--ver]

--ver: solo lista las clases y la estimación, sin llamar a la IA.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# Motor Free: se configura ANTES de importar cuadernillo (lee las constantes al importar).
os.environ.setdefault('APUNTES_MOTOR', 'opencode')
os.environ.setdefault('APUNTES_MODELO_OPENCODE', 'opencode/deepseek-v4.1-flash-free')
os.environ.setdefault('APUNTES_RESPALDO', '')  # nunca caer a cuota de Claude

SCRIPTS = Path.home() / '.config/hypr/scripts'
sys.path.insert(0, str(SCRIPTS))
import cuadernillo as cu  # noqa: E402

INTENTOS = 3
MAX_OCR = 25
MAX_OCR_CHARS = 1200
LOG = None
RESULTADO = None


def decir(*a):
    print(*a, flush=True)
    if LOG:
        LOG.write(' '.join(str(x) for x in a) + '\n')
        LOG.flush()


def leer_ocr(clase):
    """[(segundo, texto)] del OCR ya guardado, sin rehacer OCR. Filtra basura y limita."""
    ruta = clase / '.ocr-capturas.json'
    if not ruta.is_file():
        return []
    try:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return []
    tiempos = {}
    minutos = clase / '.minutos.tsv'
    if minutos.is_file():
        for linea in minutos.read_text(encoding='utf-8').splitlines():
            f, sep, t = linea.partition('\t')
            if sep:
                try:
                    tiempos[Path(f).name] = cu.a_segundos(t)
                except ValueError:
                    pass
    pantallas = []
    for nombre, texto in datos.items():
        texto = ' '.join(str(texto or '').split())
        alfa = sum(c.isalnum() for c in texto)
        if alfa < 40 or alfa / max(1, len(texto)) < 0.45:
            continue  # OCR ilegible: mejor no meter ruido
        pantallas.append((tiempos.get(Path(nombre).name, 0), texto[:MAX_OCR_CHARS]))
    pantallas.sort()
    if len(pantallas) > MAX_OCR:
        paso = len(pantallas) / MAX_OCR
        pantallas = [pantallas[int(i * paso)] for i in range(MAX_OCR)]
    return pantallas


def cues_de_transcripcion(clase):
    """Si no hay subtítulos, convierte transcripcion.md (líneas `0:00` texto) en cues."""
    ruta = clase / 'transcripcion.md'
    if not ruta.is_file():
        return []
    cues = []
    for linea in ruta.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^`(\d+(?::\d+){1,2})`\s*(.+)$', linea.strip())
        if m:
            try:
                cues.append((cu.a_segundos(m.group(1)), m.group(2).strip()))
            except ValueError:
                pass
    return cues


REGLAS = """

REGLAS EXTRA DE ESTA REGENERACIÓN (tienen prioridad sobre el estilo si hay conflicto):
- Presente atemporal e impersonal: "se configura", "hay que", "usa". Prohibido narrar al profesor
  ("el profesor muestra/hace/dice") salvo para advertir de un límite o error del material.
- Todo procedimiento de 3+ pasos o flujo de ataque/defensa lleva un diagrama Mermaid simple y correcto,
  con nodos de decisión cuando haya condiciones.
- Si hay dos o más herramientas, redes, cifrados o alternativas, incluye una tabla comparativa con
  criterios de decisión; no una lista de definiciones.
- Comenta con 👉 cada línea de código no obvia; no dejes comandos sin explicar. Si un comando del
  material es incorrecto o parcial, dilo.
- Cada punto aporta un dato, un porqué o un paso. Nada de relleno, transiciones ni "en esta clase".
- Cuida la concordancia ("1 ejercicio", "2 ejercicios") y evita repetir la idea en varios campos.
- En "corto.esencial" no repitas la idea: añade los pasos imprescindibles.
- NUNCA respondas "sin_contenido" si hay transcripción, OCR o recursos: siempre hay al menos un concepto,
  una advertencia o un paso que rescatar. "sin_contenido" es solo para clases mudas o puro relleno.
- Usa el APUNTE ACTUAL como esqueleto: conserva sus aciertos (diagramas, tablas, ejemplos, correcciones),
  verifica cada afirmación contra la transcripción/OCR y elimina relleno. No lo copies tal cual.
- Si el APUNTE ACTUAL contiene una precisión técnica que la transcripción no repite (por ejemplo, una
  condición TLS), CONSÉRVALA: fue una corrección validada. No la borres por no estar literal en el audio.
"""


def armar_prompt(clase, titulo, duracion, cues, pantallas, codigo, previo=""):
    lineas = [f"[{cu.hms(t)}] {txt}" for t, txt in cu.parrafos(cues, cada=30)]
    if lineas:
        transcripcion = "Transcripción con marcas de tiempo [h:mm:ss]:\n<<<\n" + "\n".join(lineas) + "\n>>>\n"
    else:
        transcripcion = "(No hay transcripción del audio: arma los apuntes con lo que se ve en pantalla.)\n"
    extra = ""
    if pantallas:
        extra = ("\nTexto leído de la PANTALLA (OCR, puede tener errores de lectura) en algunos momentos;"
                 " sirve para el código exacto y los datos que se ven:\n<<<\n"
                 + "\n\n".join(f"[{cu.hms(t)}]\n{txt}" for t, txt in pantallas) + "\n>>>\n")
    if codigo:
        extra += f"\nMaterial que entrega el curso (recursos.py):\n<<<\n{codigo}\n>>>\n"
    if previo:
        extra += ("\nAPUNTE ACTUAL (material de partida: puede tener errores; verifica y conserva lo correcto):\n<<<\n"
                  + previo[:7000] + "\n>>>\n")
    return cu.PROMPT.format(titulo=titulo, duracion=cu.hms(duracion),
                            n_preg=cu.n_preguntas(duracion), n_pre=cu.n_pretest(duracion),
                            n_ejer=cu.n_ejercicios(duracion), n_err=cu.n_errores(duracion),
                            n_diag=cu.n_diagramas(duracion), n_voc=cu.n_vocabulario(duracion),
                            tope=cu.tope_palabras(duracion), rango_diag=cu.rango_diagramas(duracion),
                            transcripcion=transcripcion,
                            pantallas=extra) + REGLAS


def json_valido(texto):
    try:
        datos = json.loads(texto[texto.index('{'):texto.rindex('}') + 1])
    except (ValueError, TypeError):
        return None
    if not isinstance(datos, dict) or datos.get('sin_contenido'):
        return datos if isinstance(datos, dict) else None
    secciones = datos.get('secciones')
    if not secciones or not all(isinstance(s, dict) and s.get('titulo') for s in secciones):
        return None
    if not isinstance(datos.get('corto'), dict) or not datos['corto'].get('idea'):
        return None
    return datos


def respaldar(clase):
    destino = clase / '.antes-regeneracion'
    destino.mkdir(exist_ok=True)
    for nombre in ('apuntes.md', 'resumen.md', 'tarjetas.md', 'tarjetas-anki.txt', 'transcripcion.md',
                   '.apuntes-ia.json', '.resumen-ia.json'):
        origen = clase / nombre
        if origen.is_file() and not (destino / nombre).exists():
            (destino / nombre).write_bytes(origen.read_bytes())


def restaurar(clase):
    """Vuelve al apunte previo si la regeneración salió peor (el respaldo no se toca)."""
    destino = clase / '.antes-regeneracion'
    for nombre in ('apuntes.md', 'resumen.md', 'tarjetas.md', 'tarjetas-anki.txt', 'transcripcion.md',
                   '.apuntes-ia.json', '.resumen-ia.json'):
        if (destino / nombre).is_file():
            (clase / nombre).write_bytes((destino / nombre).read_bytes())


def regenerar(clase):
    clase = Path(clase)
    apunte = clase / 'apuntes.md'
    if not apunte.is_file():
        return 'sin apuntes'
    texto_apunte = apunte.read_text(encoding='utf-8')
    titulo = texto_apunte.splitlines()[0]
    titulo = titulo.removeprefix('# 📓 ').removeprefix('# ').strip() or clase.name
    duracion = cu.editorial.duracion_guardada(str(clase))
    subs = cu.buscar_subtitulos(str(clase), None)
    cues = cu.subs_para_claude(str(clase), subs) or cues_de_transcripcion(clase)
    pantallas = leer_ocr(clase)
    recursos = clase / '.recursos.md'
    codigo = recursos.read_text(encoding='utf-8') if recursos.is_file() else ''
    prompt = armar_prompt(clase, titulo, duracion, cues, pantallas, codigo, previo=texto_apunte)
    datos = None
    for intento in range(1, INTENTOS + 1):
        t0 = time.time()
        texto = cu.consultar_ia(prompt)
        datos = json_valido(texto or '')
        if datos is not None and datos.get('sin_contenido'):
            # el modelo a veces se rinde: si hay material, no se acepta un borrado
            if len(' '.join(t for _, t in cues)) > 400 or pantallas or codigo.strip():
                decir('    dijo "sin contenido" pero hay material: reintento')
                datos = None
                continue
        if datos is not None and (datos.get('sin_contenido') or datos.get('secciones')):
            decir(f'    respuesta válida en {time.time()-t0:.0f}s (intento {intento})')
            break
        decir(f'    respuesta inválida (intento {intento}/{INTENTOS})')
        datos = None
    if datos is None:
        return 'error: sin JSON válido (se conserva)'
    if datos.get('sin_contenido'):
        return 'sin contenido real (se conserva el apunte)'
    respaldar(clase)
    corto = datos.get('corto') or {}
    capturas = cu.elegir_capturas(str(clase))
    md = cu.armar(str(clase), titulo, capturas, subs, datos, duracion, codigo)
    palabras = len(re.findall(r'\w+', md))
    p_previo = len(re.findall(r'\w+', texto_apunte))
    if p_previo >= 150 and (palabras < 0.6 * p_previo or
                            ('```mermaid' in texto_apunte and '```mermaid' not in md
                             and palabras < 0.85 * p_previo)):
        restaurar(clase)
        return f'conservado: el nuevo era peor ({palabras} vs {p_previo} palabras)'
    (clase / '.apuntes-ia.json').write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding='utf-8')
    (clase / '.resumen-ia.json').write_text(json.dumps(corto, ensure_ascii=False, indent=1), encoding='utf-8')
    apunte.write_text(md, encoding='utf-8')
    if corto.get('idea'):
        rc = cu.cargar_resumen_corto()
        (clase / 'resumen.md').write_text(rc.armar(titulo, cu.hms(duracion), corto, con_preguntas=False), encoding='utf-8')
    subprocess.run([sys.executable, str(SCRIPTS / 'tarjetas.py'), str(clase), '--forzar'],
                   capture_output=True, text=True, timeout=180)
    return f'ok: {palabras} palabras, {len(datos.get("secciones") or [])} secciones'


def clases(base):
    base = Path(base)
    for n in ('Apuntes', 'capturas'):  # v10: Apuntes/ (antes capturas/)
        if (base / n).is_dir() and base.name not in ('Apuntes', 'capturas'):
            base = base / n
            break
    return sorted(d for d in base.iterdir() if d.is_dir() and (d / '.apuntes-ia.json').is_file())


def main():
    global LOG, RESULTADO
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('curso')
    p.add_argument('--limite', type=int)
    p.add_argument('--solo', help='procesa solo clases cuyo nombre contenga este texto')
    p.add_argument('--ver', action='store_true')
    p.add_argument('--forzar', action='store_true', help='rehace también las clases ya marcadas')
    a = p.parse_args()
    lista = clases(a.curso)
    if a.solo:
        lista = [c for c in lista if a.solo.lower() in c.name.lower()]
    if a.limite:
        lista = lista[:a.limite]
    if a.ver:
        for c in lista:
            print(c.name)
        print(f'{len(lista)} clases')
        return 0
    base = Path(a.curso).resolve()
    base = base.parent if base.name in ('Apuntes', 'capturas') else base
    # v10: el registro va a la caché, no a la carpeta del curso (era ruido a la vista)
    cache = Path.home() / '.cache' / 'auto-captura'
    cache.mkdir(parents=True, exist_ok=True)
    LOG = open(cache / f'regeneracion · {base.name}.log', 'a', encoding='utf-8')
    RESULTADO = cache / f'regeneracion · {base.name}.json'
    decir(f'=== {time.strftime("%F %T")}: {len(lista)} clases · {cu.nombre_motor()} ===')
    informe = {'total': len(lista), 'ok': 0, 'errores': [], 'detalle': [], 'inicio': time.time()}
    for i, clase in enumerate(lista, 1):
        decir(f'[{i}/{len(lista)}] {clase.name}')
        if (clase / '.regenerado-v6').is_file() and not a.forzar:
            decir('    saltada: ya regenerada')
            informe['ok'] += 1
            informe['detalle'].append({'clase': clase.name, 'estado': 'saltada'})
            continue
        try:
            estado = regenerar(clase)
        except Exception as e:  # noqa: BLE001: una clase no debe tumbar el curso
            estado = f'error: {type(e).__name__}: {e}'
        decir(f'    {estado}')
        if estado.startswith(('ok', 'sin apuntes', 'conservado', 'sin contenido real')):
            informe['ok'] += 1
            if estado.startswith(('ok', 'conservado', 'sin contenido real')):
                (clase / '.regenerado-v6').write_text(time.strftime('%F %T'), encoding='utf-8')
        else:
            informe['errores'].append({'clase': str(clase), 'error': estado})
        informe['detalle'].append({'clase': clase.name, 'estado': estado})
        RESULTADO.write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding='utf-8')
    informe['fin'] = time.time()
    RESULTADO.write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding='utf-8')
    decir(f'Terminado: {informe["ok"]}/{len(lista)} correctas, {len(informe["errores"])} errores. '
          f'Informe: {RESULTADO}')
    return 0 if not informe['errores'] else 2


if __name__ == '__main__':
    sys.exit(main())
