"""Cálculos exactos auxiliares de CLASES. Víctor Estrada Díaz; código HL3.

https://estradad.es/licencia.php
No demuestra la identidad elíptica ni relaciones entre constantes físicas.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
from math import factorial
import argparse


def partial_sum(terms: int, b=1103, c=26390, d=396) -> Fraction:
    if terms < 1:
        raise ValueError('Se requiere al menos un término')
    if not d:
        raise ValueError('d no puede ser cero')
    return sum((Fraction(factorial(4*k), factorial(k)**4) * (b+c*k) / Fraction(d)**(4*k)
                for k in range(terms)), Fraction(0))


def pi_approximation(terms: int, precision: int = 80) -> Decimal:
    if precision < 16:
        raise ValueError('Usar al menos 16 dígitos de precisión de trabajo')
    value = partial_sum(terms)
    with localcontext() as context:
        context.prec = precision
        return +(Decimal(9801) / (2 * Decimal(2).sqrt() * Decimal(value.numerator) / Decimal(value.denominator)))


def rescale(a, b, c, scale):
    scale = Fraction(scale)
    if not scale:
        raise ValueError('La transformación requiere escala distinta de cero')
    return Fraction(a)*scale, Fraction(b)/scale, Fraction(c)/scale


def verify_identities():
    def multiply(x, y):
        return x[0]*y[0] + 29*x[1]*y[1], x[0]*y[1] + x[1]*y[0]
    result = Fraction(1), Fraction(0)
    for _ in range(6):
        result = multiply(result, (Fraction(5, 2), Fraction(1, 2)))
    checks = {
        'u^6 = 9801 + 1820 sqrt(29)': result == (9801, 1820),
        '9801^2 - 29*1820^2 = 1': 9801**2 - 29*1820**2 == 1,
        '1820*29 = 2*26390': 1820*29 == 2*26390,
        '-297*148 + 29*1820 = 8*1103': -297*148 + 29*1820 == 8*1103,
    }
    a, b, c = Fraction(2, 9801), 1103, 26390  # Factor común sqrt(2) separado.
    for scale in (Fraction(2), Fraction(-3, 7), Fraction(11, 5)):
        transformed = rescale(a, b, c, scale)
        checks[f'invariante ab/ac con escala {scale}'] = (a*b, a*c) == (transformed[0]*transformed[1], transformed[0]*transformed[2])
    return checks


def main():
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--terminos', type=int, default=3)
    parser.add_argument('--precision', type=int, default=80)
    args = parser.parse_args()
    checks = verify_identities()
    for label, passed in checks.items():
        print(('✅ ' if passed else '❌ ') + label)
    print(f'π aproximado ({args.terminos} términos; precisión de trabajo {args.precision}):')
    print(pi_approximation(args.terminos, args.precision))
    print('La precisión de trabajo no es una garantía de cifras correctas de la suma truncada.')
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
