makefile = """
SRCDIR = .
BUILDDIR = build
INSTALLDIR = ..

CC = {cc}
SWIG = {swig}
CFLAGS = {cflags}
IFLAGS = {iflags}
LFLAGS = {lflags}

LDSETTING = {ldsetting}

KERNELS = {kernels}

SWIGINFS = {libname}_swig.i
WRAPPERS = $(SWIGINFS:.i=_wrap.c)
SRCS = $(addsuffix .c,$(KERNELS))
HEADERS =  $(SRCS:.c=.h)
OBJS = $(SRCS:.c=.o)
WRAPOBJS = $(WRAPPERS:.c=.o)

TARGETS = _{libname}_lib.so
PYTARGETS = {libname}_lib.py

all: $(TARGETS) $(PYTARGETS)

$(TARGETS): $(OBJS) $(WRAPOBJS)
	$(CC) $(LDSETTING) $(OBJS) $(WRAPOBJS) $(LFLAGS) -o $@

$(WRAPPERS): %_wrap.c : %.i $(HEADERS)
	$(SWIG) -python -o $@ $<

$(OBJS): %.o : %.c %.h
	$(CC) $(CFLAGS) $(IFLAGS) $< -o $@
$(WRAPOBJS): %.o : %.c $(HEADERS)
	$(CC) $(CFLAGS) $(IFLAGS) $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGETSI) $(PYTARGETSI) $(OBJSB) $(WRAPPERSB)

"""

config_linux = {
    "cc":"gcc",
    "swig":"swig3.0",
    "cflags":"-c -fpic -Ofast",
    "iflags":"-I/usr/include/python2.7/ -I/usr/include/sys/ -I$(SRCDIR)",
    "lflags":"",
    "ldsetting":"-shared"
    }
config_osx = {
    "cc":"gcc-mp-5",
    "swig":"swig",
    "iflags":"-I/opt/local/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/ -I/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/numpy/core/include/ ",
    "cflags":"-c -fpic -Ofast",
    "lflags":"-F/opt/local/Library/Frameworks/ -framework python -L/opt/local/lib/ -lm",
    "ldsetting":"-dynamiclib "
}


wrapper = """
%module {libname}_lib
%{{
{0}
%}}
{1}
"""
swig_include='#include "{0}.h"'
swig_swigi = '%include "{0}.h"'

bigheader = """
#ifndef __KERNELS_{libname}_H
#define __KERNELS_{libname}_H

{0}

#endif
"""

initfile = """\
import {libname}_lib
{0}
"""
importline = "kernel_{0} = {libname}_lib.cvar.kernel_{0}"
# TODO: Add features for calling the wrapper. Now all it does is give you the struct in context.

cmakelists = """
set(KERNEL_INCLUDES ${{KERNEL_INCLUDES}} ${{CMAKE_CURRENT_SOURCE_DIR}} PARENT_SCOPE)
set(KERNEL_FILES
    ${{KERNEL_FILES}}
    {0}
    PARENT_SCOPE)
"""
cmakelists_add_src = " ${{CMAKE_CURRENT_SOURCE_DIR}}/{0}.c "
