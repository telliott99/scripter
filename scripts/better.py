import os

def run(D):
    print 'in script: ', os.path.basename(__file__)
    print 'start dict:'
    for k in D:
        print '  ', k, D[k]
    return 'taylor.png'