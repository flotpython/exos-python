"""
separate the logic of our app into a class
named ChatbotApp, which inherits from ft.Column
this way we can insert it directly into the Page
it still won't do much, but it's more reusable this way
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


TITLE = "My first Chatbot - 03"


# being a Column, ChatbotApp can be directly included in a Page
# also it is a container for other controls
# see https://flet.dev/docs/tutorials/python-todo/#reusable-ui-components
class ChatbotApp(ft.Column):

    def __init__(self):
        header = ft.Text(value=TITLE, size=40)

        self.streaming = ft.Checkbox(label="streaming", value=False)
        self.model = ft.Dropdown(
            options=[ft.dropdown.Option(model) for model in MODELS],
            value=MODELS[0],
            width=300,
        )
        self.server = ft.Dropdown(
            options=[ft.dropdown.Option(server) for server in ("CPU", "GPU")],
            value="CPU",
            width=100,
        )

        self.submit = ft.ElevatedButton("Send", on_click=self.show_current_settings)

        row = ft.Row(
            [self.streaming, self.model, self.server, self.submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, row],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # in this version we access the application status through
    # attributes in the 'ChatbotApp' instance
    def show_current_settings(self, _event):
        print("Your current settings :")
        print(f"{self.streaming.value=}")
        print(f"{self.model.value=}")
        print(f"{self.server.value=}")


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(target=main)
