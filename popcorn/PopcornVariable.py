from __future__ import print_function
from . import boilerplates as b
from .util import *
from sympy import ccode, Symbol, sympify, ImmutableDenseMatrix, expand

from . import popcorn_globals

class PopcornVariable(ImmutableDenseMatrix):
    def __new__(cls,  name, dim, rank,  offset=None ):
        if offset == None:
            offset = tuple([0 for i in range(rank if rank>0 else 1)])
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
            C.variable_length = False
        except Exception as e:
            # Can't do the MatrixRepresentation...
            C = super(PopcornVariable, cls)\
              .__new__(cls,MyMat(name,1,
                                 offset=sum([a for i,a in enumerate(offset)])))
            C.variable_length = True
            # if rank==0:
            #     C = super(PopcornVariable, cls)\
            #       .__new__(cls,MyMat(name,1,offset=offset[0]))
            # elif rank==1:
            #     C = super(PopcornVariable, cls)\
            #       .__new__(cls,MyMat(name,dim,offset=offset[0]))
            # else:
            #     C = super(PopcornVariable, cls)\
            #       .__new__(cls,MyMat(name,dim,dim,offset=offset))
        C.name = name
        C.rank = rank
        C.dim = dim
        C.offset = offset
        C.lda = tuple([ dim**(rank-i-1) for i in range(rank)])
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
        # if isinstance(index,int) or isinstance(index,tuple):
        if not isinstance(index,Symbol):
            try:
                return super(PopcornVariable, self).__getitem__(index)
            except IndexError as e:
                # raise e
                try:
                    if not self.variable_length:
                        raise e
                    else:
                        detect = False
                        try:
                            for a in index:
                                if a>1000:
                                    detect = False
                        except TypeError:
                            if index>1000:
                                detect = False
                        if detect:
                            raise AssertionError('Infinite looping through PopcornVariable'+self.name+'?')
                except AttributeError:
                    raise e
            except AttributeError as e:
                pass
        # TODO raise an error on infinite recursion
        if not hasattr(index,"__iter__"):
            index = (index,)
        if len(index)>self.rank:
            index = index[:self.rank]
        S=sum([s*(i)+o for s,i,o in zip(self.lda,index,self.offset)])
        return Symbol("{0}[{1}]".format(self.name,ccode(expand(S))),real=True)
        
    @property
    def free_symbols(self):
        return self.as_matrix().free_symbols
        
    def __iter__(self):
        try:
            return iter(self.as_matrix())
        except Exception as e:
            raise e
    
    def func(self, *args):
        """
        These should never be interpretted as expressions, only roots.
        """
        return ImmutableDenseMatrix(*args)
    
    def View(self,offset):
        return PopcornVariable(self.name,self.dim,self.rank,
                               [(a+b)*self.dim**(self.rank-i-1) 
                                for i,(a,b) in enumerate(zip(self.offset,offset))])

    def as_matrix(self):
        """
        Return a more sanitized Matrix type
        """
        try:
            if self.variable_length:
                return MyMat(self.name,1,offset=self.offset[0])
            elif self.rank==0:
                # return Symbol(self.name+"[{0}]".format(self.offset[0]),real=True)
                return MyMat(self.name,1,offset=self.offset[0])
            elif self.rank==1:
                return MyMat(self.name,self.dim,offset=self.offset)
            else:
                return MyMat(self.name, self.dim,self.dim,offset=self.offset )
        except AttributeError as e:
            return Matrix([self])
            


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
                        for i in range(self.dspace.v_end-self.dspace.v_start) ]
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
