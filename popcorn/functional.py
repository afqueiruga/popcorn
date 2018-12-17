"""
Generic tools for functional implementation

"""
from .PopcornVariable import PopcornVariable
from sympy import Matrix, eye
from . import popcorn_globals

class Field( PopcornVariable):
    def __new__(cls, name, gdim, rank):
        C = super(Field,cls).__new__(cls, 'field_'+name, gdim,rank)
        C.pv_grad_u = None
        # popcorn_globals.registered_fields.add(C)
        popcorn_globals.registered_fields[C.name] = C
        return C
    def grad(self):
        if self.pv_grad_u is None:
            self.pv_grad_u = PopcornVariable('grad_'+ self.name, self.dim, self.rank+1)
        return self.pv_grad_u
    
def extract(P, u, grad_u,   NJ, grad_NJ,
               tu, grad_tu, NI, grad_NI):
    gdim = len(grad_u)
    RI = Matrix([P]).jacobian(grad_tu).dot( grad_NI ) \
     + P.diff(tu) * NI
    KIJ = Matrix([RI]).jacobian(grad_u).dot( grad_NJ ) \
      + P.diff(u) * NJ

    return RI, KIJ

def gateaux(f, u, N, dNdx):
    R = [ Matrix([f]).diff(ui) * NA + Matrix([f]).jacobian(grad(u)[:,i]) * dNdx[:,A]
              for A,NA in enumerate(N)
              for i,ui in enumerate(u) ]
    # TODO: Reshape this guy
    return Matrix(R)

#
# Helper for subs on matrices
#
component_sub = lambda F,V : { a:b for a,b in zip(F,V) }
def dict_cat(*args):
    d = {}
    for a in args: d.update(a)
    return d
def field_keys( *args ):
    return dict_cat(*[
        component_sub(f,e) for f,e in args
        ])

#
# Additional tensor expressions
#
def inner(A,B):
    s = 0
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            s += A[i,j]*B[i,j]
    return s
def sym(A):
    return 0.5 * ( A + A.T )
def dev(A):
    return A - A.trace()/A.shape[0] * eye(A.shape[0])
def grad(A):
    try:
        return A.grad()
    except:
        return 0
