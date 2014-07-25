import os
from flask import render_template, request
from flask import flash, redirect, url_for
from app import app, run_script

script_list = ['demo', 'simple', 'better', 'awesome']
not_implemented_yet = ['awesome']
               
script_rqmts = {'demo':{'fn':False,'options':False}, 
                'simple':{'fn':True,'options':True},
                'better':{'fn':True,'options':True}}
                
file_msg = 'A file name or sequence is required:'

def parse_request_data():
    data = request.get_data()
    print 'request', data
    D = dict()
    for t in data.split('&'):
        k,v = t.strip().split('=')
        D[k] = v
    return D

def render_index_template(choice='simple'):
    return render_template(
        "index.html",
        script_list = script_list,
        default=choice)

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    print 'in: ', index.__name__
    return render_index_template()
        
@app.route('/prog_request', methods = ['POST'])
def prog_request():
    print 'in: ', prog_request.__name__
    D = parse_request_data()
    print 'request data: ', D.keys()
    prog = D['prog']
    if prog in not_implemented_yet:
        return render_template(
            "sorry.html",
            name=prog)
    if script_rqmts[prog]['fn']:
        if not 'fn' in D and D['seq'] == '':
            flash(file_msg)
            # retain users choice of program
            return render_index_template(
                choice=prog)
    print 'program requested: ', prog
    if not 'fn' in D:
        D['fn'] = 'sequence entered directly'
    if script_rqmts[prog]['options']:
        return render_template(
                "options.html",
                name=prog,
                fn = D['fn'])
    # no options needed for 'demo'
    return prog_run(prog)

@app.route('/prog_run/<pname>', methods = ['POST'])
def prog_run(pname):
    print 'in: ', prog_run.__name__, ', pname'
    D = parse_request_data()
    print 'D', D
    D['prog'] = pname

    # returns a filename where results are stored
    result = run_script.run(D)
    url = url_for('static', filename=result)
    return render_template(
        "result.html",
        result_type = 'img',
        url = url,
        description = 'image showing result')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
