from util import *

class DofSpace():
    def __init__(self, gdim, v_start=0, v_end=Symbol("l_edge"), v_stride=1):
        self.dim = gdim
        self.v_start = v_start
        self.v_end = v_end
        self.v_stride = v_stride
        
    def size(self):
        if self.v_start is int and self.v_start < 0:
            return str(self.dim)
        else:
            return sanitize(self.dim*(self.v_end-self.v_start))

    def emit(self,cnt):
        if not self.v_start == -1:
            return """\
void kmap_{cnt}(int * edge, int l_edge, int * verts, int * n, int * dim) {{
  int i;
  *dim = {dim};
  *n = (int)({vlen});
  if(edge) {{
    for( i=0 ; i<*n ; i++ ) {{
      verts[i] = edge[{start} + {vstride}*i];
    }}
  }}
}}\
""".format(
    cnt = cnt,
    dim = self.dim,
    vlen = sanitize(self.v_end - self.v_start),
    start = sanitize(self.v_start),
    vstride = self.v_stride)
        else:
            return """\
void kmap_{cnt}(int * edge, int l_edge, int * verts, int * n, int * dim) {{
  int i;
  *dim = {dim};
  *n = (int)(1);
  if(edge) verts[0]=0;
}}\
""".format(
    cnt = cnt,
    dim = self.dim)

    def name(self,cnt):
        return "kmap_"+str(cnt)
