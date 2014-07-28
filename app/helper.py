import urllib

def parse_request_data(request):
    data = request.get_data()
    D = dict()
    if not data:
        print 'no request data'
        return D
    for t in data.split('&'):
        k,v = t.strip().split('=')
        v = urllib.unquote_plus(v)
        D[k] = v
    return D

# global dict to stash form data between callbacks

def get_dict():
    return D

def set_dict(input):
    global D
    D = input

set_dict({})

