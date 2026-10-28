"""Paquete y web de CLASES: pruebas locales, sin FTP ni Zenodo."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import Mock, patch
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import empaquetado


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.run_git('init', '-b', 'main')
        self.run_git('config', 'user.name', 'Test')
        self.run_git('config', 'user.email', 'test@example.invalid')
        self.put('.gitignore', '/zenodo/\n/pdfs/\n')
        self.put('README.md', '# Proyecto de prueba')
        self.put('src/example.py', 'print(1)\n')
        self.put('LICENCIAS.md', 'Víctor Estrada Díaz, textos CC BY-NC-SA 4.0; código HL3.')
        self.put('img/CLASES_mundo_matematico.png', b'png fixture')
        self.put('.env', 'SECRET_TEST_ONLY=not-a-real-secret')
        self.put('backups/old.md', 'obsolete fixture')
        self.put('src/example.py.bak', 'obsolete fixture')
        self.put('logs/session.txt', 'old fixture log')
        self.run_git('add', '--force', '.')
        self.run_git('commit', '-m', 'fixture')

    def put(self, relative, content):
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode('utf-8') if isinstance(content, str) else content)

    def run_git(self, *args):
        return subprocess.run(['git', '-C', str(self.project), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def test_one_complete_zip_with_commit_and_no_credentials_or_old_copies(self):
        package, metadata = empaquetado.preparar_paquete(self.project)
        self.assertEqual(list((self.project / 'zenodo').iterdir()), [package])
        self.assertEqual(metadata['commit'], self.run_git('rev-parse', 'HEAD').decode().strip())
        self.assertEqual(empaquetado.verify_package(package), metadata)
        with zipfile.ZipFile(package) as archive:
            names = archive.namelist()
            for name in ['README.md', 'src/example.py', 'LICENCIAS.md', 'img/CLASES_mundo_matematico.png']:
                self.assertIn('CLASES/' + name, names)
            self.assertFalse(any('.git/' in n or '.env' in n or '.bak' in n or '/backups/' in n or '/logs/' in n for n in names))

    def test_same_version_is_byte_identical_and_does_not_rewrite_zip(self):
        package, _ = empaquetado.preparar_paquete(self.project)
        before = package.read_bytes(), package.stat().st_mtime_ns
        empaquetado.preparar_paquete(self.project)
        self.assertEqual(before, (package.read_bytes(), package.stat().st_mtime_ns))

    def test_dirty_source_is_never_replaced_by_committed_old_copy(self):
        package, _ = empaquetado.preparar_paquete(self.project)
        previous = package.read_bytes()
        self.put('README.md', '# Corrección nueva no registrada')
        with self.assertRaisesRegex(RuntimeError, 'cambios sin registrar'):
            empaquetado.preparar_paquete(self.project)
        self.assertEqual(package.read_bytes(), previous)

    def test_next_commit_replaces_single_zip_and_contains_new_content(self):
        package, before = empaquetado.preparar_paquete(self.project)
        self.put('README.md', '# Nueva versión')
        self.run_git('add', 'README.md')
        self.run_git('commit', '-m', 'new fixture')
        current, metadata = empaquetado.preparar_paquete(self.project)
        self.assertEqual(package, current)
        self.assertNotEqual(before['commit'], metadata['commit'])
        self.assertEqual(len(list(package.parent.glob('*.zip'))), 1)
        with zipfile.ZipFile(package) as archive:
            self.assertEqual(archive.read('CLASES/README.md').decode(), '# Nueva versión')

    def test_parent_repository_is_not_packaged(self):
        child = self.project / 'child'
        child.mkdir()
        with self.assertRaisesRegex(RuntimeError, 'propio repositorio'):
            empaquetado.preparar_paquete(child)

    def test_local_page_includes_download_github_author_and_same_archive(self):
        package, metadata = empaquetado.preparar_paquete(self.project)
        page = empaquetado.preparar_web(self.project, package, metadata)
        text = page.read_text(encoding='utf-8')
        self.assertIn('href="CLASES.zip"', text)
        self.assertIn('https://github.com/quark-cha/CLASES', text)
        self.assertIn('Víctor Estrada Díaz', text)
        self.assertIn(metadata['commit'][:12], text)
        self.assertEqual((page.parent / 'CLASES.zip').read_bytes(), package.read_bytes())

    def test_source_links_have_exact_local_copies_from_same_zip(self):
        self.put('documentos/UNIHOLOG/ES_49_clases.md', '# Clases $U_c$\r\n')
        self.put('documentos/UNIHOLOG/manifest.json', json.dumps({'documents': [{'file': 'ES_49_clases.md'}]}))
        self.run_git('add', 'documentos')
        self.run_git('commit', '-m', 'source fixture')
        package, metadata = empaquetado.preparar_paquete(self.project)
        page = empaquetado.preparar_web(self.project, package, metadata)
        self.assertIn('fuentes/ES_49_clases.md', page.read_text(encoding='utf-8'))
        with zipfile.ZipFile(package) as archive:
            self.assertEqual((page.parent / 'fuentes/ES_49_clases.md').read_bytes(),
                             archive.read('CLASES/documentos/UNIHOLOG/ES_49_clases.md'))


class PublicationTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('clases_publica_tested', ROOT / 'publica.py')
        self.publica = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.publica)

    def test_web_upload_includes_project_zip_page_and_sources(self):
        ftp = types.ModuleType('PackPublica.FTPClient')
        ftp.FTPClient = Mock()
        web = types.ModuleType('PackPublica.WebPublisher')
        web.WebPublisher = Mock()
        self.publica.PUBLICAR_WEB = True
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            root = Path(directory)
            (root / 'pdfs').mkdir()
            (root / 'pdfs/fuentes').mkdir(parents=True)
            package = root / 'pdfs/CLASES.zip'
            package.write_bytes(b'fixture')
            with patch.dict(sys.modules, {'PackPublica': types.ModuleType('PackPublica'),
                                        'PackPublica.FTPClient': ftp, 'PackPublica.WebPublisher': web}), \
                 patch.object(self.publica, 'PROJECT_DIR', root), \
                 patch.object(empaquetado, 'verify_package', return_value={'commit': 'fixture'}), \
                 patch.object(empaquetado, 'comprobar_version'):
                self.publica.publicar_web(root / 'pdfs')
        calls = web.WebPublisher.call_args_list
        self.assertIn('.zip', calls[0].kwargs['extensions'])
        self.assertIn('.html', calls[0].kwargs['extensions'])
        self.assertTrue(any(call.kwargs['remote_dir'].endswith('/fuentes') for call in calls))
        self.assertEqual(web.WebPublisher.return_value.sync.call_count, 3)

    def test_failed_generation_stops_publication_even_if_fallback_runs(self):
        document = Mock()
        document.fichero = Path('ES_01_example.md')
        document.generar_derivados.side_effect = [RuntimeError('PDF failed'), {}]
        with self.assertRaisesRegex(RuntimeError, 'Publicación detenida'):
            self.publica.generar_derivados([document])


if __name__ == '__main__':
    unittest.main()
