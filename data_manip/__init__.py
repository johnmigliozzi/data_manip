def flatten_json(y, preserve_name=True):
    out = {}
    def flatten(x, name=''):

        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:
            for a in x:
                if preserve_name == True:
                    flatten(x[a], name + a + '_')
                else:
                    flatten(x[a], a + '_')

        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:
            i = 0
            for a in x:
                if preserve_name == True:
                    flatten(a, name + str(i) + '_')
                else:
                    flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out