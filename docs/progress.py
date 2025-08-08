from fasthtml.common import *

def Progress():
    return Section(
        H3("Progress"),
        P(
            A("Bootstrap documentation", 
              href="http://getbootstrap.com/docs/5.1/components/progress/", 
              target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Div(
                        cls="progress-bar bg-dark",
                        role="progressbar",
                        style="width: 12%",
                        aria_valuenow="12",
                        aria_valuemin="0", 
                        aria_valuemax="100"
                    ),
                    cls="progress mb-3"
                ),
                Div(
                    Div(
                        cls="progress-bar bg-success",
                        role="progressbar",
                        style="width: 25%",
                        aria_valuenow="25",
                        aria_valuemin="0",
                        aria_valuemax="100"
                    ),
                    cls="progress mb-3"
                ),
                Div(
                    Div(
                        cls="progress-bar bg-info",
                        role="progressbar", 
                        style="width: 50%",
                        aria_valuenow="50",
                        aria_valuemin="0",
                        aria_valuemax="100"
                    ),
                    cls="progress mb-3"
                ),
                Div(
                    Div(
                        cls="progress-bar bg-warning",
                        role="progressbar",
                        style="width: 75%",
                        aria_valuenow="75",
                        aria_valuemin="0",
                        aria_valuemax="100"
                    ),
                    cls="progress mb-3"
                ),
                Div(
                    Div(
                        cls="progress-bar bg-danger",
                        role="progressbar",
                        style="width: 100%",
                        aria_valuenow="100",
                        aria_valuemin="0",
                        aria_valuemax="100"
                    ),
                    cls="progress"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="progress mb-3">\n  <div class="progress-bar bg-dark" role="progressbar" style="width: 12%" aria-valuenow="12" aria-valuemin="0" aria-valuemax="100"></div>\n</div>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )