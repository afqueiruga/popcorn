#
# Generate the wrappers for the cornflakes structure
#
strct_kernel_t = """\
kernel_t kernel_{name} = {{
{kmap}
{inp}
{outp}
.eval={name}_eval_wr,
.name="{name}"
}};
"""

strct_kernel_kmaps = """\
.nmap = {0},
.maps = {{
{1}
}},
"""

strct_kernel_inps = """\
.ninp = {0},
.inp = {{
{1}
}},
"""
strct_inp_t = '{{ .field_number={0}, .map_num={1}, .name="{2}" }}'

strct_kernel_outps = """\
.noutp = {0},
.outp = {{
{1}
}},"""
strct_outp_t = '{{ .rank = {0}, .nmap = {1}, .map_nums = {{ {2} }}, .name="{3}" }}'


eval_wr = """\
void {0}_eval_wr(int l_edge, const real_t * restrict in, real_t * restrict out) {{
   {0}_eval(l_edge,{1});
}}
"""
