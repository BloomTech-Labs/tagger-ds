import os
from flask import current_app as app
from flask import request, redirect, render_template, url_for, Response
from markdown import markdown as markd
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
from pygments.formatters import HtmlFormatter
# Helper functions
from .message_retriever import user_emails, recent_id, tag_recent
from .credentials import construct_creds

@app.route('/', methods=['GET'])
def index():
    return redirect('/api/docs')

@app.route('/api/docs', methods=['GET'])
def docs():
    """ Main documentation display route """

    # Read doc markdown
    doc_page = open("tagger/pages/docs_v1.md", "r")
    md_string = markd(
        doc_page.read(), extensions=['fenced_code', 'codehilite']
    )
    formatter = HtmlFormatter(
        style="friendly", full=True, cssclass="codehilite"
    )

    # generate codestyle
    code_style = formatter.get_style_defs()
    style_string = f"<style>{code_style}</style>"

    return render_template(
        "docs.html", style_string=style_string, md_string=md_string
    )

@app.route('/api/sync', methods=['POST'])
def sync():
    """ Accepts POST request from application for email sync """

    # Get request args from POST
    content = request.get_json()

    # Gmail handoff ->
    if content['provider'] == 'gmail':

        # Create OAuth Credentials
        creds = construct_creds(content['token'])

        # Get some emails
        message_list = user_emails(creds)
        recent = recent_id(message_list)
        tags = tag_recent(recent, creds)

        return tags

    else:
        return "This functionality has not been created, yet."
