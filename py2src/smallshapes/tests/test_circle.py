# -*- coding: utf8 -*-
from smallshapes.tests.test_base import LocatableBase, HasAABBBase
from smallshapes import Circle, mCircle
import unittest


class CircleTest(LocatableBase, HasAABBBase, unittest.TestCase):
    mutable_cls = mCircle
    immutable_cls = Circle
    args = (2.5, (0, 1))
    aabb_args = (0.5, (0.5, 1.5))


del HasAABBBase, LocatableBase

            
if __name__ == '__main__':
    unittest.main()
    