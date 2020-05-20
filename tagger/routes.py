from flask import current_app as app
from flask import request, redirect, render_template, url_for
from markdown import markdown as markd
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
from pygments.formatters import HtmlFormatter

@app.route('/', methods=['GET'])
def index():
    return redirect('/api/docs')

@app.route('/api/docs', methods=['GET'])
def docs():
    doc_page = open("tagger/pages/docs_v1.md", "r")
    md_string = markd(
        doc_page.read(), extensions=['fenced_code', 'codehilite']
    )
    formatter = HtmlFormatter(
        style="friendly", full=True, cssclass="codehilite"
    )
    code_style = formatter.get_style_defs()
    style_string = f"<style>{code_style}</style>"
    return render_template(
        "docs.html", style_string=style_string, md_string=md_string
    )

@app.route('/api/sync', methods=['POST'])
def sync():
    pass
