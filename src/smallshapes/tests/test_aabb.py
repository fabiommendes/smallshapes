from smallshapes.tests.test_base import LocatableBase, HasAABBBase
from smallshapes import AABB, mAABB
import unittest


class AABBTest(LocatableBase, HasAABBBase):
    mutable_cls = mAABB
    immutable_cls = AABB
    args = (0, 1, 0, 2)
    aabb_args = (0, 1, 1, 2)


del HasAABBBase, LocatableBase

            
if __name__ == '__main__':
    unittest.main()
    