import os
from subprocess import call
from flask import render_template, request
from flask import flash, redirect, url_for
from app import app, run_script

import helper
from helper import script_info

script_list = ['demo','format_DNA','translate','extra_sites']
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
    
    # all entries in script_info have this key:
    if not 'seq_needed' in D:
        D.update(script_info[prog])
    
    seq_needed = D['seq_needed']
    # did we already ask for a sequence?
    seq_requested = D.get('seq_requested',False)
    no_seq = not 'seq' in D or D['seq'] == ''
    
    if seq_needed and no_seq:
        if seq_requested:
            # remind them, but also go back to index page
            flash(file_msg)
            render_index_template(refresh=False)
            
        # so ask them, retaining users choice of prog
        D['seq_requested'] = True
        return render_template(
            D['option_form'],
            prog = prog)
    
    # minimalist error handling, user can't fix this anyway
    debug=True
    if debug:
        result = run_script.run(D)
    else:
        try:
            result = run_script.run(D)
        except:
            return render_template(
                'error.html',
                name = prog)
    
    result_type = D['result_type']
    if result_type == 'png':
        return render_template(
            D['result_form'],
            result_type=result_type,
            url = url_for('static',
            filename=D['result_filename']),
            description="image showing result")
    
    # simple if OK, given return above     
    if result_type == 'txt':
        return render_template(
                D['result_form'],
                mytext=result)
