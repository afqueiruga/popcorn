from util import *
from codegenutil import *
import boilerplates as b


class Asgn():
    def __init__(self,asgn, expr, op="="):
        self.asgn = asgn
        self.expr = expr
        self.op = op
    def emit(self):
        from itertools import product as PRI
        lines = ["/* Evaluation of {0} */".format(self.asgn.name) ]
        try:
            it =  PRI(*[xrange(j) for j in self.expr.shape])
        except:
            it = xrange(len(self.expr))
            print it
        for i in it:
            print i
            lines += [ ccode( self.expr[i],self.asgn[i] ).replace(" =",self.op) ]
        return "\n".join(lines)

class IfElse():
    def __init__(self, cond,ifb, elb=None):
        self.cond = cond
        self.ifb = ifb
        self.elb = elb
    def emit(self):
        return b.lang.if_fmt.format( ccode(self.cond), self.ifb.emit(), self.elb.emit() if self.elb else "" )

class Loop():
    def __init__(self,index,start,end, body):
        self.index = index
        self.start = start
        self.end = end
        self.body = body

    def emit(self):
        bodycode = "\n".join([ l.emit() for l in self.body ])
        
        return b.lang.loop_fmt.format(ix=self.index,
                                      st=int_sanitize(self.start),
                                      end=int_sanitize(self.end),
                                      body=bodycode)

class DebugPrint():
    def __init__(self, var):
        self.var = var
    def emit(self):
        from itertools import product as PRI
        lines = []
        if self.var.rank==0:
            lines += [ 'printf("{0}:\%lf",{0}[0]);'.format(self.var.name) ]
        elif self.var.rank==1:
            ix = "ix_{0}".format(self.var.name)
            lines += ['printf("{0}: ");'.format(self.var.name)]
            bcode = 'printf("% 6.3lf",{0}[{1}]);'.format(self.var.name,ix)
            lines += b.lang.loop_fmt.format(ix=ix,st=0,end=self.var.dim, body=bodycode)
            lines += "\n" + 'printf("\\n");'
        else:
            ix = Symbol("ix_{0}".format(self.var.name))
            jx = Symbol("jx_{0}".format(self.var.name))
            innercode = 'printf("% 6.3lf ",{0});'.format(self.var[ix,jx])
            innerloop = b.lang.loop_fmt.format(ix=ix,st=0,end=self.var.dim, body=innercode)
            outercode = "\n".join([ innerloop ] + [ 'printf("\\n");' ])
            lines = b.lang.loop_fmt.format(ix=jx,st=0,end=self.var.dim, body=outercode) + '\nprintf("\\n");'
        return lines
