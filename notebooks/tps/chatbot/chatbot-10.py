"""
instead of using a hard-wired list of models,
we prompt the server for the list of known models
"""

import json

import requests
import flet as ft

DEFAULT_SERVER = "GPU fast"

SERVERS = [
    # this one is fast because it has GPUs,
    # but it requires a login / password
    {
        "name": "GPU fast",
        "url": "https://ollama-sam.inria.fr",
        "username": "Bob",
        "password": "hiccup",
    },
    # this one is slow because it has no GPUs,
    # but it does not require a login / password
    {
        "name": "CPU slow",
        "url": "http://ollama.pl.sophia.inria.fr:8080",
    },
]

# models are now fetched, no longer need for a global list


TITLE = "My first Chatbot 10"


# find the server details from the UI label
def spot_server(servername):
    return next(server for server in SERVERS if servername in server["name"])


class History(ft.Column):
    """
    the history is a column of text messages
    where prompts and answers alternate
    """

    def __init__(self, app):
        self.app = app
        super().__init__(
            [ft.TextField(
                label="Type a message...",
                on_submit=lambda event: self.app.submit(event),
                fill_color="lightgrey",
            )],
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True,
            expand=True,
            )

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
        # we keep a cache of available models on each server
        self.models_per_server = {}

        header = ft.Text(value=TITLE, size=40)

        self.streaming = ft.Checkbox(label="streaming", value=True)
        #  will be populated later
        self.model = ft.Dropdown(
            # options=[],
            width=300,
        )

        servernames = [s['name'] for s in SERVERS]
        self.server = ft.Dropdown(
            options=[ft.dropdown.Option(server) for server in servernames],
            value=DEFAULT_SERVER,
            width=150,
            on_change=lambda event: self.update_models(),
        )

        self.submit_button = ft.ElevatedButton("Send", on_click=self.submit)

        self.history = History(self)

        row = ft.Row(
            [self.streaming, self.model, self.server, self.submit_button],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, row, self.history],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        # xxx somehow I need to move this here because after __init__ self.page is .. None !?!
        self.page = page
        # a local attribute to prevent multiple submissions
        self.disabled = False
        self.update_models()

    def fetch_models(self):
        if self.server.value in self.models_per_server:
            return
        server = spot_server(self.server.value)
        url = f"{server['url']}/api/tags"
        # authentication
        extra_args = {}
        if server.get("username"):
            extra_args['auth'] = (server["username"], server["password"])
        answer = requests.get(url, **extra_args)
        print("HTTP status code:", answer.status_code)
        raw = answer.json()
        # for model in sorted(raw['models'], key=lambda record: record['name']):
        #     print("Model:", model)
        models = [ record['name'] for record in raw['models'] ]
        # for usability: sort the models alphabetically
        models.sort()
        print(f"For model {self.server.value}, received models:", models)
        self.models_per_server[self.server.value] = models

    def update_models(self):
        # print("Updating models")
        # preserve current setting
        current_model = self.model.value
        self.fetch_models()
        available_models = self.models_per_server[self.server.value]
        # replace the current options with the new ones
        self.model.options = [
            ft.dropdown.Option(model) for model in self.models_per_server[self.server.value]
        ]
        # preserve setting if possible, otherwise pick first one
        if current_model in available_models:
            self.model.value = current_model
        else:
            # find the first model that does start with 
            available_models[0]
        self.page.update()

    def submit(self, event):
        # and now that the textfield itself is linked to this callback
        # we enforce it even further
        if self.disabled:
            return
        # disable the button to prevent double submission
        # mark the button as disabled for the visual effect
        self.submit_button.disabled = True
        self.disabled = True
        self.send_request(event)
        # once the request is completed we can re-enable the button
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
        # streaming or non streaming
        url = f"{server['url']}/api/generate"
        data = {'model': model, 'prompt': prompt}
        # authentication
        # see https://requests.readthedocs.io/en/latest/user/authentication/#basic-authentication
        extra_args = {}
        if server.get("username"):
            extra_args['auth'] = (server["username"], server["password"])
        # print(f"{extra_args=}")
        if not streaming:
            answer = requests.post(url, json=data, **extra_args)
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
                    print("Error:", e, type(e))
            self.page.update()
        else:
            # streaming version
            # we need to keep the connection open
            # and read the stream
            with requests.post(url, json=data, stream=True, **extra_args) as answer:
                print("HTTP status code:", answer.status_code)
                for line in answer.iter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if data['done']:
                            pass
                        history.add_chunk(data['response'])
                        self.page.update()
                    except Exception as e:
                        print(f"Exception {type(e)=}, {e=}")


def main(page: ft.Page):
    page.title = TITLE

    # we need page to be able to do updates..
    chatbot = ChatbotApp(page)
    page.add(chatbot)


ft.app(target=main)
