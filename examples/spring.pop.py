from popcorn import *
# This is an example of a spring-law, the simplest possible kernel
# The edge is fixed-length and looks like this:
#
# P0 ---- P1
#

# This will generate any dimension
gdim = 2

# Set up the DofSpaces. These say what sort of data lives on the edge.
# These are sort-of Typedefs
PtSca = DofSpace(   1,0,2) # a sclar field associated with P0 and P1 ( 2 numbers )
PtVec = DofSpace(gdim,0,2) # a vector field associated with P0 and P1 ( 4 numbers )
Param = DofSpace(2,-1) # a field to input global parameters. 2 numbers, not associated with a vertex

i_x = Input("x", PtVec)
i_params = Input("params",Param)

o_R = Output("R", [PtVec], 1)
o_K = Output("K", [PtVec], 2)

x0,x1 = i_x.Vertex_Handles(0,1) # Split into blocks of gdim
K, L0 = i_params.Entry_Handles(0,1) # split into each entry in the vector

r = x1 - x0
rabs = sqrt((r.T*r)[0,0])

f_expr = K*(rabs-L0) * r/rabs

R_expr = Matrix([ f_expr, -f_expr])
K_expr = R_expr.jacobian( i_x.as_matrix() )

prgm = [
    Asgn(o_R, R_expr, "+="),
    Asgn(o_K, K_expr, "+=")
    ]

kernel_linear_spring = Kernel("linear_spring",
                              [i_x, i_params],
                              [o_R, o_K],
                              listing=prgm)

# Write a husk
Husk("pair_bond", [ kernel_linear_spring ])
# There's now a folder filled with files. Look at 'em.
# You have the following options:
# 1) cd into the folder and type "make". That'll use swig
#    to turn that folder into a python module.
# 2) Copy and paste the .c and .h files whereever you want
# 3) In your CMakeLists.txt, add_subdirectory(husk_pair_bond) to populate
#    KERNEL_FILES and KERNEL_INCLUDES in your build system
