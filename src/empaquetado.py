"""Un único ZIP reproducible de CLASES para Zenodo, sin publicar.

Autor: Víctor Estrada Díaz. Código HL3. https://estradad.es/licencia.php
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import zipfile
import html

EXCLUDED_DIRS = {
    '.git', '.ssh', '.aws', '.azure', '.gnupg', '.kube', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    '.venv', 'venv', 'node_modules', 'logs', 'tmp', 'temp', 'backups',
    'backup', 'bck', 'old', 'sav', 'anterior', 'historial', 'respaldos',
    'zenodo', 'dist', 'build',
}
SECRET_NAMES = {'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519', '.git-credentials', 'credentials', '.netrc', '.npmrc', '.pypirc', 'credentials.json', 'credentials.txt',
                'secrets.json', 'secrets.yaml', 'secrets.yml', 'token.txt', 'tokens.txt'}


def eligible(name: str) -> bool:
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError(f'Ruta no admisible: {name}')
    if any(part.casefold() in EXCLUDED_DIRS for part in path.parts[:-1]):
        return False
    filename = path.name.casefold()
    if filename.startswith('.env') or filename in SECRET_NAMES:
        return False
    if path.suffix.casefold() in {'.pem', '.key', '.p12', '.pfx', '.kdbx', '.keystore', '.pyc', '.pyo', '.tmp'}:
        return False
    return not re.search(r'\.bak(?:\.|$)|\.old$|\.orig$|~$|\.antes_|\.backup', filename)


def git(root: Path, *args: str) -> bytes:
    process = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
    if process.returncode:
        raise RuntimeError('Git no pudo comprobar la versión local de CLASES: ' +
                           process.stderr.decode('utf-8', errors='replace').strip())
    return process.stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _member(archive, name, data, executable=False):
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.create_system = 3
    info.external_attr = (0o100755 if executable else 0o100644) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, data, compresslevel=9)


def verify_package(package: Path):
    with zipfile.ZipFile(package) as archive:
        if archive.testzip() is not None:
            raise ValueError('El ZIP contiene una entrada dañada')
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('El ZIP contiene nombres duplicados')
        manifest_name = 'CLASES/VERSION_ARCHIVO.json'
        metadata = json.loads(archive.read(manifest_name))
        expected = {manifest_name}
        for item in metadata['files']:
            relative = item['path']
            if not eligible(relative):
                raise ValueError(f'Archivo excluido dentro del ZIP: {relative}')
            name = 'CLASES/' + relative
            expected.add(name)
            if sha(archive.read(name)) != item['sha256']:
                raise ValueError(f'Contenido distinto al manifiesto: {relative}')
        if set(names) != expected:
            raise ValueError('El contenido del ZIP no coincide con el manifiesto')
        return metadata


def preparar_paquete(root: Path):
    root = root.resolve()
    actual_root = Path(git(root, 'rev-parse', '--show-toplevel').decode('utf-8').strip()).resolve()
    if actual_root != root:
        raise RuntimeError('CLASES debe tener su propio repositorio Git; no se empaqueta el proyecto padre')
    if git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all'):
        raise RuntimeError('Hay cambios sin registrar en CLASES. Revisarlos y registrarlos antes de crear el ZIP de versión.')
    commit = git(root, 'rev-parse', 'HEAD').decode('ascii').strip()
    tree = git(root, 'ls-tree', '-rz', '--full-tree', 'HEAD')
    contents = []
    for record in tree.split(b'\0'):
        if not record:
            continue
        properties, raw_name = record.split(b'\t', 1)
        mode, kind, object_id = properties.split()
        name = raw_name.decode('utf-8')
        if name == 'VERSION_ARCHIVO.json':
            raise RuntimeError('VERSION_ARCHIVO.json está reservado para el manifiesto del ZIP')
        if not eligible(name):
            continue
        if mode not in (b'100644', b'100755') or kind != b'blob':
            raise RuntimeError(f'No se empaquetan enlaces ni submódulos como archivos: {name}')
        data = git(root, 'cat-file', 'blob', object_id.decode('ascii'))
        contents.append((name, data, mode == b'100755'))
    if not contents:
        raise RuntimeError('No hay archivos de proyecto para empaquetar')
    metadata = {
        'project': 'CLASES', 'author': 'Víctor Estrada Díaz',
        'repository': 'https://github.com/quark-cha/CLASES',
        'commit': commit,
        'licenses': {'text': 'CC BY-NC-SA 4.0', 'code': 'HL3',
                     'author_terms': 'https://estradad.es/licencia.php'},
        'files': [{'path': name, 'sha256': sha(data), 'bytes': len(data)}
                  for name, data, executable in sorted(contents)],
    }
    destination = root / 'zenodo' / 'CLASES.zip'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, suffix='.tmp', delete=False) as stream:
        temporary = Path(stream.name)
    try:
        with zipfile.ZipFile(temporary, 'w') as archive:
            for name, data, executable in sorted(contents):
                _member(archive, 'CLASES/' + name, data, executable)
            _member(archive, 'CLASES/VERSION_ARCHIVO.json',
                    (json.dumps(metadata, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        verify_package(temporary)
        # Cancelar si el autor modifica el proyecto durante el empaquetado.
        if git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all'):
            raise RuntimeError('El proyecto cambió durante el empaquetado; se conserva el ZIP anterior')
        if git(root, 'rev-parse', 'HEAD').decode('ascii').strip() != commit:
            raise RuntimeError('El commit cambió durante el empaquetado; se conserva el ZIP anterior')
        if not destination.exists() or sha(destination.read_bytes()) != sha(temporary.read_bytes()):
            os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination, metadata


def _write_current(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)


def preparar_web(root: Path, package: Path, metadata):
    """Preparar la página y su descarga local; no realiza conexiones de red."""
    if verify_package(package)['commit'] != metadata['commit']:
        raise RuntimeError('El ZIP no corresponde a la versión de la página')
    comprobar_version(root, metadata)
    destination = root / 'pdfs'
    _write_current(destination / 'CLASES.zip', package.read_bytes())
    sources = []
    with zipfile.ZipFile(package) as archive:
        members = set(archive.namelist())
        cover = 'CLASES/img/CLASES_mundo_matematico.png'
        has_cover = cover in members
        if has_cover:
            _write_current(destination / 'CLASES_mundo_matematico.png', archive.read(cover))
        manifest = 'CLASES/documentos/UNIHOLOG/manifest.json'
        if manifest in members:
            manifest_bytes = archive.read(manifest)
            _write_current(destination / 'fuentes/manifest.json', manifest_bytes)
            for item in json.loads(manifest_bytes)['documents']:
                name = item['file']
                if PurePosixPath(name).name != name or not eligible(name):
                    raise ValueError('Nombre de fuente no admisible en el manifiesto')
                from urllib.parse import quote
                data = archive.read('CLASES/documentos/UNIHOLOG/' + name)
                if item.get('sha256') and sha(data) != item['sha256']:
                    raise ValueError('La fuente web no coincide con su manifiesto: ' + name)
                _write_current(destination / 'fuentes' / name, data)
                sources.append(f'<li><a href="fuentes/{quote(name)}">{html.escape(name)}</a></li>')
    hero = '<img class="cover" src="CLASES_mundo_matematico.png" alt="Montañero explorando un paisaje matemático con montañas fractales">' if has_cover else ''
    document = '''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>CLASES · Víctor Estrada Díaz</title>
<style>body{margin:0;background:#f4f6f8;color:#182b3c;font:18px/1.6 system-ui,sans-serif}
main{max-width:960px;margin:auto;padding:24px}.cover{width:100%;height:auto;border-radius:12px}
section{background:white;padding:24px;border-radius:12px;margin:20px 0}h1{font-size:2.5rem;margin:0}
a{color:#075c70}nav{display:flex;gap:12px;flex-wrap:wrap}.button{background:#075c70;color:white;
padding:12px 18px;border-radius:6px;text-decoration:none;display:inline-block}small{color:#42576a}
</style></head><body><main>''' + hero + '''<section><h1>CLASES</h1>
<p>Un proyecto de investigación de <strong>Víctor Estrada Díaz</strong> sobre clases,
transformaciones e invariantes, basado en UNIHOLOG.</p>
<nav><a class="button" href="CLASES.zip" download>Descargar proyecto completo (ZIP)</a>
<a class="button" href="https://github.com/quark-cha/CLASES">Ver en GitHub</a>
<a class="button" href="index.php">Artículos del proyecto</a></nav>
<p><small>Versión: ''' + html.escape(metadata['commit'][:12]) + '''.</small></p></section>
<section><h2>Qué contiene la descarga</h2><p>Código, documentos de consulta, portada,
pruebas, instrucciones y licencias. El archivo incluye la referencia exacta a su versión
y las huellas de sus archivos.</p><p>Las herramientas se documentan en <a href="https://github.com/quark-cha/CLASES/tree/main/src">src</a>.</p></section>
<section><h2>Fuentes de UNIHOLOG</h2><ul>''' + ''.join(sources) + '''</ul>
<p>Los documentos se conservan íntegros, con su autoría y procedencia. Las comprobaciones
auxiliares no constituyen por sí mismas nuevas demostraciones matemáticas.</p></section>
<section><h2>Autoría y licencias</h2><p>Víctor Estrada Díaz · Textos CC BY-NC-SA 4.0 · Código HL3.</p>
<p><a href="https://estradad.es/licencia.php">Licencias y condiciones del autor</a></p>
</section></main></body></html>'''
    path = destination / 'proyecto.html'
    _write_current(path, document.encode('utf-8'))
    return path


def comprobar_version(root: Path, metadata):
    if git(root, 'rev-parse', 'HEAD').decode('ascii').strip() != metadata['commit']:
        raise RuntimeError('El ZIP pertenece a otro commit; preparar la versión actual antes de publicar')
    if git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all'):
        raise RuntimeError('El proyecto tiene cambios sin registrar; no se publica una versión distinta del ZIP')
