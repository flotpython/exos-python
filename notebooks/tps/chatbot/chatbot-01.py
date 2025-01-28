"""
starter code for a chatbot - made with flet 0.25.2 (https://flet.dev)

starter code has the dialogs for choosing the model, the server, and the
streaming option, plus a button to send the request
none of this is actually connected to anything yet
"""


import flet as ft

SERVERS = {
    # this one is fast because it has GPUs,
    # but it requires a login / password
    'GPU': {
        "name": "GPU fast",
        "url": "https://ollama-sam.inria.fr",
        "username": "Bob",
        "password": "hiccup",
    },
    # this one is slow because it has no GPUs,
    # but it does not require a login / password
    'CPU': {
        "name": "CPU slow",
        "url": "http://ollama.pl.sophia.inria.fr:8080",
    },
}


# a hardwired list of models
MODELS = [
    "gemma2:2b",
    "mistral:7b",
    "deepseek-r1:7b",
]


TITLE = "My first Chatbot 01"


def main(page: ft.Page):
    # set the overall window title
    page.title = TITLE

    ### the visual pieces
    # a checkbox to select "streaming" mode or not - default is false
    streaming = ft.Checkbox(label="streaming", value=False)

    # choose the model
    model = ft.Dropdown(
        options=[ft.dropdown.Option(model) for model in MODELS],
        value=MODELS[0],
        width=300,
    )
    # choose the server
    server = ft.Dropdown(
        options=[ft.dropdown.Option(server) for server in ("CPU", "GPU")],
        value="CPU",
        width=100,
    )

    # the submit button

    # what do we want to happen when we click the button ?
    def send_request(_event):
        """
        the callback that fires when clicking the 'submit' button
        """
        # NOTE that we can use the variables that are local to 'main'
        # i.e. model, server, streaming...
        # for now, just show current settings
        print("Your current settings :")
        print(f"{streaming.value=}")
        print(f"{model.value=}")
        print(f"{server.value=}")

    # send_request is the callback function defined above
    # it MUST accept one parameter which is the event that triggered the callback
    submit = ft.ElevatedButton("Send", on_click=send_request)


    # arrange these pieces in a single row
    page.add(
        ft.Row(
            [streaming, model, server, submit],
            # for a row: main axis is horizontal
            # and cross axis is vertical
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main)
