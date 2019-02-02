import markdown

def render(raw):
    html = markdown.markdown(raw)
    return html

def head():
    html = """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        <script>
            MathJax.Hub.Config({
                tex2jax: {
                    inlineMath: [['$','$']],
                    processEscapes: true
                }
            });
        </script>
    """
    return html