# -*- coding: utf8 -*-
from smallshapes.tests.test_base import LocatableBase, HasAABBBase
from smallshapes import Poly, mPoly, PolyAny, center_of_mass
import unittest


class PolyTest(LocatableBase, HasAABBBase, unittest.TestCase):
    mutable_cls = mPoly
    immutable_cls = Poly
    args = aabb_args = ((0, 1), (1, 1), (0, 2))
    

def test_basic_poly_funcionality():
    tri = Poly((0, 0), (3, 0), (0, 3))
    assert list(tri) == [(0, 0), (3, 0), (0, 3)]
    assert list(tri.flat) == [0, 0, 3, 0, 0, 3]
    assert tri[0] == (0, 0)
    assert tri[1] == (3, 0)
    assert tri[2] == (0, 3)
    assert tri[-1] == (0, 3)
    
def test_poly_center_of_mass():
    tri = Poly((0, 0), (3, 0), (0, 3))
    assert tri.pos == center_of_mass([(0, 0), (3, 0), (0, 3)])
    assert tri.pos == (1, 1)
    
def test_poly_aabb():
    tri = Poly((0, 0), (3, 0), (0, 3))
    assert list(tri.aabb) == [0, 3, 0, 3]

    tri = Poly((0, 0), (4, 0), (0, 3))
    L = list(tri.aabb)
    assert L == [0, 4, 0, 3]

if __name__ == '__main__':
    from pytest import main
    main('-ra -q -l')
    