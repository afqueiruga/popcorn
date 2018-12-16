# Popcorn uses a global context to keep track of 
# inputs and outputs etc. to generate kernels
# with no bookkeeping by the developer
registered_inputs = {} #set()
registered_outputs = {} #set()
registered_fields = {} #set()
registered_kernels = set()

def reset_context():
    """
    If you're generating lots of husks in one file, you'll
    probably want to do this when starting a new one.
    """
    global registered_inputs,registered_outputs
    global registered_fields,registered_kernels
    registered_inputs = {} #set()
    registered_outputs = {} #set()
    registered_fields = {} #set()
    registered_kernels = set()