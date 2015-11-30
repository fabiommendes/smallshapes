# -*- coding: utf8 -*-
from smallvectors import Vec


class HasAABB(object):

    '''
    Shape objects can define a AABB and properties defining the extreme points
    of the boundary.
    '''

    __slots__ = ()
    
    #
    # Main entry point
    #
    @property
    def aabb(self):
        return self.__aabb_t__(self.xmin, self.xmax, self.ymin, self.ymax)

    #
    # Scalar positions
    #    
    @property
    def xmin(self):
        return self.aabb.xmin

    @property
    def xmax(self):
        return self.aabb.xmax

    @property
    def ymin(self):
        return self.aabb.ymin

    @property
    def ymax(self):
        return self.aabb.ymax

    #
    # Vector positions
    #
    @property
    def pos_sw(self):
        return Vec(self.xmin, self.ymin)

    @property
    def pos_se(self):
        return Vec(self.xmax, self.ymin)

    @property
    def pos_nw(self):
        return Vec(self.xmin, self.ymax)

    @property
    def pos_ne(self):
        return Vec(self.xmax, self.ymax)

    @property
    def pos_right(self):
        return Vec(self.xmax, self.pos.y)

    @property
    def pos_left(self):
        return Vec(self.xmin, self.pos.y)

    @property
    def pos_up(self):
        return Vec(self.pos.x, self.ymax)

    @property
    def pos_down(self):
        return Vec(self.pos.x, self.ymin)

    #
    # Vector setters: set the value of the given reference point
    #
    pos_sw = pos_sw.setter(lambda obj, v: obj.move(v - obj.pos_sw))
    pos_nw = pos_nw.setter(lambda obj, v: obj.move(v - obj.pos_nw))
    pos_se = pos_se.setter(lambda obj, v: obj.move(v - obj.pos_se))
    pos_ne = pos_ne.setter(lambda obj, v: obj.move(v - obj.pos_ne))
    pos_up    = pos_up.setter(lambda obj, v: obj.move(v - obj.pos_up))
    pos_down  = pos_down.setter(lambda obj, v: obj.move(v - obj.pos_down))
    pos_right = pos_right.setter(lambda obj, v: obj.move(v - obj.pos_right))
    pos_left  = pos_left.setter(lambda obj, v: obj.move(v - obj.pos_left))
    
    #
    # Shape parameters
    #
    @property
    def bbox(self):
        return (self.xmin, self.xmax, self.ymin, self.ymax)

    @property
    def shape(self):
        return (self.xmax - self.xmin, self.ymax - self.ymin)

    @property
    def rect(self):
        x, y = self.xmin, self.ymin
        return (x, y, self.xmax - x, self.ymax - y)
    
    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin
