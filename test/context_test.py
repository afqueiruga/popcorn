import unittest as ut

from popcorn import *
from popcorn.functional import *

class ConextTest(ut.TestCase):
    def fails_test_variables(self):
        with Husk_ctx('first_husk'):
            Fixed = DofSpace(1,0,1)
            i_a_1 = Input('a',Fixed)
        with Husk_ctx('second_husk'):
            Fixed = DofSpace(2,0,1)
            i_a_2 = Input('a',Fixed)
        self.assertEqual(i_a_2.dim, 2)
        self.assertEqual(i_a_1.dim, 1)

    def fails_test_kernels(self):
        with Husk_ctx('first_husk'):
            Kernel('a')
            self.assertEqual(len(popcorn_globals.registered_kernels), 1)

        with Husk_ctx('second_husk'):
            Kernel('a')
            Kernel('b')
            self.assertEqual(len(popcorn_globals.registered_kernels), 2)
