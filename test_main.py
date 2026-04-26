import unittest
from main import somar, subtrair, multiplicar, dividir


class TestCalculadora(unittest.TestCase):

    def test_soma(self):
        self.assertEqual(somar(2, 3), 5)

    def test_subtracao(self):
        self.assertEqual(subtrair(5, 3), 2)

    def test_multiplicacao(self):
        self.assertEqual(multiplicar(4, 3), 12)

    def test_divisao(self):
        self.assertEqual(dividir(10, 2), 5)

    def test_divisao_por_zero(self):
        with self.assertRaises(ValueError):
            dividir(10, 0)


if __name__ == "__main__":
    unittest.main()