#!/usr/bin/env python3
# CLASES/publica.py
#
# Publicacion local/web del proyecto CLASES.
# No usa Zenodo. Genera derivados verificables (.json y .lean), prepara
# catalogo.cat. La opción --web publica la interfaz web del proyecto.

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
    fuente = PROJECT_DIR / "tools" / "pdfs"
    destino.mkdir(parents=True, exist_ok=True)

    if not fuente.is_dir():
        return destino

    copiados = 0
    for src in sorted(fuente.glob("*.pdf")):
        dst = destino / src.name
        if (not dst.exists()) or src.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(src, dst)
            copiados += 1
    if copiados:
        print(f"[PDF] Copiados/actualizados desde tools/pdfs: {copiados}")
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


def publicar_web(pdf_dir: Path):
    if not PUBLICAR_WEB:
        print("[WEB] PUBLICAR_WEB = False")
        return

    from PackPublica.FTPClient import FTPClient
    from PackPublica.WebPublisher import WebPublisher

    ftp = FTPClient()

    WebPublisher(
        ftp,
        local_dir=pdf_dir,
        remote_dir=REMOTE_DIR,
        extensions={".pdf", ".php", ".csv", ".cat", ".abstract", ".png"},
    ).sync()

    WebPublisher(
        ftp,
        local_dir=PROJECT_DIR,
        remote_dir=REMOTE_DIR + "/md",
    ).sync()

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
    parser.add_argument('--web', action='store_true', help='Subir los resultados a la web del autor')
    args = parser.parse_args()
    PUBLICAR_WEB = args.web
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    from PackPublica.publicar import Publicar

    os.chdir(PROJECT_DIR)
    print("CLASES: PUBLICAR sin Zenodo")
    print(f"Proyecto: {PROJECT_DIR}")

    publica = Publicar(__file__)
    publica.FORZADO = False
    md_objects = [publica.test(path.stem) for path in sorted(PROJECT_DIR.glob('*.md')) if parse_doc_id(path.stem)]

    generar_catalogo_cat(md_objects)
    generar_derivados(md_objects)

    pdf_dir = asegurar_pdfs_publicables()
    copiar_web_base_a_pdfs(pdf_dir)
    shutil.copy2(PROJECT_DIR / "catalogo.cat", pdf_dir / "catalogo.cat")

    publicar_web(pdf_dir)
    print("CLASES: proceso terminado.")


if __name__ == "__main__":
    main()
