import unittest as ut

from popcorn import *
from popcorn.functional import *

class PatternsTest(ut.TestCase):
    def test_fixed(self):
        Fixed = DofSpace(1,0,2)
        i_a = Input('a',Fixed)
        o_y = Output('y',[Fixed],1)
        Kernel('foobar',listing=[
            Asgn(o_y,2*i_a)
        ])
        Husk('foobar')
        