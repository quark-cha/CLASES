#!/usr/bin/env python3
# CLASES/publica.py
#
# Publicacion local/web del proyecto CLASES.
# Prepara un ZIP local de la versión completa para Zenodo, sin subirlo.
# La opción --web publica el proyecto y el catálogo en la web del autor.

import argparse
import csv
import os
import re
import shutil
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parent
PUBLICAR_DIR = REPO_ROOT / "PUBLICAR"
SRC_DIR = PROJECT_DIR / 'src'
sys.path.insert(0, str(SRC_DIR))

if str(PUBLICAR_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICAR_DIR))



PAGE_SIZE = "6x9"

GENERAR_HTML = True
GENERAR_PDF = True
GENERAR_DOCX = False
GENERAR_JSON = True
GENERAR_LEAN = True
PUBLICAR_WEB = False

REMOTE_DIR = "/estradad.es/teorias/pdf/CLASES"
CATALOGO_CAT_LANGS = ["ES", "EN", "FR", "IT", "PT", "DE", "AR", "JP", "RU", "CH"]


def parse_doc_id(stem: str):
    match = re.match(r"^([A-Za-z]{2})_(\d+)(?:[_\-\s].*)?$", stem)
    if not match:
        return None
    return match.group(1).upper(), str(int(match.group(2)))


def clean_title(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    value = value.strip(" #\t\r\n")
    value = re.sub(r"^\s*[A-Za-z]{2}_\d+\s*[:\-â€“â€”]\s*", "", value)
    value = re.sub(r"^\s*\d+\s*[:\-â€“â€”]\s*", "", value)
    return value.strip()


def title_from_filename(stem: str) -> str:
    parsed = parse_doc_id(stem)
    if parsed:
        lang, number = parsed
        prefix = f"{lang}_{number}"
        rest = re.sub(rf"^{lang}_0*{number}[_\-\s]*", "", stem, flags=re.I)
    else:
        rest = stem
    rest = rest.replace("_", " ").replace("-", " ")
    rest = re.sub(r"\s+", " ", rest).strip()
    return rest.title() if rest else stem


def title_from_md(md_path: Path) -> str:
    fallback = title_from_filename(md_path.stem)
    try:
        lines = md_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return fallback

    for line in lines[:60]:
        clean = line.strip()
        if not clean.startswith("# "):
            continue
        title = clean_title(clean[2:])
        low = title.lower()
        if not title:
            continue
        if "autoria" in low or "autorÃ­a" in low or "authorship" in low or "contact" in low:
            continue
        return title
    return fallback


def generar_catalogo_cat(md_objects) -> Path:
    rows = {}
    for md_obj in md_objects:
        md_path = Path(md_obj.fichero)
        parsed = parse_doc_id(md_path.stem)
        if not parsed:
            continue
        lang, number = parsed
        if lang not in CATALOGO_CAT_LANGS:
            continue
        rows.setdefault(number, {"Id": number})
        rows[number][lang] = title_from_md(md_path)

    catalog_path = PROJECT_DIR / "catalogo.cat"
    with catalog_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["Id"] + CATALOGO_CAT_LANGS,
            delimiter=";",
            lineterminator="\n",
        )
        writer.writeheader()
        for number in sorted(rows, key=lambda x: int(x)):
            writer.writerow(rows[number])

    print(f"[CAT] {catalog_path} ({len(rows)} documentos numerados)")
    return catalog_path


def asegurar_pdfs_publicables():
    """Mantiene PROJECT_DIR/pdfs como carpeta unica de publicacion web."""
    destino = PROJECT_DIR / "pdfs"
    destino.mkdir(parents=True, exist_ok=True)
    return destino



def copiar_web_base_a_pdfs(pdf_dir: Path):
    web_base = PROJECT_DIR / "web-base"
    if not web_base.is_dir():
        return
    for name in ("index.php", "index.csv"):
        src = web_base / name
        if src.is_file():
            shutil.copy2(src, pdf_dir / name)
    for src in sorted(web_base.glob("*.png")):
        if re.match(r"^[A-Za-z]{2}_\d+\.png$", src.name):
            shutil.copy2(src, pdf_dir / src.name)


def generar_derivados(md_objects):
    fallidos = []
    for md_obj in md_objects:
        nombre = Path(md_obj.fichero).name
        try:
            resultados = md_obj.generar_derivados(
                page_size=PAGE_SIZE,
                generar_html=GENERAR_HTML,
                generar_pdf=GENERAR_PDF,
                generar_docx=GENERAR_DOCX,
                generar_json=GENERAR_JSON,
                generar_lean=GENERAR_LEAN,
            )
            hechos = [k for k, v in resultados.items() if v]
            print(f"[OK] {nombre}: {', '.join(hechos) if hechos else 'sin cambios'}")
        except Exception as exc:
            fallidos.append(nombre)
            print(f"[WARN] fallo generando derivados completos para {nombre}: {exc}")
            if GENERAR_JSON or GENERAR_LEAN:
                try:
                    md_obj.generar_derivados(
                        page_size=PAGE_SIZE,
                        generar_html=False,
                        generar_pdf=False,
                        generar_docx=False,
                        generar_json=GENERAR_JSON,
                        generar_lean=GENERAR_LEAN,
                    )
                    print(f"[OK] {nombre}: json/lean generados tras fallback")
                except Exception as exc2:
                    print(f"[ERROR] {nombre}: tampoco se pudo generar json/lean: {exc2}")

    if fallidos:
        raise RuntimeError('Publicación detenida: generación incompleta de ' + ', '.join(fallidos))


def publicar_web(pdf_dir: Path):
    if not PUBLICAR_WEB:
        print("[WEB] PUBLICAR_WEB = False")
        return

    from empaquetado import verify_package, comprobar_version
    metadata = verify_package(pdf_dir / 'CLASES.zip')
    comprobar_version(PROJECT_DIR, metadata)

    from PackPublica.FTPClient import FTPClient
    from PackPublica.WebPublisher import WebPublisher

    ftp = FTPClient()

    WebPublisher(
        ftp,
        local_dir=pdf_dir,
        remote_dir=REMOTE_DIR,
        extensions={".pdf", ".php", ".html", ".csv", ".cat", ".abstract", ".png", ".zip"},
    ).sync()

    WebPublisher(
        ftp,
        local_dir=PROJECT_DIR,
        remote_dir=REMOTE_DIR + "/md",
    ).sync()

    fuentes_dir = pdf_dir / 'fuentes'
    if fuentes_dir.is_dir():
        WebPublisher(ftp, local_dir=fuentes_dir, remote_dir=REMOTE_DIR + '/fuentes',
                     extensions={'.md', '.json'}).sync()

    json_dir = PROJECT_DIR / "json"
    if json_dir.is_dir():
        WebPublisher(
            ftp,
            local_dir=json_dir,
            remote_dir=REMOTE_DIR + "/json",
            extensions={".json"},
        ).sync()

    lean_dir = PROJECT_DIR / "lean"
    if lean_dir.is_dir():
        WebPublisher(
            ftp,
            local_dir=lean_dir,
            remote_dir=REMOTE_DIR + "/lean",
            extensions={".lean"},
        ).sync()


def main():
    global PUBLICAR_WEB
    parser = argparse.ArgumentParser(description='Preparar y publicar CLASES')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--web', action='store_true', help='Subir los resultados a la web del autor')
    mode.add_argument('--solo-zip', action='store_true', help='Preparar únicamente el ZIP local, sin publicar')
    mode.add_argument('--preparar-web', action='store_true', help='Preparar ZIP y página web local sin convertir documentos ni subir archivos')
    args = parser.parse_args()
    if args.solo_zip and (args.web or args.preparar_web):
        parser.error('--solo-zip no se combina con opciones web')
    PUBLICAR_WEB = args.web
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    from empaquetado import preparar_paquete, preparar_web
    from fuentes import verify

    os.chdir(PROJECT_DIR)
    print('CLASES: proyecto completo, ZIP local para Zenodo y web opcional')
    if (PROJECT_DIR / 'documentos/UNIHOLOG/manifest.json').is_file():
        source = PROJECT_DIR.parent / 'UNIHOLOG'
        verify(PROJECT_DIR, source if source.is_dir() else None)
    package, metadata = preparar_paquete(PROJECT_DIR)
    print(f'[ZIP] {package} · versión {metadata["commit"][:12]} · {len(metadata["files"])} archivos')
    if args.solo_zip:
        return

    if not args.preparar_web:
        from PackPublica.publicar import Publicar
        publica = Publicar(__file__)
        publica.FORZADO = False
        md_objects = [publica.test(path.stem) for path in sorted(PROJECT_DIR.glob('*.md')) if parse_doc_id(path.stem)]
        generar_catalogo_cat(md_objects)
        generar_derivados(md_objects)

    pdf_dir = asegurar_pdfs_publicables()
    copiar_web_base_a_pdfs(pdf_dir)
    shutil.copy2(PROJECT_DIR / 'catalogo.cat', pdf_dir / 'catalogo.cat')
    page = preparar_web(PROJECT_DIR, package, metadata)
    print(f'[WEB] Página local preparada: {page}')
    publicar_web(pdf_dir)
    print('CLASES: proceso terminado.')


if __name__ == '__main__':
    main()
