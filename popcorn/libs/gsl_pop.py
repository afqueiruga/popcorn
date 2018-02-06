
class mat_solve():
    def __init__(self, A, x, R):
        self.A = A
        self.x = x
        self.R = R
    def emit(self):
        return """
        {{
        gsl_vector_view gsl_vec_{R} 
         = gsl_vector_view_array( {R}, {n} );
        gsl_vector_view gsl_vec_{x} 
         = gsl_vector_view_array( {x}, {n} );
        gsl_matrix_view gsl_mat_{A} 
          = gsl_matrix_view_array( {A}, {n}, {n} );
        gsl_permutation * gsl_p_{A}
          = gsl_permutation_alloc( {n} );
        int gsl_s_{A};

        gsl_linalg_LU_decomp(&gsl_mat_{A}.matrix, gsl_p_{A}, &gsl_s_{A});
        gsl_linalg_LU_solve( &gsl_mat_{A}.matrix, gsl_p_{A}, 
                             &gsl_vec_{R}.vector,
                             &gsl_vec_{x}.vector );

        gsl_permutation_free(gsl_p_{A});
        }}
        """.format(A=self.A.name, x=self.x.name, R=self.R.name, n=self.A.dim)

class mat_lu():
    def __init__(self, A):
        self.A = A
    def emit(self):
        return """
        
        gsl_matrix_view gsl_mat_{A} 
          = gsl_matrix_view_array( {A}, {n}, {n} );
        gsl_permutation * gsl_p_{A}
          = gsl_permutation_alloc( {n} );
        int gsl_s_{A};

        gsl_linalg_LU_decomp(&gsl_mat_{A}.matrix, gsl_p_{A}, &gsl_s_{A});

        
        """.format(A=self.A.name, n=self.A.dim)
class mat_lu_solve():
    def __init__(self, A, x, R):
        self.A = A
        self.x = x
        self.R = R
    def emit(self):
        return """
        {{
        gsl_vector_view gsl_vec_{R} 
         = gsl_vector_view_array( {R}, {n} );
        gsl_vector_view gsl_vec_{x} 
         = gsl_vector_view_array( {x}, {n} );

        gsl_linalg_LU_solve( &gsl_mat_{A}.matrix, gsl_p_{A}, 
                             &gsl_vec_{R}.vector,
                             &gsl_vec_{x}.vector );

        }}
        """.format(A=self.A.name, x=self.x.name, R=self.R.name, n=self.A.dim)
class mat_lu_cleanup():
    def __init__(self, A):
        self.A = A
    def emit(self):
        return """
        gsl_permutation_free(gsl_p_{A});
        """.format(A=self.A.name)
