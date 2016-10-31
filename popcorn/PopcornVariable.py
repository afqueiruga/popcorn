import boilerplates as b
from sympy import ccode, Symbol, sympify

class PopcornVariable():
    def __init__(self, name, rank, dim, offset=None, depends = []):
        self.name = name
        self.rank = rank
        self.dim = dim
        if offset == None:
            self.offset = tuple([0 for i in xrange(rank)])
        else:
            self.offset = offset
        self.lda = tuple([ dim**(rank-i-1) for i in xrange(rank)])
        self.depends = depends
    def emit(self):
        return "real_t {0}[{1}];{{int i; for(i= 0;i<{1};i++) {0}[i]=0.0;}}".format(self.name,self.dim**self.rank)
    def __getitem__(self, index):
        
        if not hasattr(index,"__iter__"):
            index = (index,)
        if len(index)>self.rank:
            index = index[:self.rank]
        
        S=sum([s*(i+o) for s,i,o in zip(self.lda,index,self.offset)])
        
        return Symbol("{0}[{1}]".format(self.name,ccode(sympify(S))))
    def View(self,offset):
        return TensorVariable(self.name,self.rank,self.dim, [a+b for a,b in zip(self.offset,offset)])

    def as_matrix(self):
        if self.rank==0:
            return Symbol(self.name+"[{0}]".format(0))
        elif self.rank==1:
            return MyMat(self.name,self.dim,offset=0)
        else:
            return MyMat(self.name, self.dim,self.dim,offset=0)
    
