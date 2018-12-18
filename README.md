# Popcorn

2016-2017 Alejandro F Queiruga  
Lawrence Berkeley National Lab

This is the DSL for cornflakes. The architecture is described in the cornflakes repository at
[https://github.com/afqueiruga/cornflakes](https://github.com/afqueiruga/cornflakes)

## Overview

Popcorn is a specification language for computational kernels.
You specify inputs and outputs to a kernel and how those inputs and outputs map a list of graph nodes to data.
Then you build the expressions you are will compute *symbollically* in SymPy.
You can use vector algebra, take tangents, generate shape functions---whatever you can express symbollically---plus directly type in C code to define a **Kernel**.
Popcorn then spits out a C file with unrolled low-level code with a simple call signature, and a kernel data structure that describes the call signature and how it was specified to apply to a graph.
The **Husk** of kernels can be imported into Python and then applied onto **Hypergraphs** by **cornflakes**.
(Calling import triggers the compiler.)

Popcorn was heavily inspired by FEniCS, but I needed a DSL to do things other than finite elements. 
The guiding work was numerical method searching for Peridynamics, now released in [PeriFlakes](https://github.com/afqueiruga/periflakes).
It's sort-of meant as an abstraction to define a DSL for a numerical method.
With a numerics-agnostic kernel specification and runtime (cornflakes), one can write syntax generaters that take symbolic expressions as inputs.
E.g., type in a force law in vector notation or a variational form using the **popcorn.functional.Field** types, 
do symbolic operations to apply a discretization, and spit out C code.

Popcorn is designed for Ahead-Of-Time compilation. 

## Example

**PopcornVariable**s conditionally inherit from SymPy matrix classes when they have defined lengths. (Conditional inheritance! Eek! I know! I should clean it up.) 

## License

Copyright (C) Alejandro Francisco Queiruga, Lawrence Berkeley National Lab, 2016-2018

As with cornflakes, the license is also LGPL3 as per LICENSE.txt. Note that the output of popcorn, the transpiled C and Python source, are free of this license, such that the C files may be freely incorporated into another software. However, I would appreciate a citation or the note that Popcorn was used to generate some of the source code in your documentation.
