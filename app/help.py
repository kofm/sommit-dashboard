from dash import html, dcc

with open("help/README.md") as file:
    file_contents = file.read()

about_text = dcc.Markdown(
    children=file_contents, className = "my-3"
)

tab_help = [about_text]
