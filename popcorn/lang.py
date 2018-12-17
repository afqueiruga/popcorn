from .util import *
from .codegenutil import *
from . import boilerplates as b

def freesym(x):
    try:
        return x.free_symbols
    except:
        try:
            return set.union(*[ freesym(y) for y in x ])
        except:
            return set()

class Asgn():
    def __init__(self,asgn, expr, op="="):
        self.asgn = asgn
        self.expr = expr
        self.op = op
        self.free_symbols = self.asgn.free_symbols | self.expr.free_symbols
        
    def emit(self):
        # TODO: Sanitize transposing of row/columns
        from itertools import product as PRI
        lines = ["/* Evaluation of {0} */".format(self.asgn.name) ]
        try:
            it =  PRI(*[range(j) for j in self.expr.shape])
        except:
            it = range(len(self.expr))
        for i in it:
            lines += [ ccode( self.expr[i],self.asgn[i] ).replace(" =",self.op) ]
        #lines += [ ccode( a, b).replace(" =",self.op) for a,b in zip( self.asgn, self.expr ) ]
        return "\n".join(lines)

class IfElse():
    def __init__(self, cond,ifb, elb=None):
        self.cond = cond
        self.ifb = ifb
        self.elb = elb
        self.free_symbols = cond.free_symbols | freesym(ifb)
        if elb is not None:
            self.free_symbols = self.free_symbols | freesym(elb)
        
    def emit(self):
        return b.lang.if_fmt.format( ccode(self.cond),
                                     emit(self.ifb),
                                     emit(self.elb) if self.elb else "" )

class Loop():
    def __init__(self,index,start,end, body):
        self.index = index
        self.start = start
        self.end = end
        self.body = body
        self.free_symbols = freesym( self.body )
        
    def emit(self):
        bodycode = "\n".join([ emit(l) for l in self.body ])
        
        return b.lang.loop_fmt.format(ix=self.index,
                                      st=int_sanitize(self.start),
                                      end=int_sanitize(self.end),
                                      body=bodycode)

class DebugPrint():
    def __init__(self, var):
        self.var = var
        self.free_symbols = var.free_symbols
        
    def emit(self):
        from itertools import product as PRI
        lines = ['printf("{0}: ");'.format(self.var.name)]
        if self.var.rank==0:
            lines += [ 'printf("{0}:\%lf",{0}[0]);'.format(self.var.name) ]
            lines = "\n".join(lines)
        elif self.var.rank==1:
            ix = "ix_{0}".format(self.var.name)
            # lines = []
            # lines += []
            bcode = 'printf("% 6.3lf",{0}[{1}]);'.format(self.var.name,ix)
            lines += [b.lang.loop_fmt.format(ix=ix,st=0,end=self.var.dim, body=bcode)]
            lines += ["\n" + 'printf("\\n");']
            lines = "\n".join(lines)
        else:
            ix = Symbol("ix_{0}".format(self.var.name))
            jx = Symbol("jx_{0}".format(self.var.name))
            innercode = 'printf("% 6.3lf ",{0});'.format(self.var[jx,ix])
            innerloop = b.lang.loop_fmt.format(ix=ix,st=0,end=self.var.dim, body=innercode)
            outercode = "\n".join([ innerloop ] + [ 'printf("\\n");' ])
            lines = lines[0] + b.lang.loop_fmt.format(ix=jx,st=0,end=self.var.dim, body=outercode) + '\nprintf("\\n");'
        
        return lines
