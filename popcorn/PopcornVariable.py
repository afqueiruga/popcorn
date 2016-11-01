import boilerplates as b
from util import *
from sympy import ccode, Symbol, sympify

class PopcornVariable():
    def __init__(self, name, rank, dim, offset=None ):
        self.name = name
        self.rank = rank
        self.dim = dim
        if offset == None:
            self.offset = tuple([0 for i in xrange(rank)])
        else:
            self.offset = offset
        self.lda = tuple([ dim**(rank-i-1) for i in xrange(rank)])
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
    


class Input( PopcornVariable ):
    def __init__(self, name, dspace):
        PopcornVariable.__init__(self, name, 1, dspace.size(), offset=0)
        self.dspace = dspace
    
    def Entry_Handle(self,i):
        return Symbol(self.name+"["+str(i)+"]")
    def Entry_Handles(self,*args):
        return [ self.Entry_Handle(i) for i in args ]
    
    def Entry_Split(self):
        try:
            return [ self.Entry_Handle(i) for i in self.dspace.size() ]
        except TypeError:
            raise Exception("Can't seperate entries for variable length inputs")
        
    def Vertex_Handle(self,i):
        return MyMat(self.name,self.dspace.dim,offset = i*self.dspace.dim)
    def Vertex_Handles(self,*args):
        return [ self.Vertex_Handle(i) for i in args ]
    
    def Vertex_Split(self):
        try:
            if self.dspace.v_end < 0:
                raise Exception("Can't seperate vertices for variable length inputs")
            else:
                return [ self.Vertex_Handle(i)
                        for i in xrange(self.dspace.v_end-self.dspace.v_start) ]
        except TypeError:
            raise Exception("Can't seperate entries for variable length inputs")
        

class Output( PopcornVariable ):
    def __init__(self, name, dspaces, rank):
        self.dspaces = dspaces
        self.rank = rank
        PopcornVariable.__init__(self, name, rank, self.size(), offset=(0,0))

    def size(self):
        if self.rank==0:
            return 1
        else:
            size = sum([d.size() for d in self.dspaces])
            if self.rank==1:
                return size
            else:
                return size*size
