# -*- coding: utf8 -*-

from __future__ import division
from math import sqrt
from smallvectors import dot, Vec
from smallshapes.circle import Circle

__all__ = ['AABB', 'mAABB',
           'aabb_rect', 'aabb_bbox',
           'aabb_pshape', 'aabb_shape', 'aabb_center']

direction_x = Vec(1, 0)
direction_y = Vec(0, 1)


class AABBBase(object):

    '''Classe pai para AABB e mAABB'''

    # if C.compiled:
    #    __slots__ = []
    # else:
    __slots__ = ['xmin', 'xmax', 'ymin', 'ymax']

    def __init__(self,
                 xmin=None, xmax=None, ymin=None, ymax=None,
                 bbox=None, rect=None, shape=None, pos=None):

        self.xmin, self.xmax, self.ymin, self.ymax = map(
            float, aabb_bbox(xmin, xmax, ymin, ymax, bbox, rect, shape, pos)
        )

    #@C.locals(xmax='double', xmin='double', ymax='double', ymin='double')
    @classmethod
    def _constructor(cls, xmin, xmax, ymin, ymax):
        new = AABB.__new__(cls)
        new.xmin = xmin
        new.xmax = xmax
        new.ymin = ymin
        new.ymax = ymax
        assert xmin <= xmax
        assert ymin <= ymax
        return new

    @property
    def bbox(self):
        return (self.xmin, self.xmax, self.ymin, self.ymax)

    #@C.locals(width='double', height='double')
    @property
    def shape(self):
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        return width, height

    @property
    def rect(self):
        return (self.xmin, self.ymin,
                self.xmax - self.xmin, self.ymax - self.ymin)

    #@C.locals(x='double', y='double')
    @property
    def pos(self):
        x = (self.xmin + self.xmax) / 2
        y = (self.ymin + self.ymax) / 2
        return Vec(x, y)

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
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin

    @property
    def vertices(self):
        return (Vec(self.xmin, self.ymin), Vec(self.xmax, self.ymin),
                Vec(self.xmax, self.ymax), Vec(self.xmin, self.ymax))

    @property
    def radius_cbb(self):
        return sqrt(
            (self.xmax - self.xmin) ** 2 + (self.ymax - self.ymin) ** 2) / 2

    @property
    def aabb(self):
        return self

    @property
    def cbb(self):
        return Circle(self.radius_cbb, self.pos)

    # Magic methods ###########################################################
    def __repr__(self):
        data = '%.1f, %.1f, %.1f, %.1f' % self.bbox
        return 'AABB([%s])' % data

    def _eq(self, other):
        xmin, xmax, ymin, ymax = other
        return ((xmin == self.xmin) and (xmax == self.xmax)
                and (ymin == self.ymin) and (ymax == self.ymax))

    def __richcmp__(self, other, method):
        if method == 2:
            return self._eq(other)
        elif method == 3:
            return not self._eq(other)
        raise

    def __iter__(self):
        yield self.xmin
        yield self.xmax
        yield self.ymin
        yield self.ymax

    def __len__(self):
        return 4

    # Métodos utilizado pelo SAT ##############################################
    def directions(self, n):
        '''Retorna a lista de direções exaustivas para o teste do SAT
        associadas ao objeto.

        A rigor esta lista é infinita para um círculo. Retornamos uma lista
        vazia de forma que somente as direções do outro objeto serão
        consideradas'''

        return [direction_x, direction_y]

    def shadow(self, n):
        '''Retorna as coordenadas da sombra na direção n dada.
        Assume n normalizado.'''

        points = [dot(n, p) for p in self.vertices]
        return min(points), max(points)

    # Transformações geométricas ##############################################
    def move(self, delta_or_dx, dy=None):
        '''Retorna uma outra AABB deslocada pelas coordenadas (dx, dy)
        fornecidas'''

        if dy is None:
            dx, dy = delta_or_dx
        else:
            dx = delta_or_dx
        return self._constructor(self.xmin + dx, self.xmax + dx,
                                 self.ymin + dy, self.ymax + dy)

    def rotate(self, theta):
        '''Retorna o objeto rotacionado pelo ângulo fornecido'''

        if theta != 0:
            raise ValueError('cannot rotate AABB')
        return self.copy()

    def rescale(self, scale):
        '''Retorna um objeto modificado pelo fator de escala fornecido'''

        x, y = self.pos
        dx, dy = self.shape
        dx *= scale / 2
        dy *= scale / 2
        return self._constructor(x - dx, x + dx, y - dy, y + dy)

    # Cálculo de distâncias ###################################################
    def distance_center(self, other):
        '''Retorna a distância entre centros de duas AABBs.'''

        return (self.pos - other.pos).norm()

    def distance_aabb(self, other):
        '''Retorna a distância para outra AABB. Zero se elas se interceptam'''

    # Pontos de intersecção ###################################################

    def intercepts_aabb(self, other):
        '''Retorna True caso os dois objetos se interceptem'''

    def intercepts_point(self, point, tol=1e-6):
        '''Retorna True se o ponto está na linha que forma a AABB a menos de
        uma margem de tolerância tol.'''

    # Contêm figuras ##########################################################

    def contains_aabb(self, other):
        '''Retorna True se o argumento está contido na AABB.'''

        cpoint = self.contains_point
        x, y, xm, ym = other
        return (cpoint(x, y) and cpoint(x, ym)
                and cpoint(xm, y) and cpoint(xm, ym))

    def contains_circle(self, other):
        '''Retorna True se o argumento está contido na AABB.'''

        cpoint = self.contains_point
        x, y, xm, ym = other
        return (cpoint(x, y) and cpoint(x, ym)
                and cpoint(xm, y) and cpoint(xm, ym))

    def contains_point(self, point):
        '''Retorna True se o ponto está contido na AABB.'''

        x, y = point
        return ((self.xmin <= x <= self.xmax)
                and (self.ymin <= y <= self.ymax))

    # Sombras e projeções #####################################################
    def shadow_x(self):
        return (self.xmin, self.xmax)

    def shadow_y(self):
        return (self.ymin, self.ymax)


class AABB(AABBBase):

    '''Representa uma caixa de contorno retangular alinhada aos eixos.

    Atributos
    ---------

    xmin, xmax, ymin, ymax
        Limites da AABB
    bbox
        Tupla com (xmin, xmax, ymin, ymax)
    shape
        Tupla com (largura, altura)
    pos
        Posição do centro da AABB
    pos_sw, pos_se, pos_ne, pos_nw,
        Posições dos extremos da AABB nas direções sudoeste, sudeste, nordeste
        e noroeste
    vertices
        Tupla com os quatro vétices acima que formam a AABB
    radius_cbb
        Raio do círculo de contorno que envolve o objeto cujo centro é dado
        por pos


    Exemplos
    --------

    Objetos do tipo AABB podem ser inicializados a partir das coordenadas
    (xmin, xmax, ymin, ymax) ou especificando qualquer conjunto de parâmetros
    que permita a construção da caixa de contorno.

    Todas os construtores abaixo são equivalentes

    >>> a = AABB(0, 50, 0, 100)
    >>> b = AABB((0, 50, 0, 100))
    >>> c = AABB(bbox=(0, 50, 0, 100))
    >>> d = AABB(pos=(25, 50), shape=(50, 100))
    >>> e = AABB(rect=(0, 0, 50, 100))

    #TODO
    #>>> a == b == c == d == e
    #True

    '''

    def copy(self):
        return self


class mAABB(AABBBase):

    '''Mutable version of AABB'''

    def copy(self):
        return self._constructor(self.xmin, self.xmax, self.ymin, self.ymax)

    def imove(self, delta_or_dx, dy=None):
        '''Move a AABB *inplace*'''

        if dy is None:
            dx, dy = delta_or_dx
        else:
            dx = delta_or_dx

        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy

    @AABBBase.pos.setter
    def pos(self, value):
        self.imove(value - self.pos)


# if not C.compiled:
#    @pyinject(globals())
#    class AABBInject:
#
#        def __eq__(self, other):
#            return self._eq(other)

###############################################################################
# Extrai caixas de contorno a partir das entradas
###############################################################################


def aabb_bbox(xmin=None, xmax=None,
              ymin=None, ymax=None,
              bbox=None, rect=None,
              shape=None, pos=None):
    '''
    Retorna a caixa de contorno (xmin, xmax, ymin, ymax) a partir dos
    parâmetros fornecidos.
    '''

    if (xmin is not None) and (xmax is None):
        bbox = xmin
        xmin = None
    if bbox is not None:
        xmin, xmax, ymin, ymax = bbox
    elif shape is not None:
        pos = pos or (0, 0)
        dx, dy = map(float, shape)
        x, y = pos
        xmin, xmax = x - dx / 2., x + dx / 2.
        ymin, ymax = y - dy / 2., y + dy / 2.
    elif rect is not None:
        xmin, ymin, dx, dy = map(float, rect)
        xmax = xmin + dx
        ymax = ymin + dy
    elif None not in (xmin, xmax, ymin, ymax):
        pass
    else:
        raise TypeError('either shape, bbox or rect  must be defined')

    return (xmin, xmax, ymin, ymax)


def aabb_rect(xmin=None, xmax=None,
              ymin=None, ymax=None,
              bbox=None, rect=None,
              shape=None, pos=None):
    '''
    Retorna o rect  (xmin, ymin, width, height) a partir dos parâmetros
    fornecidos.
    '''

    x, xmax, y, ymax = aabb_bbox(xmin, xmax, ymin, ymax,
                                 bbox, rect, shape, pos)
    return (x, y, xmax - x, ymax - y)


def aabb_pshape(xmin=None, xmax=None,
                ymin=None, ymax=None,
                bbox=None, rect=None,
                shape=None, pos=None):
    '''
    Retorna uma tupla de (centro, shape) a partir dos parâmetros fornecidos.
    '''
    x, xmax, y, ymax = aabb_bbox(xmin, xmax, ymin, ymax,
                                 bbox, rect, shape, pos)
    center = Vec((x + xmax) / 2.0, (y + ymax) / 2.0)
    shape = (xmax - x, ymax - y)
    return center, shape


def aabb_center(bbox=None, rect=None,
                shape=None, pos=None,
                xmin=None, xmax=None,
                ymin=None, ymax=None):
    '''
    Retorna um vetor com a posição do centro da caixa de contorno.
    '''

    return aabb_pshape(xmin, ymin, xmax, ymax, bbox, rect, shape, pos)[0]


def aabb_shape(bbox=None, rect=None,
               shape=None, pos=None,
               xmin=None, xmax=None,
               ymin=None, ymax=None):
    '''
    Retorna uma tupla (width, height) com o formato da caixa de contorno.
    '''

    return aabb_shape(xmin, ymin, xmax, ymax, bbox, rect, shape, pos)[1]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
