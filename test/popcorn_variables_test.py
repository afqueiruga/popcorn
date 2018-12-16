import unittest as ut

from popcorn import *
from popcorn.functional import *

class InitializeInputs(ut.TestCase):
    def test_fixed_size(self):
        FixedSingle = DofSpace(1,0,1)
        i_a = Input('a',FixedSingle)
        self.assertEqual(i_a.dim,1)
        
        FixedTwo = DofSpace(1,0,2)
        i_b = Input('b',FixedTwo)
        self.assertEqual(i_b.dim,2)
        
        FixedVec = DofSpace(2,0,1)
        i_c = Input('c',FixedTwo)
        self.assertEqual(i_c.dim,2)
        
    def test_variable_size(self):
        VariableScalar = DofSpace(1,0)
        i_d = Input('d',VariableScalar)
        
    def test_field(self):
        scalar = Field('scalar',1,0)
        self.assertTupleEqual(scalar.shape,(1,1))
        self.assertEqual(scalar.dim,1)
        
        vector1d = Field('vector1d',1,1)
        self.assertTupleEqual(vector1d.shape,(1,1))
        self.assertEqual(vector1d.dim,1)
        
        vector2d = Field('vector2d',2,1)
        self.assertTupleEqual(vector2d.shape,(2,1))
        self.assertEqual(vector2d.dim,2)