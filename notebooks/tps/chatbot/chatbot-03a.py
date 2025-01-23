"""
separate the logic of our app into a class
named ChatbotApp, which inherits from ft.Column
this way we can insert it directly into the Page
it still won't do much, but it's more reusable this way
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
        "default": True,
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
]


TITLE = "My first Chatbot 03a"


# being a Column, ChatbotApp can be directly included in a Page
# also it is a container for other controls
# see https://flet.dev/docs/tutorials/python-todo/#reusable-ui-components
class ChatbotApp(ft.Column):

    def __init__(self):
        header = ft.Text(value="My Chatbot", size=40)

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

        def send_request(_event):
            print("Your current settings :")
            print(f"{streaming.value=}")
            print(f"{model.value=}")
            print(f"{server.value=}")

        submit = ft.ElevatedButton("Send", on_click=send_request)

        row = ft.Row(
            [streaming, model, server, submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # we initialize ourselves as a ft.Column
        # so we need to call ft.Column.__init__( list-of-children, ...)
        super().__init__(
            [header, row],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

# tag to show the code in the instructions
def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(main)
