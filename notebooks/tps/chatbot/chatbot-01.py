"""
starter code for a chatbot

this was made with flet 0.22.0 (https://flet.dev)

has the dialogs for choosing the model, the server, and the streaming option
plus a button to send the request
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

    # we're not (yet?) using the event parameter,
    # but unlike with JavaScript, we need to define it
    # NOTE that we can use the variables that are local to 'main'
    # i.e. model, server, streaming...

    def show_current_settings(_event):
        print("Your current settings :")
        print(f"{streaming.value=}")
        print(f"{model.value=}")
        print(f"{server.value=}")

    # the visual pieces
    streaming = ft.Checkbox(label="streaming", value=False)
    model = ft.Dropdown(
        options=[ft.dropdown.Option(model) for model in MODELS],
        value=MODELS[0],
        width=100,
    )
    server = ft.Dropdown(
        options=[ft.dropdown.Option(server) for server in ("CPU", "GPU")],
        value="CPU",
        width=100,
    )

    submit = ft.ElevatedButton("Send", on_click=show_current_settings)

    # arrange them in a row
    page.add(
        ft.Row(
            [streaming, model, server, submit],
            # for a row: main axis is horizontal
            # and cross axis is vertical
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main)
