import markdown

def render(raw):
    html = markdown.markdown(raw)
    return html