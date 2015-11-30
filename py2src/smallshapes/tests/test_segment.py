# -*- coding: utf8 -*-
from smallshapes.tests.test_base import LocatableBase, HasAABBBase
from smallshapes import Segment, mSegment
import unittest


class SegmentTest(LocatableBase, HasAABBBase, unittest.TestCase):
    mutable_cls = mSegment
    immutable_cls = Segment
    args = ((0, 1), (1, 2))
    aabb_args = ((0, 1), (1, 2))     
     
     
del HasAABBBase, LocatableBase

            
if __name__ == '__main__':
    unittest.main()
    