"""Variantes LinkedIn locales de CLASES. Víctor Estrada Díaz; código HL3.

https://estradad.es/licencia.php
No publica en LinkedIn, web, GitHub ni Zenodo.
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
from pathlib import Path
import re
from fuentes import write_current, encode

ARTICLE = re.compile(r'^[A-Za-z]{2}_\d+(?:[_\-\s].*)?$')
FORMATS = {'.md', '.pdf', '.html', '.docx', '.odt', '.json', '.lean', '.pl'}


def es_version_linkedin(path):
    path = Path(path)
    return path.stem.casefold().endswith('_linkedin') and path.suffix.casefold() in FORMATS


def sha(data):
    return hashlib.sha256(data).hexdigest()


def preparar_variantes(root, crear=True, revisado=False):
    root = Path(root)
    state_file = root / 'logs/linkedin_estado.json'
    state = json.loads(state_file.read_text(encoding='utf-8')) if state_file.exists() else {}
    variants = {p.name: p for p in root.glob('*.md') if ARTICLE.fullmatch(p.stem) and es_version_linkedin(p)}
    bases = [p for p in root.glob('*.md') if ARTICLE.fullmatch(p.stem) and not es_version_linkedin(p)]
    for base in bases:
        variant = base.with_name(base.stem + '_linkedin.md')
        if crear or variant.exists():
            variants[variant.name] = variant
    prepared = []
    for variant in sorted(variants.values()):
        base = variant.with_name(variant.stem[:-len('_linkedin')] + '.md')
        data = base.read_bytes() if base.exists() else None
        source_hash = sha(data) if data is not None else None
        previous = state.get(variant.name, {})
        current = variant.read_bytes() if variant.exists() else None
        automatic = previous.get('automatic', current == data)
        if current is None:
            if data is None:
                raise ValueError(f'No hay texto para {variant.name}')
            write_current(variant, data)
            current, automatic = data, True
        elif previous and previous.get('source_sha256') != source_hash:
            if automatic and sha(current) == previous.get('variant_sha256') and data is not None:
                write_current(variant, data)
                current = data
            elif revisado:
                automatic = False
            else:
                raise ValueError(f'El artículo base cambió y {variant.name} tiene una edición propia; revisar ambas versiones y ejecutar --linkedin --revisado sin sobrescribirlas')
        elif previous and sha(current) != previous.get('variant_sha256'):
            automatic = False
        prepared.append((variant, base, source_hash, current, automatic, previous))
    return state_file, state, prepared


def generar_linkedin(root, publisher, crear=True, revisado=False):
    from PackPublica.logging import document_work
    root = Path(root)
    state_file, state, variants = preparar_variantes(root, crear, revisado)
    cover = root / 'img/CLASES_mundo_matematico.png'
    cover_bytes = cover.read_bytes() if cover.exists() else b''
    profile = sha(b'linkedin-A4-v4' + cover_bytes)
    results = []
    for variant, base, source_hash, data, automatic, previous in variants:
        destination = root / 'linkedin' / variant.with_suffix('.pdf').name
        with document_work(variant):
            current_hash = sha(data)
            if (previous.get('variant_sha256') == current_hash and
                    previous.get('profile') == profile and destination.is_file()):
                state[variant.name] = {'source_sha256': source_hash, 'variant_sha256': current_hash,
                                       'automatic': automatic, 'profile': profile,
                                       'pdf': str(destination.relative_to(root))}
                write_current(state_file, encode(state))
                results.append(destination)
                continue
            md = publisher.test(variant.stem)
            rendered = md.html(guardar=False)
            title = next((line.strip().lstrip('#').strip() for line in data.decode('utf-8-sig').splitlines() if line.strip()), variant.stem)
            image = '<img src="data:image/png;base64,' + base64.b64encode(cover_bytes).decode('ascii') + '" alt="CLASES">' if cover_bytes else ''
            front = '<section class="linkedin-cover">' + image + '<h1>' + html.escape(title) + '</h1><p>Víctor Estrada Díaz</p></section>'
            style = '''<style>
@page{size:A4;margin:18mm;@bottom-center{content:'CLASES - ' counter(page);font-size:10px;color:#536273}}body{font-size:19px;line-height:1.5;max-width:none}
.linkedin-cover{break-after:page;text-align:center;padding-top:15mm}
.linkedin-cover img{width:100%;height:auto}.linkedin-cover h1{font-size:28px;line-height:1.25;margin-top:18mm}
.linkedin-cover p{font-size:19px}math[display="block"]{break-inside:avoid;max-width:100%;margin:1em 0}
p{orphans:3;widows:3}.math-lead{break-after:avoid}h1,h2,h3{break-after:avoid}
</style>'''
            rendered.contenido = re.sub(r'<p>((?:(?!</p>).)*:)</p>\s*(?=<math\b|<p>\s*<math\b)',
                                       r'<p class="math-lead">\1</p>', rendered.contenido, flags=re.S)
            rendered.contenido = re.sub(r'''(<math\b(?![^>]*display=["']block["'])[^>]*>(?:(?!</math>).)*</math>)([.,;:!?])''',
                                       r'<span style="white-space:nowrap;display:inline-block">\1\2</span>',
                                       rendered.contenido, flags=re.S)
            rendered.contenido = rendered.contenido.replace('</head>', style + '</head>', 1)
            rendered.contenido = rendered.contenido.replace('<body>', '<body>' + front, 1)
            destination.parent.mkdir(parents=True, exist_ok=True)
            rendered.pdf(page_size='A4').save(destination)
            if variant.read_bytes() != data or (base.exists() and sha(base.read_bytes()) != source_hash):
                raise RuntimeError('El texto cambió durante la generación; no se marca la versión LinkedIn como terminada')
            state[variant.name] = {'source_sha256': source_hash, 'variant_sha256': current_hash,
                                   'automatic': automatic, 'profile': profile,
                                   'pdf': str(destination.relative_to(root))}
            write_current(state_file, encode(state))
            results.append(destination)
    return results
