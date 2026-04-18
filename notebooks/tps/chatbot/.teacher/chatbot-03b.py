"""
the code of the callback goes in a class method

for that to work, we need to store the 3 settings widgets
as attributes in the ChatbotApp instance
"""

import os

# reads GPU_USERNAME, GPU_PASSWORD, CPU_USERNAME, CPU_PASSWORD from .env
from dotenv import load_dotenv
import flet as ft

load_dotenv()

SERVERS = {
    'GPU': {
        "name": "GPU fast",
        "url": "https://ollama-sam.inria.fr",
        "username": os.getenv("GPU_USERNAME"),
        "password": os.getenv("GPU_PASSWORD"),
    },
    'CPU': {
        "name": "CPU slow",
        "url": "https://ollama.pl.sophia.inria.fr",
        "username": os.getenv("CPU_USERNAME"),
        "password": os.getenv("CPU_PASSWORD"),
    },
}


# a hardwired list of models
MODELS = [
    "gemma2:2b",
    "mistral:7b",
    "deepseek-r1:7b",
]


TITLE = "My first Chatbot 03b"


# being a Column, ChatbotApp can be directly included in a Page
# also it is a container for other controls
# see https://flet.dev/docs/tutorials/python-todo/#reusable-ui-components
class ChatbotApp(ft.Column):

    def __init__(self):
        header = ft.Text(value=TITLE, size=40)

        # the 3 settings widgets need to be inspectable
        # later on in the code (in the submit method)
        # so we store them as attributes in the ChatbotApp instance

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

        # the callback is now a method
        # note that self.send_request, being a bound method object,
        # really expects exactly 1 parameter and not 2
        submit = ft.ElevatedButton("Send", on_click=self.send_request)

        row = ft.Row(
            [self.streaming, self.model, self.server, submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # we initialize ourselves as a ft.Column
        # so we need to call ft.Column.__init__( list-of-children, ...)
        super().__init__(
            [header, row],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # in this version we access the application status through
    # attributes in the 'ChatbotApp' instance
    def send_request(self, _event):
        print("Your current settings :")
        print(f"{self.streaming.value=}")
        print(f"{self.model.value=}")
        print(f"{self.server.value=}")


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(main)
