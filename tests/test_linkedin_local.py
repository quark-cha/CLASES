"""Las variantes LinkedIn son locales y las ediciones del autor se conservan."""
from contextlib import nullcontext
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import linkedin
import empaquetado


class LocalLinkedInTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.base = self.project / 'ES_01_example.md'
        self.text = '# Clases $U_c$\r\n\r\n$$a=b$$\r\n'.encode('utf-8')
        self.base.write_bytes(self.text)
        self.variant = self.project / 'ES_01_example_linkedin.md'

    def record(self):
        state_file, state, items = linkedin.preparar_variantes(self.project)
        variant, base, source_hash, data, automatic, _ = items[0]
        state[variant.name] = dict(source_sha256=source_hash, variant_sha256=linkedin.sha(data), automatic=automatic)
        state_file.parent.mkdir(exist_ok=True)
        state_file.write_text(json.dumps(state), encoding='utf-8')

    def test_initial_variant_preserves_exact_source_and_math(self):
        linkedin.preparar_variantes(self.project)
        self.assertEqual(self.variant.read_bytes(), self.text)
        self.assertEqual(self.base.read_bytes(), self.text)

    def test_untouched_variant_tracks_current_base(self):
        self.record()
        self.base.write_bytes(self.text + b'Current correction')
        linkedin.preparar_variantes(self.project)
        self.assertEqual(self.base.read_bytes(), self.variant.read_bytes())

    def test_author_edit_is_not_overwritten_by_base_change(self):
        self.record()
        manual = self.text + b'Own edition'
        self.variant.write_bytes(manual)
        self.base.write_bytes(self.text + b'New base')
        with self.assertRaisesRegex(ValueError, 'edición propia'):
            linkedin.preparar_variantes(self.project)
        self.assertEqual(self.variant.read_bytes(), manual)
        linkedin.preparar_variantes(self.project, revisado=True)
        self.assertEqual(self.variant.read_bytes(), manual)

    def test_suffix_without_underscore_is_recognized_and_does_not_duplicate_variant(self):
        variant = self.project / 'ES_01_exampleLinkedIn.md'
        variant.write_bytes(self.text)
        items = linkedin.preparar_variantes(self.project)[2]
        self.assertEqual([item[0] for item in items], [variant])
        self.assertEqual(items[0][1], self.base)
        self.assertFalse(self.variant.exists())

    def test_normal_publication_does_not_create_extra_variants(self):
        self.assertEqual(linkedin.preparar_variantes(self.project, crear=False)[2], [])
        self.assertFalse(self.variant.exists())

    def test_generated_variants_are_not_eligible_for_project_archive(self):
        for name in ['ES_01_example_linkedin.md', 'ES_01_example_LINKEDIN.pdf',
                     'linkedin/ES_01_example.pdf', 'pdfs/ES_01_example_LinkedIn.html', 'ES_01_examplelinkedin.md',
                     'ES_01_example-LinkedIn.pdf', 'ES_01_example.LinkedIn.html']:
            self.assertFalse(empaquetado.eligible(name), name)
        self.assertTrue(empaquetado.eligible('ES_01_example.md'))
        self.assertTrue(empaquetado.eligible('src/linkedin.py'))
        self.assertTrue(empaquetado.eligible('tests/test_linkedin_local.py'))

    def test_completed_pdf_skips_rendering_when_variant_is_unchanged(self):
        publisher = Mock()
        rendered = publisher.test.return_value.html.return_value
        rendered.contenido = '<html><head></head><body>Texto</body></html>'
        rendered.pdf.return_value.save.side_effect = lambda path: Path(path).write_bytes(b'%PDF fixture')
        module = types.ModuleType('PackPublica.logging')
        module.document_work = lambda path: nullcontext()
        with patch.dict(sys.modules, {'PackPublica': types.ModuleType('PackPublica'), 'PackPublica.logging': module}):
            outputs = linkedin.generar_linkedin(self.project, publisher)
            before = outputs[0].read_bytes(), outputs[0].stat().st_mtime_ns
            publisher.test.reset_mock()
            linkedin.generar_linkedin(self.project, publisher)
            publisher.test.assert_not_called()
            self.assertEqual(before, (outputs[0].read_bytes(), outputs[0].stat().st_mtime_ns))

    def test_catalog_and_web_filter_only_linkedin_variants(self):
        spec = importlib.util.spec_from_file_location('clases_publica_linkedin_test', ROOT / 'publica.py')
        publica = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(publica)
        normal = Mock(fichero=self.base)
        social = Mock(fichero=self.variant)
        self.variant.write_bytes(self.text)
        with patch.object(publica, 'PROJECT_DIR', self.project):
            publica.generar_catalogo_cat([normal, social])
        catalog = (self.project / 'catalogo.cat').read_text(encoding='utf-8')
        self.assertNotIn('Linkedin', catalog)
        self.assertEqual(len(catalog.splitlines()), 2)

    def test_real_web_hash_selection_excludes_only_social_variants(self):
        spec = importlib.util.spec_from_file_location('clases_publica_web_filter_test', ROOT / 'publica.py')
        publica = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(publica)
        from PackPublica.WebPublisher import WebPublisher
        self.variant.write_bytes(self.text)
        pdfs = self.project / 'pdfs'
        pdfs.mkdir()
        (pdfs / 'ES_01_example.pdf').write_bytes(b'normal')
        (pdfs / 'ES_01_example_LinkedIn.pdf').write_bytes(b'local social')
        (pdfs / 'CLASES.zip').write_bytes(b'package fixture')
        ftp = types.ModuleType('PackPublica.FTPClient')
        ftp.FTPClient = Mock()
        publica.PUBLICAR_WEB = True
        selected = []
        def local_hashes(publisher):
            selected.append(publisher.compute_local_hashes())
        with patch.dict(sys.modules, {'PackPublica.FTPClient': ftp}), \
             patch.object(publica, 'PROJECT_DIR', self.project), \
             patch.object(empaquetado, 'verify_package', return_value={'commit': 'fixture'}), \
             patch.object(empaquetado, 'comprobar_version'), \
             patch.object(WebPublisher, 'sync', local_hashes):
            publica.publicar_web(pdfs)
        self.assertIn('ES_01_example.pdf', selected[0])
        self.assertNotIn('ES_01_example_LinkedIn.pdf', selected[0])
        self.assertIn(self.base.name, selected[1])
        self.assertNotIn(self.variant.name, selected[1])
