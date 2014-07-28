import os
from subprocess import call
from flask import render_template, request
from flask import flash, redirect, url_for
from app import app, run_script

import helper
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
                  'result_form':'text.html' } }

script_list = ['demo','format_DNA','translate']
default_choice = 'format_DNA'
file_msg = 'A sequence is required:'

def render_index_template(refresh=True):
    if refresh:
    # we're starting from the beginning
        helper.set_dict({})
        default=default_choice
    else:
    # script has already been chosen
    # prompting because we didn't get sequence
        D = helper.get_dict()
        print 'in render_index_template:  D', D
        default = D['prog']
    return render_template(
        "index.html",
        script_list = script_list,
        default=default)          

# index shows form with scripts listed
@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    return render_index_template()

# common route to deal with all forms
@app.route('/dispatch', methods = ['POST'])
def dispatch():
    print 'in: ', dispatch.__name__
    D = helper.get_dict()
    D.update(helper.parse_request_data(request))
    
    prog = D['prog']
    print 'prog', prog
    if not 'seq_needed' in D:
        D.update(script_info[prog])
    
    seq_needed = D['seq_needed']
    # modifiable
    seq_requested = 'seq_requested' in D and D['seq_requested']
    no_seq = not 'seq' in D or D['seq'] == ''
    if seq_needed and no_seq:
        if seq_requested:
            # remind them and throw them out
            flash(file_msg)
            render_index_template(refresh=False)
            
        # now ask, and retain users choice of program
        D['seq_requested'] = True
        return render_template(
            D['option_form'],
            prog = prog)
    
    try:
        result = run_script.run(D)
    except:
        return render_template(
            'error.html',
            name = prog)
        
    if D['result_type'] == 'png':
        return render_template(
            D['result_form'],
            result_type=D['result_type'],
            url = url_for('static',filename=D['result_filename']),
            description="image showing result")
            
    if D['result_type'] == 'txt':
        return render_template(
                D['result_form'],
                mytext=result)
