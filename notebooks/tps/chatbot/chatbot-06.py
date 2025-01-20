"""
this version now actually displays the answer from the server

to this end, the History class is a little more elaborate,
it can add new texts, or append to the last one
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


TITLE = "My first Chatbot 06"


# find the server details from the UI label
def spot_server(servername):
    return next(server for server in SERVERS if servername in server["name"])


class History(ft.Column):
    """
    the history is a column of text messages
    where prompts and answers alternate
    """

    def __init__(self):
        super().__init__([ft.TextField(label="Type a message...")])

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
        self.controls.insert(-1, display)

    # we always insert in the penultimate position
    # given that the last item in controls is the prompt TextField
    def add_chunk(self, chunk):
        self.controls[-2].value += chunk
    def current_prompt(self):
        return self.controls[-1].value


class ChatbotApp(ft.Column):

    def __init__(self, page):
        self.page = page
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

        self.submit = ft.ElevatedButton("Send", on_click=self.submit)

        self.history = History()

        row = ft.Row(
            [self.streaming, self.model, self.server, self.submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, row, self.history],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)


    def submit(self, event):
        # disable the button to prevent double submission
        self.submit.disabled = True
        self.send_request(event)
        self.submit.disabled = False
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
