"""Verificación local de CLASES, sin red ni publicación."""
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import fuentes
import ramanujan


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.origin = base / 'UNIHOLOG'
        self.project = base / 'CLASES'
        self.origin.mkdir()
        self.project.mkdir()
        config = {'author': 'Víctor Estrada Díaz', 'license': 'https://estradad.es/licencia.php',
                  'source_project': 'UNIHOLOG', 'documents': [{'pattern': 'ES_49_*.md', 'role': 'Clases'}]}
        (self.project / 'fuentes.json').write_bytes(fuentes.encode(config))
        self.source = self.origin / 'ES_49_clases.md'
        self.content = '# Clases de equivalencia\r\n\r\n$U_ñ$ y $$a=b$$.\r\n'.encode('utf-8')
        self.source.write_bytes(self.content)
        self.target = self.project / 'documentos/UNIHOLOG' / self.source.name

    def test_copy_preserves_origin_math_and_line_endings(self):
        fuentes.synchronize(self.origin, self.project)
        self.assertEqual(self.source.read_bytes(), self.content)
        self.assertEqual(self.target.read_bytes(), self.content)
        self.assertEqual(len(fuentes.verify(self.project, self.origin)['documents']), 1)

    def test_second_run_does_not_rewrite_copies_or_manifest(self):
        fuentes.synchronize(self.origin, self.project)
        paths = [self.target, self.target.parent / 'manifest.json', self.project / 'FUENTES_UNIHOLOG.md']
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
        fuentes.synchronize(self.origin, self.project)
        self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths})

    def test_spanish_update_replaces_only_untouched_copy(self):
        fuentes.synchronize(self.origin, self.project)
        self.source.write_bytes(self.content + 'Corrección española actual.\n'.encode('utf-8'))
        with self.assertRaisesRegex(ValueError, 'origen ha cambiado'):
            fuentes.verify(self.project, self.origin)
        fuentes.synchronize(self.origin, self.project)
        self.assertEqual(self.source.read_bytes(), self.target.read_bytes())

    def test_local_edit_blocks_blind_replacement(self):
        fuentes.synchronize(self.origin, self.project)
        self.target.write_bytes(self.content + b'Local edit')
        self.source.write_bytes(self.content + b'Spanish edit')
        with self.assertRaisesRegex(ValueError, 'Copia local modificada'):
            fuentes.synchronize(self.origin, self.project)
        self.assertTrue(self.target.read_bytes().endswith(b'Local edit'))

    def test_ambiguous_or_missing_source_is_never_replaced_by_old_version(self):
        (self.origin / 'ES_49_otro.md').write_bytes(self.content)
        with self.assertRaisesRegex(ValueError, 'única fuente actual'):
            fuentes.synchronize(self.origin, self.project)
        self.assertFalse(self.target.exists())


class MathTests(unittest.TestCase):
    def test_first_partial_sum_and_positive_tail(self):
        self.assertEqual(ramanujan.partial_sum(1), Fraction(1103))
        self.assertGreater(ramanujan.partial_sum(2), ramanujan.partial_sum(1))

    def test_three_term_approximation_has_expected_leading_digits(self):
        value = ramanujan.pi_approximation(3, 80)
        self.assertLess(abs(value - Decimal('3.1415926535897932384626433832795028841971693993751')), Decimal('1e-23'))

    def test_rescaling_preserves_each_finite_sum_exactly(self):
        a, b, c = Fraction(2, 9801), 1103, 26390
        for scale in [Fraction(2), Fraction(-3, 7)]:
            aa, bb, cc = ramanujan.rescale(a, b, c, scale)
            for n in [1, 2, 4]:
                self.assertEqual(a*ramanujan.partial_sum(n, b, c), aa*ramanujan.partial_sum(n, bb, cc))

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            ramanujan.rescale(1, 2, 3, 0)
        with self.assertRaises(ValueError):
            ramanujan.partial_sum(0)

    def test_algebraic_identities_hold_exactly(self):
        self.assertTrue(all(ramanujan.verify_identities().values()))


if __name__ == '__main__':
    unittest.main()
