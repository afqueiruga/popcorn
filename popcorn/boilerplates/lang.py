# Loops
loop_fmt = """\
{{
int {ix};
for({ix}={st};{ix}<{end};{ix}++) {{
{body}
}}
}}"""

#Ifs
if_fmt = """
if( {0} ) {{
{1}
}} else {{
{2}
}}
"""
