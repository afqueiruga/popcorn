from boilerplates import pylink as BP
from subprocess import call
import popcorn_globals

def Husk(libname,kernels=None,installdir=".",config=BP.config_linux):
    targetdir = installdir + "/husk_" + libname + "/"
    call(['mkdir','-p',targetdir])

    kernels = list(popcorn_globals.registered_kernels)
    # Tell the kernels to write themselves
    for k in kernels:
        k.Write_Module(targetdir)

    kernelnames = [ k.name for k in kernels]
    
    d = {"libname":libname,"kernels":" ".join(kernelnames)}
    d.update(config)
    
    # mf = open(targetdir+"Makefile","w")    
    # mf.write(BP.makefile.format(**d))
    # mf.close()

    sf = open(targetdir+libname+"_swig.i","w")    
    sf.write(BP.wrapper.format(
        "\n".join([BP.swig_include.format(n) for n in kernelnames]),
        "\n".join([BP.swig_swigi.format(n)   for n in kernelnames]),
        **d))
    sf.close()

    initf = open(targetdir+"__init__.py","w")
    initf.write(BP.initfile.format(
        "\n".join([BP.importline.format(n,**d) for n in kernelnames ]),
        **d))
    initf.close()

    bigheader = open(targetdir+"kernels_{0}.h".format(libname),"w")
    bigheader.write(BP.bigheader.format(
        "\n".join([BP.swig_include.format(n) for n in kernelnames]),
        **d))
    bigheader.close()

    cmakelists = open(targetdir+"CMakeLists.txt","w")
    cmakelists.write(BP.cmakelists2.format(
        "\n".join([BP.cmakelists_add_src.format(n) for n in kernelnames]),
        **d))
    cmakelists.close()
