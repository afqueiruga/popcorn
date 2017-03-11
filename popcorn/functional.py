"""
Generic tools for functional implementation

"""
from PopcornVariable import PopcornVariable
from sympy import Matrix

class Field( PopcornVariable):
    def __new__(cls, name, gdim, rank):
        #if rank==0:
        #    C = super(Field,cls).__new__(cls, 'field_'+name, 1,1)
        #else:
        C = super(Field,cls).__new__(cls, 'field_'+name, gdim,rank)
        #C.gdim = gdim
        C.pv_grad_u = None
        return C
    #def __init__(self, name, gdim, rank):
    #    self.pv_u = PopcornVariable('field_'+name, gdim,rank)
    #    self.pv_grad_u = None
    #def val(self):
    #    return self.pv_u.as_matrix()
    def grad(self):
        if self.pv_grad_u is None:
            self.pv_grad_u = PopcornVariable('grad_'+ self.name, self.dim, self.rank+1)
        return self.pv_grad_u #.as_matrix()
    #def emit(self):
    #    return "\n".join([
    #        super(Field,self).emit(),
    #        ( self.pv_grad_u.emit() if self.pv_grad_u is not None else "" )
    #        ])
    
def extract(P, u, grad_u,   NJ, grad_NJ,
               tu, grad_tu, NI, grad_NI):
    gdim = len(grad_u)
    RI = Matrix([P]).jacobian(grad_tu).dot( grad_NI ) \
     + P.diff(tu) * NI
    KIJ = Matrix([RI]).jacobian(grad_u).dot( grad_NJ ) \
      + P.diff(u) * NJ
    # RI = RI.subs(u, P0.dot(pv_a.as_matrix()) )
    # for i in range(gdim):
        # RI = RI.subs(grad_u[i], grad_NI[i] )
    # KIJ = KIJ.subs(u, P0.dot(pv_a.as_matrix()) )
    # for i in range(gdim):
        # KIJ = KIJ.subs(grad_u[i], grad_NJ[i] )

    return RI, KIJ

def gateaux(f, u, N, dNdx): # NOTE
    R = [ Matrix([f]).diff(ui) * NA + Matrix([f]).jacobian(grad(u)[:,i]) * dNdx[:,A]
              for A,NA in enumerate(N)
              for i,ui in enumerate(u) ]
    # print len(R)
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
    for i in xrange(A.shape[0]):
        for j in xrange(A.shape[1]):
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
