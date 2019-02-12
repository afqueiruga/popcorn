from popcorn import *

# A kernel for the heat equation using the
# reproducing kernel partical method

gdim = 2
II, JJ, l_edge = symbols('II JJ l_edge')

PtVec = DofSpace(gdim, 0,l_edge)
PtSca = DofSpace(1, 0,l_edge)
Param = DofSpace(1, -1)

i_x = Input('x', PtVec)
i_u = Input('u', PtSca)
i_params = Input('params', Param)

o_R = Output('R', [PtVec], 1)
o_K = Output('K', [PtVec], 1)

x0, xI = i_x.Vertex_Handles(0,II)
u0, uI = i_u.Vertex_Handles(0,II)
K = i_params.Entry_Handle(0)

rI = xI - x0
rIabs = sqrt((rI.T*rI)[0,0])

Polys = [ lambda x,y : Matrix([ 1.0, x, y ]),
          lambda x,y : Matrix([ 1.0, x, y, x**2, x*y, y**2 ])
        ]
Weights = { 'cubic' : lambda r : (1.0-r)**3 }

P = Polys[ 1 ]( *rI )
w = Weights['cubic']( rIabs )

# Set up the polynomial system
pv_RHS = PopcornVariable('RHS', len(P), 1 )
pv_M   = PopcornVariable('M', len(P), 2 )
pv_Mi  = PopcornVariable('Mi', len(P), 2 )
pv_a   = PopcornVariable('a', len(P), 1 )
RHS_expr = w * P * uI
M_expr = w * P * P.T

class gsl_linalg_LU_decomp():
    def __init__(self, Alu, A):
        self.Alu = Alu
        self.A   = A
    def emit(self):
        return """
        gsl_matrix_view gsl_mat_{name} 
          = gsl_matrix_view_array( {name}, {size}, {size} );
        gsl_permutation * gsl_p_{name}
          = gsl_permutation_alloc( {size} );
        int gsl_s_{name};

        gsl_linalg_LU_decomp(&gsl_mat_{name}.matrix, gsl_p_{name}, &gsl_s_{name});
        """.format(name=A.name, size=A.dim)
    
class gsl_linalg_LU_solve():
    def __init__(self, Alu, x, R):
        self.Alu = Alu
        self.x = x
        self.R = R
    def emit(self):
        return """
        
        """
class gsl_mat_solve():
    def __init__(self, A, x, R):
        self.A = A
        self.x = x
        self.R = R
    def emit(self):
        return """
        {{
        gsl_vector_view gsl_vec_{R} 
         = gsl_vector_view_array( {R}, {n} );
        gsl_vector_view gsl_vec_{x} 
         = gsl_vector_view_array( {x}, {n} );
        gsl_matrix_view gsl_mat_{A} 
          = gsl_matrix_view_array( {A}, {n}, {n} );
        gsl_permutation * gsl_p_{A}
          = gsl_permutation_alloc( {n} );
        int gsl_s_{A};

        gsl_linalg_LU_decomp(&gsl_mat_{A}.matrix, gsl_p_{A}, &gsl_s_{A});
        gsl_linalg_LU_solve( &gsl_mat_{A}.matrix, gsl_p_{A}, 
                             &gsl_vec_{R}.vector,
                             &gsl_vec_{x}.vector );

        gsl_permutation_free(gsl_p_{A});
        }}
        """.format(A=self.A.name, x=self.x.name, R=self.R.name, n=self.A.dim)
prgm = [
    pv_M,
    pv_RHS,
    pv_a,
    Loop(II,0,l_edge, [
        Asgn( pv_RHS, RHS_expr, '+='),
        Asgn( pv_M,   M_expr, '+=')
    ]),
    gsl_mat_solve(pv_M, pv_a, pv_RHS ),
    DebugPrint(pv_M),
    DebugPrint(pv_a)
    #GSL_Mat_LU_decomp( pv_Mi, pv_M)
    #GSL_Mat_LUSolve( pv_M, pv_a, pv_RHS)
]

kernel_rkpm2 = Kernel("rkpm",
                              [i_x, i_u, i_params],
                              [o_R, o_K],
                              listing=prgm)

# Write a husk
from popcorn import boilerplates
Husk("rkpm", [ kernel_rkpm2 ])
