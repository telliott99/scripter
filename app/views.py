import os
from subprocess import call
from flask import render_template, request
from flask import flash, redirect, url_for
from app import app, run_script

import helper
templateD = {'format_DNA':'fmtDNA.html'}

script_list = ['demo','format_DNA']
default_choice = 'format_DNA'
file_msg = 'A sequence is required:'
seq_progs = ['format_DNA']

def render_index_template(refresh=True):
    if refresh:
    # we're starting from the beginning
        helper.set_dict({})
        default=default_choice
    else:
    # we have a choice of script
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

# returns form to get seq and options
@app.route('/choose_prog', methods = ['POST'])
def choose_prog():
    print 'in: ', choose_prog.__name__
    D = helper.get_dict()
    D.update(helper.parse_request_data(request))
    prog = D['prog']
    print 'prog', prog
    # ugly, but for now:
    D['seq_required'] = prog in seq_progs
    if D['seq_required']:
        # match the options form to the request
        return render_template(
                templateD[prog],
                prog = prog)
    else:
        return render_template(
            'image.html',
            result_type='img',
            url = url_for('static',filename='info.png'),
            result='.png', 
            description="image showing result")

# now deal with seq and options and run script
@app.route('/input_options', methods = ['POST'])
def input_options():
    print 'in: ', input_options.__name__
    D = helper.get_dict()
    D.update(helper.parse_request_data(request))
    if D['seq'] == '':
        flash(file_msg)
        # retain users choice of program
        return render_index_template(
            refresh=False)
    result_type,result = run_script.run(D)
    if result_type is 'txt':
        return render_template(
            'text.html',
            mytext=result)
        
