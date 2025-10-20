"""
instead of using a hard-wired list of models,
we fetch the list of supported models at the server
at the api/tags endpoint using GET
"""

import json
from typing import Iterator

import requests
import flet as ft

# in this version we create servers as INSTANCES of CLASSES
# so we can encapsulate the logic to interact with them
#
# rationale is to be able to talk with servers that implement other APIs
# e.g. litellm that has also been deployed and on more servers

# we keep the idea of specifying our available servers as this dictionary
# but below we'll use this to create actual server INSTANCES

# provided-by-another-channel
from litellm_key import KEY as LITE_LLM_KEY

SERVER_SPECS = {
    # this one is fast because it has GPUs,
    # but it requires a login / password
    'GPU': {
        "type": "ollama",
        "name": "GPU fast",
        "url": "https://ollama-sam.inria.fr",
        "username": "Bob",
        "password": "hiccup",
    },
    # this one is slow because it has no GPUs,
    # but it does not require a login / password
    'CPU': {
        "type": "ollama",
        "name": "CPU slow",
        "url": "http://ollama.pl.sophia.inria.fr:8080",
    },
    'LiteLLM': {
        "type": "litellm",
        "name": "LiteLLM (GPUs)",
        "url": "https://litellm-sam.inria.fr",
        "key": LITE_LLM_KEY,
    }
}

TITLE = "My first Chatbot 11"

class Server:
    """
    an abstract server class
    """
    def list_model_names(self) -> list[str]:
        pass
    def generate_blocking(self, prompt, model) -> list[str]:
        """
        non-streaming generation - returns a list of text chunks
        """
        pass
    def generate_streaming(self, prompt, model) -> Iterator[str]:
        """
        streaming generation - yields text chunks
        """
        pass


class OllamaServer(Server):
    """
    for servers that comply with ollama's API
    """
    def __init__(self, name, url, username=None, password=None):
        self.name = name
        self.url = url
        self.username = username
        self.password = password

    def _authenticate_extra_args(self) -> dict:
        auth_args = {}
        if self.username is not None:
            auth_args = {
                'auth': (self.username, self.password)
            }
        return auth_args

    def list_model_names(self):
        url = f"{self.url}/api/tags"
        auth_args = self._authenticate_extra_args()
        answer = requests.get(url, **auth_args)
        print(f"HTTP retcod on {url}:", answer.status_code)
        if not (200 <= answer.status_code < 300):
            print("not 2xx, aborting")
            return []
        raw = answer.json()
        return [model['name'] for model in raw['models']]

    def generate_blocking(self, prompt, model):
        url = f"{self.url}/api/generate"
        auth_args = self._authenticate_extra_args()
        payload = {'model': model, 'prompt': prompt}
        result = []

        answer = requests.post(url, json=payload, **auth_args)
        print(f"HTTP retcod on {url}:", answer.status_code)
        if not (200 <= answer.status_code < 300):
            print("not 2xx, aborting")
            return result
        for line in answer.text.split("\n"):
            # splitting artefacts can be ignored
            if not line:
                continue
            # there should be no exception, but just in case...
            try:
                data = json.loads(line)
                # the last JSON chunk contains statistics and is not a message
                if data['done']:
                    break
                result.append(data['response'])
            except Exception as e:
                print(f"Exception {type(e)=}, {e=}")
        return result

    def generate_streaming(self, prompt, model):
        url = f"{self.url}/api/generate"
        auth_args = self._authenticate_extra_args()
        payload = {'model': model, 'prompt': prompt}
        result = []

        answer = requests.post(url, json=payload, stream=True, **auth_args)
        print(f"HTTP retcod on {url}:", answer.status_code)
        if not (200 <= answer.status_code < 300):
            print("not 2xx, aborting")
            return
        for line in answer.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line)
                if data['done']:
                    return
                yield data['response']
            except Exception as e:
                print(f"Exception {type(e)=}, {e=}")


class LitellmServer(Server):
    """
    for servers that comply with LiteLLM's API
    """
    def __init__(self, name, url, key):
        self.name = name
        self.url = url
        self.key = key

    def _authenticate_headers(self) -> dict:
        if not self.key:
            return {}
        return dict(headers={"X-API-KEY": LITE_LLM_KEY})

    def list_model_names(self):
        url = f"{self.url}/models"
        extra_args = self._authenticate_headers()
        req = requests.get(url, **extra_args)
        print(f"HTTP retcod on {url}:", req.status_code)
        if not (200 <= req.status_code < 300):
            print("not 2xx, aborting")
            return []
        raw = req.json()
        return [
            chunk['id'] for chunk in raw['data']
        ]

    def generate_blocking(self, prompt, model):
        url = f"{self.url}/v1/completions"
        payload = {
            "model": model,
            "prompt": prompt,
        }
        # print("sending POST to", url, "with payload", payload)
        req = requests.post(
            url,
            json=payload,
            **self._authenticate_headers()
        )
        print(f"HTTP retcod on {url}:", req.status_code)
        if not (200 <= req.status_code < 300):
            print("not 2xx, aborting")
            return []
        raw = req.json()
        result = []
        if 'choices' in raw:
            for choice in raw['choices']:
                result.append(choice['text'])
        return result


    def generate_streaming(self, prompt, model):
        url = f"{self.url}/v1/completions"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
        }
        # print("sending POST to", url, "with payload", payload)
        req = requests.post(
            url,
            json=payload,
            stream=True,
            **self._authenticate_headers()
        )
        print(f"HTTP retcod on {url}:", req.status_code)
        if not (200 <= req.status_code < 300):
            print("not 2xx, aborting")
            return
        for chunk in req.iter_lines():
            if not chunk:
                continue
            try:
                chunk = chunk.decode('utf-8')
                # remove extra 'data: ' prefix
                if chunk.startswith("data: "):
                    chunk = chunk[6:]
                data = json.loads(chunk)
                if 'choices' in data:
                    for choice in data['choices']:
                        yield choice['text']
            except Exception as e:
                print(f"Exception {type(e)=}, {e=}")


SERVERS = {}
for key, spec in SERVER_SPECS.items():
    match spec['type']:
        case 'ollama':
            SERVERS[key] = OllamaServer(
                name=spec['name'],
                url=spec['url'],
                username=spec.get('username', None),
                password=spec.get('password', None),
            )
        case 'litellm':
            SERVERS[key] = LitellmServer(
                name=spec['name'],
                url=spec['url'],
                key=spec['key'],
            )


class History(ft.Column):
    """
    the history is a column of text messages
    where prompts and answers alternate
    """

    def __init__(self, app):
        super().__init__(
            [ft.TextField(
                label="Type a message...",
                on_submit=lambda event: app.send_request(event),
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

    def enable_prompt(self):
        self.controls[-1].disabled = False
    def disable_prompt(self):
        self.controls[-1].disabled = True

class ChatbotApp(ft.Column):

    def __init__(self):
        # we keep a cache of available models on each server
        self.model_names_per_server = {}

        header = ft.Text(value=TITLE, size=40)

        self.streaming = ft.Checkbox(label="streaming", value=True)
        #  will be populated later
        self.model = ft.Dropdown(
            # options=[],
            width=300,
        )
        self.server = ft.Dropdown(
            options=[ft.dropdown.Option(server)
                     for server in SERVER_SPECS.keys()],
            value="GPU",
            width=100,
            on_change=lambda event: self.update_models(),
        )

        self.submit = ft.ElevatedButton("Send", on_click=self.send_request)

        self.history = History(self)

        row = ft.Row(
            [self.streaming, self.model, self.server, self.submit],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        super().__init__(
            [header, row, self.history],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        # go fetch the relevant models for the selected server
        # as explained below, at this point we are not yet in the page
        # so we cannot yet call update() at this point
        self.update_models(update=False)

    def fetch_models(self):
        # already fetched ?
        # if empty, try again
        if (self.server.value in self.model_names_per_server
            and self.model_names_per_server[self.server.value]):
            return
        server_instance = SERVERS[self.server.value]
        model_names = server_instance.list_model_names()
        # for usability: sort the models alphabetically
        model_names.sort()
        self.model_names_per_server[self.server.value] = model_names

    def update_models(self, *, update=True):
        # preserve current setting as far as possible
        current_model = self.model.value
        self.fetch_models()
        available_models = self.model_names_per_server[self.server.value]
        # replace the current options with the new ones
        self.model.options = [
            ft.dropdown.Option(model) for model in self.model_names_per_server[self.server.value]
        ]
        # preserve setting if possible, otherwise pick first one
        if current_model in available_models:
            self.model.value = current_model
        else:
            # xxx somehow the first model on GPU - all-minilm:22m-l6-v2-fp16
            # returns an error saying the model does not support generate
            # so, as a workaround, find the first model that does not start with all-
            self.model.value = next(
                model for model in available_models if not model.startswith("all-")
            )
        # a subtle point here: because we call update_models in the constructor,
        # and because at that time the app is not yet in the page
        # we cannot call update() in that circumstance()
        # BUT since this method is bound the the 'change' event on the server widget
        # in that circumstance we need to update
        if update:
            self.update()

    def send_request(self, _event):
        # disable the button to prevent double submission
        self.submit.disabled = True
        self.history.disable_prompt()
        self.send_request_2(_event)
        self.submit.disabled = False
        self.history.enable_prompt()
        self.update()


    # send the prompt to the server and display the answer
    def send_request_2(self, _event):
        model = self.model.value
        prompt = self.history.current_prompt()
        server_instance = SERVERS[self.server.value]

        # record the question asked
        self.history.add_prompt(prompt)
        # create placeholder for the answer
        self.history.add_answer("")
        # update UI
        self.update()

        # send the request
        streaming = self.streaming.value

        print(f"Sending message to {server_instance.name}, {model=}, {streaming=}, {prompt=}")

        # streaming or non streaming
        if not streaming:
            # not streaming = blocking
            answers = server_instance.generate_blocking(prompt, model)
            for text in answers:
                self.history.add_chunk(text)
            self.update()
        else:
            # streaming version
            answers = server_instance.generate_streaming(prompt, model)
            for text in answers:
                self.history.add_chunk(text)
                self.update()


def main(page: ft.Page):
    page.title = TITLE

    chatbot = ChatbotApp()
    page.add(chatbot)


ft.app(target=main)
