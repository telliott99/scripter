import os, sys

# http://effbot.org/zone/import-string.htm
def my_import(name):
    m = __import__(name)
    for n in name.split(".")[1:]:
         m = getattr(m, n)
    return m

def run(D):
    print 'in run_script.run: ', os.path.basename(__file__)
    prog = D['prog']
    module = my_import("scripts." + prog)
    print module.__file__
    return module.run(D)
