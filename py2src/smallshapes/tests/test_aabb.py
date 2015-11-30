# -*- coding: utf8 -*-
from smallshapes.tests.test_base import LocatableBase, HasAABBBase
from smallshapes import AABB, mAABB, aabb_bbox
import unittest
import pytest

class AABBTest(LocatableBase, HasAABBBase, unittest.TestCase):
    mutable_cls = mAABB
    immutable_cls = AABB
    args = (0, 1, 0, 2)
    aabb_args = (0, 1, 1, 2)


del HasAABBBase, LocatableBase


def test_aabb_func():
    assert aabb_bbox(1, 2, 3, 4) == (1, 2, 3, 4)
    assert aabb_bbox(shape=(10, 20)) == (-5, 5, -10, 10)
    assert aabb_bbox(bbox=(1, 2, 3, 4)) == (1, 2, 3, 4)


if __name__ == '__main__':
    pytest.main('test_aabb.py -q')
    