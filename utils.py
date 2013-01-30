def print_dict(d):
    '''Return intuitive textual representation for a dict.'''
    
    s = ""
    
    for k, v in d.iteritems():
        s += "{} ---> {}\n".format(k, v)
        
    return s