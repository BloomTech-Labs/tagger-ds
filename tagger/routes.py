# Main imports
import os
from flask import current_app as app
from flask import request, redirect, render_template, url_for, Response
# Markdown imports
from markdown import markdown as markd
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
from pygments.formatters import HtmlFormatter
# App functions
import tagger.message_retriever as msg


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

    # Generate codestyle
    code_style = formatter.get_style_defs()
    style_string = f"<style>{code_style}</style>"

    return render_template(
        "docs.html", style_string=style_string, md_string=md_string
    )


@app.route('/api/sync', methods=['POST'])
def sync():
    """ Accepts POST request from application for email sync """

    # Retrieve JSON body from request.
    content = request.get_json()

    # Gmail handoff ->
    if content['provider'] == 'gmail':

        # Create resource service
        service = msg.build_service(content['token'])

        # Assign recent email id
        if "recent_id" in content.keys():
            recent_id = content['recent_id']
        else:
            recent_id = None

        # Get list of email ids
        email_list = msg.user_emails(service, recent_id)

        # Create generator for individual emails
        email_gen = msg.generate_emails(service, email_list)

        return Response(msg.generate_tagged_emails(service, email_gen),
                        headers={"Content-Type": "application/json"})

    else:
        return "This functionality has not been created, yet."
