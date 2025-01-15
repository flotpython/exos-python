"""
just add a main title on top of the page
this is to ilustrate the layout model of flet
"""

import flet as ft

SERVERS = [
    # this one is fast because it has GPUs,
    # but it requires a login / password
    {
        "name": "GPU fast",
        "url": "https://ollama-sam.inria.fr",
        "username": "Bob",
        "password": "hiccup",
        "default": True,
    },
    # this one is slow because it has no GPUs,
    # but it does not require a login / password
    {
        "name": "CPU slow",
        "url": "http://ollama.pl.sophia.inria.fr:8080",
    },
]


# a hardwired list of models
MODELS = [
    "gemma2:2b",
    "mistral:7b",
]


TITLE = "My first Chatbot"


def main(page: ft.Page):
    page.title = TITLE

    header = ft.Text(value=TITLE, size=40)

    # we're not (yet?) using the event parameter,
    # but unlike with JavaScript, we need to define it
    # NOTE that we can use the variables that are local to 'main'
    # i.e. model, server, streaming...
    def show_current_settings(_event):
        print("Your current settings :")
        print(f"{streaming.value=}")
        print(f"{model.value=}")
        print(f"{server.value=}")

    streaming = ft.Checkbox(label="streaming", value=False)
    model = ft.Dropdown(
        options=[ft.dropdown.Option(model) for model in MODELS],
        value=MODELS[0],
        width=300,
    )
    server = ft.Dropdown(
        options=[ft.dropdown.Option(server) for server in ("CPU", "GPU")],
        value="CPU",
        width=100,
    )

    submit = ft.ElevatedButton("Send", on_click=show_current_settings)

    page.add(
        ft.Column(
            [
                header,
                ft.Row(
                    [streaming, model, server, submit],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.app(main)
