from __future__ import print_function
from sympy import ccode, Matrix

def assignment(expr,asgn, op="="):
    if type(asgn) is str:
        lines = ["/* Evaluate {0} */".format(asgn)]
        for i,p in enumerate(expr):
            lines += [ ccode( p, "{0}[{1}]".format(asgn,i) ).replace("=",op) ]
    elif type(asgn) is Matrix:
        lines = ["/* Evaluating something */"]
        for i,(p,a) in enumerate(zip(expr,asgn)):
            lines += [ ccode( p, a ).replace("=",op) ]
    else:
        lines += []
    return "\n".join(lines)


def emit(l):
    if isinstance(l, str):
        return l
    try:
        return l.emit()
    except AttributeError as err:
        print("Object with no emit:", l, err)
        #l.emit()
        return l
