from __future__ import print_function
import unittest as ut

from popcorn import *
from popcorn.functional import *
from IPython import embed
class AlgebraTest(ut.TestCase):
    def test_field(self):
        u = Field('u',2,1)
        self.assertEqual(u.dim,2)
        self.assertEqual(u.dim,2)
        gu = grad(u)
        self.assertTupleEqual(gu.shape, (2,2))
        
    def test_strain(self):
        u = Field('u',2,1)
        gu = grad(u)
        e = sym(gu)
        self.assertTupleEqual(e.shape, (2,2))
        tr_e = trace(e)
        
    def test_diff(self):
        u = Field('u',2,1)
        expr = inner(u,u)
        d0 = expr.diff(u[0])
        d1 = expr.diff(u[1])
        Matrix([expr]).diff(u[0])
        
    def test_diff_grad(self):
        u = Field('u',2,1)
        expr2 = inner(grad(u),grad(u))
        expr2.diff(u[0])
        Matrix([expr2]).diff(u[0])
        Matrix([expr2]).jacobian(grad(u)[:,0])

    def test_gateaux(self):
        u,tu = Field('u',2,1), Field('tu',2,1)
        expr = inner(u,u) + inner(tu,Matrix([1,0]))
        self.assertIsInstance(expr, Add)
        g = gateaux(expr,u,Matrix([[1]]),Matrix([[1],[1]]))
        