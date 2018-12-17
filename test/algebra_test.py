from __future__ import print_function
import unittest as ut

from popcorn import *
from popcorn.functional import *
from IPython import embed
class AlgebraTest(ut.TestCase):
    def test_field(self):
        pass
    def test_strain(self):
        u = Field('u',2,1)
        print(u)
        self.assertEqual(u.dim,2)
        gu = grad(u)
        print(gu)
        self.assertTupleEqual(gu.shape, (2,2))
        e = sym(gu)
        self.assertTupleEqual(e.shape, (2,2))

        print(e)
        # embed()
        tr_e = trace(e)
        
        