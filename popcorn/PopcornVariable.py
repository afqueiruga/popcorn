import boilerplates as b
from util import *
from sympy import ccode, Symbol, sympify, ImmutableDenseMatrix

import popcorn_globals

class PopcornVariable(ImmutableDenseMatrix):
    def __new__(cls,  name, dim, rank,  offset=None ):
        if offset == None:
            offset = tuple([0 for i in xrange(rank if rank>0 else 1)])
        if not hasattr(offset,"__getitem__"):
            offset=(offset,)
        try:
            if rank==0:
                m= MyMat(name, 1, offset=offset[0])
            elif rank==1:
                m= MyMat(name,dim,offset=offset[0])
            else:
                m= MyMat(name, dim,dim,offset=offset)
            
            C = super(PopcornVariable, cls).__new__(cls, m)
        except Exception as e:
            # Can't do the MatrixRepresentation...
            C = super(PopcornVariable, cls).__new__(cls, MyMat(name,1,offset=offset[0]))
            C.bad = True
        C.name = name
        C.rank = rank
        C.dim = dim
        C.offset = offset
        C.lda = tuple([ dim**(rank-i-1) for i in xrange(rank)])
        return C

    def emit(self):
        """
        Print out the allocation and initialization to 0.
        """
        return "real_t {0}[{1}];{{int i; for(i= 0;i<{1};i++) {0}[i]=0.0;}}".format(self.name,self.dim**self.rank)
    
    def __getitem__(self, index):
        """
        Extra logic to handle the case where index is not an int, or 
        the variable has an indefinite length.
        """
        try:
            return super(PopcornVariable, self).__getitem__( index)
        except: # IndexError, AttributeError:
            pass
        if not hasattr(index,"__iter__"):
            index = (index,)
        if len(index)>self.rank:
            index = index[:self.rank]
        
        S=sum([s*(i+o) for s,i,o in zip(self.lda,index,self.offset)])
        
        return Symbol("{0}[{1}]".format(self.name,ccode(sympify(S))),real=True)
    def __iter__(self):
        if type(self.dim) is int:
            return iter(self.as_matrix())
        else:
            return None
    def func(self, *args):
        """
        These should never be interpretted as expressions, only roots.
        """
        return ImmutableDenseMatrix(*args)
    
    def View(self,offset):
        return PopcornVariable(self.name,self.dim,self.rank,
                                   [a+b for a,b in zip(self.offset,offset)])

    def as_matrix(self):
        if self.rank==0:
            return Symbol(self.name+"[{0}]".format(self.offset[0]),real=True)
        elif self.rank==1:
            return MyMat(self.name,self.dim,offset=self.offset)
        else:
            return MyMat(self.name, self.dim,self.dim,offset=self.offset )
    


class Input( PopcornVariable ):
    def __new__(cls, name, dspace ):
        C = super(Input,cls).__new__(cls, name, dspace.size(), 1, offset=0)
        C.dspace = dspace
        # popcorn_globals.registered_inputs.add(C)
        popcorn_globals.registered_inputs[name] = C
        return C
    
    def Entry_Handle(self,i):
        return self[i]
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
    def __new__(cls, name, dspaces, rank):
        dim = sum([d.size() for d in dspaces])
        C = super(Output, cls).__new__(cls, name,dim, rank,offset=(0,0))
        C.dspaces = dspaces
        # popcorn_globals.registered_outputs.add(C)
        popcorn_globals.registered_outputs[name] = C
        return C
    def size(self):
        if self.rank==0:
            return 1
        else:
            size = sum([d.size() for d in self.dspaces])
            if self.rank==1:
                 return size
            else:
                return size*size
