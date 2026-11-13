"""Exemple associé au ticket OpenProject fourni."""


def divide(a, b):
    if b == 0:
        raise ValueError("division par zero")
    return a / b


def substract(a, b):
    return a - b


def square_root(a):
    if a < 0:
        raise ValueError("racine carrée d'un nombre négatif")
    return a ** 0.5
