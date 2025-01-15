"""
we add protection against multiple submissions
also, one can simply type Return in the prompt to send the request

"""

import json

import requests
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


# find the server details from the UI label
def spot_server(servername):
    return next(server for server in SERVERS if servername in server["name"])


class History(ft.Column):
    """
    the history is a column of text messages
    where prompts and answers alternate
    """

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.controls = [
            ft.TextField(
                label="Type a message...",
                on_submit=lambda event: self.app.submit(event),
            ),
        ]

    # insert material - prompt or answer - to allow for different styles
    def add_prompt(self, message):
        self._add_entry(message, "prompt")
    def add_answer(self, message):
        self._add_entry(message, "answer")
    def _add_entry(self, message, kind):
        display = ft.Text(value=message)
        display.color = "blue" if kind == "prompt" else "green"
        display.size = 20 if kind == "prompt" else 16
        display.italic = kind == "prompt"
        self.controls[-1:-1] = [display]

    # we always insert in the penultimate position
    # given that the last item in controls is the prompt TextField
    def add_chunk(self, chunk):
        self.controls[-2].value += chunk
    def current_prompt(self):
        return self.controls[-1].value


# being a Column, ChatbotApp can be directly included in a Page
# also it is a container for other controls
class ChatbotApp(ft.Column):

    def __init__(self, page):
        super().__init__()
        self.page = page
        self.disabled = False
        self.header = ft.Text(value=TITLE, size=40)

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

        self.submit_button = ft.ElevatedButton("Send", on_click=self.submit)

        self.history = History(self)

        self.controls = [
                self.header,
                ft.Row(
                    [self.streaming, self.model, self.server, self.submit_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.history,
            ]
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER

    def submit(self, event):
        # and now that the textfield itself is linked to this callback
        # we enforce it even further
        if self.disabled:
            return
        # disable the button to prevent double submission
        # keep it for the visual effect
        self.submit_button.disabled = True
        self.disabled = True
        self.send_request(event)
        self.submit_button.disabled = False
        self.disabled = False
        self.page.update()


    # send the prompt to the server and display the answer
    def send_request(self, _event):
        # retrieve the current state
        history = self.history
        streaming = self.streaming.value
        model = self.model.value
        servername = self.server.value
        prompt = history.current_prompt()

        # record question asked
        history.add_prompt(prompt)
        # create placeholder for the answer
        history.add_answer("")
        # update UI
        self.page.update()

        # send the request
        server = spot_server(servername)
        print(f"Sending message to {server=}, {model=}, {streaming=}, {prompt=}")
        # first version is non-streaming
        url = f"{server['url']}/api/generate"
        data = {'model': model, 'prompt': prompt}
        answer = requests.post(url, json=data)
        print("HTTP status code:", answer.status_code)
        # print(f"Received answer: {answer.text}")
        # turns out we receive a stream of JSON objects
        # each one on its own line
        for line in answer.text.split("\n"):
            # splitting artefacts can be ignored
            if not line:
                continue
            # ther should be no exception, but just in case...
            try:
                # print("line:", line)
                data = json.loads(line)
                # the last JSON chunk contains statistics and is not a message
                if data['done']:
                    # ignore last summary chunk
                    pass
                # display that message; it's only a token so we append it to the last message
                history.add_chunk(data['response'])
            except Exception as e:
                print("Error:", e)
        self.page.update()


def main(page: ft.Page):
    page.title = TITLE

    # we need page to be able to do updates..
    chatbot = ChatbotApp(page)
    page.add(chatbot)


ft.app(target=main)
