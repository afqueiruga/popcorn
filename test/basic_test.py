import unittest as ut

from popcorn import *

class MakeSpringHusk(ut.TestCase):
    def test_generate(self):
        Vector = DofSpace(2,0,2) # vector on each vertex
        Param  = DofSpace(1,-1) # global
        i_x = Input('x',Vector) # original position
        i_y = Input('y',Vector) # new position
        i_k = Input('k',Param) # stiffness
        x0,x1 = i_x.Vertex_Split()
        y0,y1 = i_y.Vertex_Split()
        norm = lambda a : sqrt( (a.T*a)[0,0] )
        f = i_k[0] * (norm(y0-y1)-norm(x0-x1))/norm(y0-y1) * (y1-y0)
        R = Matrix([f,-f])
        K = R.jacobian(i_y) # <---- Take a symbolic derivative!
        o_R = Output('R',[Vector],1)
        o_K = Output('K',[Vector],2)
        Kernel("spring_force",
                   listing=[
                       Asgn(o_R,R,'='),
                       Asgn(o_K,K,'=')
                       ])
        Husk('spring')
        # import husk_spring
        
