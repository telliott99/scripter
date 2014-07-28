import os
from subprocess import call
from flask import render_template, request
from flask import flash, redirect, url_for
from app import app, run_script

import helper
script_info = { 'demo': {'seq_needed':False,
                         'opt_needed':False,
                         'result_type':'png',
                         'result_form':'image.html',
                         'result_filename':'info.png' },

                'format_DNA':{ 'seq_needed':True,
                               'opt_needed':True,
                               'option_form':'fmtDNA.html',
                               'result_form':'text.html',
                               'result_type':'txt', } }

script_list = ['demo','format_DNA']
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
        # a global dictionary to stash sequence, etc., defined in helper
        D = helper.get_dict()
        print 'in render_index_template:  D', D
        default = D['prog']
    return render_template(
        "index.html",
        script_list = script_list,
        default=default)          

# index has a form that lists scripts
@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    return render_index_template()

# returns form to get seq and options, if necessary
@app.route('/choose_prog', methods = ['POST'])
def choose_prog():
    print 'in: ', choose_prog.__name__
    D = helper.get_dict()
    D.update(helper.parse_request_data(request))
    prog = D['prog']
    print 'prog', prog
    D.update(script_info[prog])
    # dispatch is a bit clunky
    if D['seq_needed']:
        # match the options form to the request
        return render_template(
                D['option_form'],
                prog = prog)
    else:
        return render_template(
            D['result_form'],
            result_type=D['result_type'],
            url = url_for('static',filename=D['result_filename']),
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
    result = run_script.run(D)
    # for now, it's all text results here
    return render_template(
            D['result_form'],
            mytext=result)
