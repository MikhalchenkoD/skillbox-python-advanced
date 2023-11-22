import unittest
from python_advanced.module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt


class TestCorrectDecryption(unittest.TestCase):
    def test_get_correct_decryption_with_one_point(self):
        self.assertEqual(decrypt('абра-кадабра.'), 'абра-кадабра')
        self.assertEqual(decrypt('.'), '')

    def test_get_correct_decryption_with_two_point(self):
        self.assertEqual(decrypt('абраа..-кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абра--..кадабра'), 'абра-кадабра')

    def test_get_correct_decryption_with_three_and_more_point(self):
        self.assertEqual(decrypt('абраа..-.кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абрау...-кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абра........'), '')
        self.assertEqual(decrypt('абр......а.'), 'а')
        self.assertEqual(decrypt('1..2.3'), '23')
        self.assertEqual(decrypt('1.......................'), '')