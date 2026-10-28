"""Copias trazables de los españoles actuales de UNIHOLOG. Autor: Víctor Estrada Díaz.

Texto CC BY-NC-SA 4.0; código HL3. https://estradad.es/licencia.php
No usa red, no modifica el origen ni restaura versiones anteriores.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import os
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_current(path: Path, data: bytes) -> None:
    if path.is_file() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(data)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def encode(data) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def plan(origin: Path, project: Path):
    config = json.loads((project / 'fuentes.json').read_text(encoding='utf-8'))
    records = []
    for item in config['documents']:
        matches = sorted(path for path in origin.glob(item['pattern']) if path.is_file())
        if len(matches) != 1:
            raise ValueError(f"Se necesita una única fuente actual para {item['pattern']}: {len(matches)} encontradas")
        source = matches[0]
        data = source.read_bytes()
        text = data.decode('utf-8-sig')
        hits = [{'line': n, 'text': line.strip()} for n, line in enumerate(text.splitlines(), 1)
                if re.search(r'\bclases?\b', line, re.I)]
        if not hits:
            raise ValueError(f'{source.name} no contiene referencias a clases')
        records.append((source, data, dict(file=source.name, role=item['role'],
                        sha256=sha(data), bytes=len(data), references=hits)))
    return config, records


def synchronize(origin: Path, project: Path = ROOT):
    origin, project = origin.resolve(), project.resolve()
    if origin == project or origin in project.parents or project in origin.parents:
        raise ValueError('El origen y CLASES deben ser proyectos separados')
    config, records = plan(origin, project)
    destination = project / 'documentos/UNIHOLOG'
    manifest_path = destination / 'manifest.json'
    old = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'documents': []}
    previous = {item['file']: item['sha256'] for item in old['documents']}
    # Comprobar todo antes de escribir. Una edición local no se sustituye a ciegas.
    for source, data, record in records:
        target = destination / source.name
        if target.exists() and target.read_bytes() != data:
            if previous.get(source.name) != sha(target.read_bytes()):
                raise ValueError(f'Copia local modificada: {source.name}; resolver antes de sincronizar')
    for source, data, record in records:
        if source.read_bytes() != data:
            raise RuntimeError(f'La fuente cambió durante la lectura: {source.name}')
    for source, data, record in records:
        write_current(destination / source.name, data)
    for source, data, record in records:
        if source.read_bytes() != data:
            raise RuntimeError(f'La fuente cambió durante la copia: {source.name}')
    manifest = {key: config[key] for key in ('author', 'license', 'source_project')}
    manifest['documents'] = [record for source, data, record in records]
    write_current(manifest_path, encode(manifest))
    lines = ['# Fuentes de UNIHOLOG para CLASES', '',
             'Autor: **Víctor Estrada Díaz**. [Licencias y condiciones](https://estradad.es/licencia.php).', '',
             'Copias íntegras de los españoles actuales de la raíz del proyecto vecino UNIHOLOG.',
             'Los originales permanecen allí. No se han usado traducciones ni totales como fuente.', '',
             '| Documento | Uso en CLASES | Referencias a clases |', '|---|---|---:|']
    for record in manifest['documents']:
        lines.append(f"| [{record['file']}](documentos/UNIHOLOG/{record['file']}) | {record['role']} | {len(record['references'])} |")
    lines += ['', 'Las líneas y sus huellas exactas están en [manifest.json](documentos/UNIHOLOG/manifest.json).', '',
              'Estos textos son antecedentes del autor. Su recuperación no constituye una nueva verificación científica.', '']
    write_current(project / 'FUENTES_UNIHOLOG.md', '\n'.join(lines).encode('utf-8'))
    return manifest


def verify(project: Path = ROOT, origin: Path | None = None):
    destination = project / 'documentos/UNIHOLOG'
    manifest = json.loads((destination / 'manifest.json').read_text(encoding='utf-8'))
    for record in manifest['documents']:
        if sha((destination / record['file']).read_bytes()) != record['sha256']:
            raise ValueError(f"Copia modificada: {record['file']}")
        if origin is not None and sha((origin / record['file']).read_bytes()) != record['sha256']:
            raise ValueError(f"El español de origen ha cambiado: {record['file']}")
    return manifest


def main():
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['listar', 'sincronizar', 'verificar'])
    parser.add_argument('--origen', type=Path, default=None)
    args = parser.parse_args()
    origin = args.origen or ROOT.parent / 'UNIHOLOG'
    if args.action == 'sincronizar':
        result = synchronize(origin)
    elif args.action == 'verificar':
        result = verify(origin=origin if origin.is_dir() else None)
    else:
        result = {'documents': [record for source, data, record in plan(origin, ROOT)[1]]}
    for record in result['documents']:
        print(f"✅ {record['file']} · {len(record['references'])} referencias · SHA-256 {record['sha256']}")


if __name__ == '__main__':
    main()
