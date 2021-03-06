from sympy import Matrix, Symbol, ccode
import re

class Diff_Symbol(Symbol):
    def diff(self,wrt):
        if '[' in self.name:
            newname = re.sub(r'(.*)\[(.*)',r'\1_D{0}[\2'.format(wrt.name),self.name)
        else:
            newname = self.name + "_D" + wrt.name
        return Diff_Symbol(newname)


def MyMat(name, m,n=0,offset=0, SYMTYPE=Symbol):
    # n=Symbol(name)
    if not hasattr(offset,"__getitem__"):
        offset=(offset,)
    if n==0:
        return Matrix([SYMTYPE(name+"["+str(offset[0]+i)+"]", real=True) for i in range(m)])
    else:
        #return #Matrix([[SYMTYPE(name+"["+self.m+"*("+str(offset+i)+"+""+str(j)+"]") for j in range(n)] for i in range(m)])
        return Matrix([[
            SYMTYPE(name+"["+str(n*(offset[1]+i)+j+offset[0])+"]",real=True)
            for j in range(n) ] for i in range(m)])


def int_sanitize(result):
    #print result
    try:
        return "(int)("+ccode(result)+")"
    except:
        #print 'fail'
        return str(int(result))
