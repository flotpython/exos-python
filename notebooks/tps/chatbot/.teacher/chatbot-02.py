"""
just add a main title on top of the page
this is to illustrate the layout model of flet
and how to mix and match Rows and Columns
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


TITLE = "My first Chatbot 02"


def main(page: ft.Page):
    page.title = TITLE

    header = ft.Text(value=TITLE, size=40)

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

    # the submit button

    def send_request(_event):
        print("Your current settings :")
        print(f"{streaming.value=}")
        print(f"{model.value=}")
        print(f"{server.value=}")

    # send_request is the callback function defined above
    # it MUST accept one parameter which is the event that triggered the callback
    submit = ft.ElevatedButton("Send", on_click=send_request)

    # a slightly more elaborate layout creates:
    # a Column, that has 2 children:
    # - a Text (for the newly inserted title)
    # - the Row we had in v01
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
