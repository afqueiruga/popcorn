from boilerplates import general as g
from boilerplates import afq_wrap as aw
from codegenutil import *
from util import *
import lang
import popcorn_globals

from sympy import ccode

from collections import OrderedDict
from oset import oset

class Kernel():
    def __init__(self, name, inputs, outputs, listing=[]):
        self.name = name
        self.listing = listing
        self.free_symbols = lang.freesym(self.listing)
        names = set([ x.name[:x.name.find('[')] for x in self.free_symbols ])
        self.inputs= [ x for x in popcorn_globals.registered_inputs
                      if x.name in names ]
        self.outputs= [ x for x in popcorn_globals.registered_outputs
                      if x.name in names ]
        # This doesn't work. We need to do something a little different
        # We need to make it index agnostic
        #self.inputs = [ x for x in popcorn_globals.registered_inputs
        #                if not x.free_symbols.isdisjoint( self.free_symbols ) ] 
        #self.outputs = [ x for x in popcorn_globals.registered_outputs
        #                if not x.free_symbols.isdisjoint( self.free_symbols ) ]
        # Make a list of all of the DOfSpaces and then order them
        S = oset()
        for i in inputs:
            S.add( i.dspace )
        for o in outputs:
            for d in o.dspaces:
                S.add(d)
        dic = OrderedDict()
        for i,d in enumerate(S):
            dic[d]=i
        self.spaces = dic


    def Write_Module(self, fname=None, wrap_type = "afq"):
        eval_code = self.Write_Eval()
        if wrap_type:
            code = g.module_c.format(hname=self.name+".h" if fname else "",
                                     evalmethod=eval_code,
                                     wrapper= self.afq_write_wrapper() )
            hcode = g.module_header.format(self.name,self.name)
        else:
            code = eval_code
            hcode = ""

        if fname:
            cfile = open(fname+"/"+self.name+".c","w")
            cfile.write( code )
            cfile.close()
            
            cfile = open(fname+"/"+self.name+".h","w")
            cfile.write( hcode )
            cfile.close()
        else:
            return code,hcode

    def Write_Eval(self):
        # Arguments
        inplines = ",\n".join(g.inpdcl.format(d) for d in self.inputs)
        outplines = ",\n".join(g.outpdcl.format(d) for d in self.outputs)
        code_arg = g.arguments.format(inplines,outplines)

        # Outputs
        code_body = "\n\n".join([ emit(l) for l in self.listing ])
        

        #code_body = g.body.format("","", code_outp)
        
        code = g.evalfmt.format(self.name,code_arg,code_body)
        return code

    def afq_write_wrapper(self):
        code = [
            self.afq_eval_wrapper(),
            self.afq_kernel_struct()
        ]
        return "\n".join(code)
    
    def afq_eval_wrapper(self):
        argstring = ""
        iiter=""
        for i,d in enumerate(self.inputs):
            argstring += "in"+str(iiter)+", "
            iiter += "+"+ int_sanitize(d.dspace.size())
            # TODO: RAISE ERROR for variable length input not at end
        argstring += "\n"
        iiter=""
        for i,op in enumerate(self.outputs):
            argstring += "out"+str(iiter)+", "
            iiter += "+" + int_sanitize(op.size())
        argstring = argstring[:-2]
        
        return aw.eval_wr.format(self.name, argstring)

    def afq_kernel_struct(self):
        kmap_codes = "\n".join( k.emit(self.name+str(i)) for k,i in self.spaces.iteritems() )


        
        list_kmaps = ",\n".join([ k.name(self.name+str(i)) for k,i in self.spaces.iteritems() ])
        code_kmap = aw.strct_kernel_kmaps.format(len(self.spaces.keys()),list_kmaps)

        list_inps = [ aw.strct_inp_t.format(i,self.spaces[inp.dspace],inp.name)
                      for i,inp in enumerate(self.inputs) ]
        code_inp = aw.strct_kernel_inps.format( len(self.inputs), ",\n".join(list_inps) )

        list_outps = [ aw.strct_outp_t.format(op.rank, len(op.dspaces),
                                              ",".join([str(self.spaces[d]) for d in op.dspaces]),
                                              op.name)
                       for i,op in enumerate(self.outputs) ]
        code_outp = aw.strct_kernel_outps.format(len(self.outputs),",\n".join(list_outps) )
        
        return kmap_codes +"\n" + \
            aw.strct_kernel_t.format(name=self.name,
                                     kmap=code_kmap,
                                     inp = code_inp,
                                     outp = code_outp)
    
