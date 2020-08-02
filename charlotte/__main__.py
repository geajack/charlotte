from werkzeug.serving import run_simple

import charlotte

if __name__ == "__main__":
    run_simple(
        "localhost",
        8000,
        charlotte.application,
        use_reloader=False
    )