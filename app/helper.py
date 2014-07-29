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

# notice we execute upon import
set_dict({})

script_info = { 
    'demo': {'seq_needed':False,
             'option_form':None,
             'result_type':'png',
             'result_form':'image.html',
             'result_filename':'info.png' },

    'format_DNA':{ 'seq_needed':True,
                   'option_form':'fmtDNAopts.html',
                   'result_type':'txt',
                   'result_form':'text.html' },
                   
    'translate':{ 'seq_needed':True,
                  'option_form':'fmtDNAopts.html',
                  'result_type':'txt',
                  'result_form':'text.html' },
                   
    'extra_sites':{ 'seq_needed':True,
                    'option_form':'sites_opts.html',
                    'result_type':'txt',
                    'result_form':'text.html' } 
}


