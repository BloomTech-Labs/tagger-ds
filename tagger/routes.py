from flask import current_app as app
from flask import request, make_response, jsonify, redirect, url_for

@app.route('/', methods=['GET'])
def index():
    return redirect('/api/docs')

@app.route('/api/docs', methods=['GET'])
def docs():
    return "This is where the docs will go."

@app.route('/api/sync', methods=['POST'])
def sync():
    pass
