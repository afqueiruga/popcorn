import unittest as ut

from popcorn import *
from popcorn.functional import *

class PatternsTest(ut.TestCase):
    def test_fixed(self):
        Fixed = DofSpace(1,0,2)
        i_a = Input('a1',Fixed)
        o_y = Output('y1',[Fixed],1)
        Kernel('pattern_fixed',listing=[
            Asgn(o_y,2*i_a)
        ]).Write_Module()
        
    def test_variable_view_scalar(self):
        Variable = DofSpace(1,0)
        i_b = Input('b1',Variable)
        o_z = Output('z1',[Variable],1)
        II, l_edge = symbols('II l_edge')
        Kernel('foobar2',listing=[
            Loop(II,0,l_edge,[
                Asgn(o_z.View((II,)),Matrix([2*i_b[II]]) )
            ])
        ]).Write_Module()
        
        
    def test_variable_view_vector(self):
        Variable = DofSpace(3,0)
        i_b = Input('b2',Variable)
        o_z = Output('z2',[Variable],1)
        II, l_edge = symbols('II l_edge')
        Kernel('foobar3',listing=[
            Loop(II,0,l_edge,[
                Asgn(o_z.View((II,)),Matrix([2*i_b[II]]) )
            ])
        ]).Write_Module()
        
    
    def TODO_test_variable_3(self):
        # TODO I want this to work
        Variable = DofSpace(3,0)
        i_b = Input('b3',Variable)
        o_z = Output('z3',[Variable],1)
        II, l_edge = symbols('II l_edge')
        Kernel('foobar4',listing=[
            Loop(II,0,l_edge,[
                Asgn( o_z[II],2*i_b[II] )
            ])
        ]).Write_Module()
        
    def test_variable_expr(self):
        II, l_edge = symbols('II l_edge')
        Variable = DofSpace(3,0)
        i_b = Input('b4',Variable)
        bv = i_b.Vertex_Handle(II)
        o_z = Output('z4',[Variable],1)
        expr = Matrix([trace(i_b * i_b.T)])
        
        Kernel('foobar5',listing=[
            Loop(II,0,l_edge,[
                Asgn( o_z.View((II,)), expr )
            ])
        ]).Write_Module()
