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
        Script("""
let editor;
document.addEventListener('DOMContentLoaded', function() {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");
    editor.setOptions({
        fontSize: "14px",
        showPrintMargin: false,
        showGutter: true,
        highlightActiveLine: true,
        wrap: true
    });
    editor.setValue("# Write your Python code here");
});
        """),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"),
        cls="px-md-10 py-10"
    )