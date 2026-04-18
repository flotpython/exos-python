"""
introduce class History that will store the history of the chatbot
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


TITLE = "My first Chatbot 04a"


class History(ft.Column):
    """
    the history is a column of text messages
    where prompts and answers alternate

    it is created with a TextField widget
    (the editable area where the prompt is entered)
    that always remains last (at the bottom)

    as the dialog proceeds, the questions and answers
    are added, always on top of the prompt itself
    (so at the penultimate rank in the column)
    """

    # constructor
    def __init__(self):
        super().__init__([ft.TextField(label="Type a message...")])

    def add_message(self, message):
        # leave the prompt as the last entry
        # so insert at the penultimate position;
        self.controls.insert(-1, ft.Text(value=message))

    def current_prompt(self):
        return self.controls[-1].value


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

        submit = ft.ElevatedButton("Send", on_click=self.send_request)

        self.history = History()

        row = ft.Row(
            [self.streaming, self.model, self.server, submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, row, self.history],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # in this version we access the application status through
    # attributes in the 'ChatbotApp' instance
    def send_request(self, _event):
        print("Your current settings :")
        print(f"{self.streaming.value=}")
        print(f"{self.model.value=}")
        print(f"{self.server.value=}")
        print(f"{self.history.current_prompt()=}")


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(main)
