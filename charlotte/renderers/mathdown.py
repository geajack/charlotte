import markdown

def render(raw):
    html = markdown.markdown(raw)
    return html

def head():
    html = """
        <script type="text/x-mathjax-config">
            MathJax.Hub.Config(
                {
                    elements: document.querySelectorAll(".mathdown-format"),
                    tex2jax: {
                        inlineMath: [['$','$']],
                        processEscapes: true
                    }
                }
            );
        </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"></script>        
    """
    return html