from fasthtml.common import *

def Rates():
    return Section(
        H3("Code Editor Example"),
        P(
            "This is a code editor example using Ace Editor and FastHTML.",
            cls="text-gray-500"
        ),
        Div(
            Div(id="editor", cls="w-full h-96 border rounded mb-4"),
            Button("Run", cls="bg-blue-500 text-white px-4 py-2 rounded"),
            cls="flex flex-col gap-4"
        ),
        cls="px-md-10 py-10"
    )
