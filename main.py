import re
from pathlib import Path
from aiofauna import Api, Response
from markdown import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from jinja2 import Environment, FileSystemLoader, select_autoescape

MD_FMT_CDN = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css">"""
CODE_FMT_CDN = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pygments-css@1.0.0/github.min.css">"""

html_formatter = HtmlFormatter(style='default')

jinja_env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / 'docs'),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=['jinja2.ext.do']
)

def render_md(md):
    template = jinja_env.get_template(md)
    text = template.render()
    code = re.findall(r'```[a-z]*\n[\s\S]*?\n```', text)
    for c in code:
        lang = re.findall(r'```([a-z]*)\n', c)[0]
        lexer = get_lexer_by_name(lang)
        code = re.findall(r'```[a-z]*\n([\s\S]*?)\n```', c)[0]
        code = highlight(code, lexer, html_formatter)
        text = text.replace(c, code)
    text = markdown(text, extensions=['fenced_code'])   
    text = f"""
    <html>
        <head>
            <meta charset="utf-8">
            {MD_FMT_CDN}
            {CODE_FMT_CDN}
        </head>
        <style>
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 40px;
            text-align: center;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        </style>
        <body class="markdown-body">
        <main class="container">
            {text}
        </main>
        </body>
    </html>
    """
    
    return Response(text=text, content_type='text/html')

app = Api()

app.router.add_static('/static', Path(__file__).parent / 'static')

@app.get('/')
async def index():
    return render_md('index.md')