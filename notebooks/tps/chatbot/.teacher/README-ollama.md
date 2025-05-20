# The CPU instance

## infra

runs in a container in stupeflip

## security

runs on port 8080; no authentication

## management

to manage it, use the `ollama` command but that requires an environment variable to be set

```bash
export OLLAMA_HOST=0.0.0.0:8080
# then you can use the ollama command as usual
ollama list
ollama pull gemma2:2b
ollama pull mistral:7b
ollama pull deepseek-r1:7b
```

## testing

Using `http` (from `pip install httpie`) you can reach both instances from the command line like so:

```bash

# the CPU
http http://ollama.pl.sophia.inria.fr:8080/api/generate model=mistral:7b prompt="Hey"

# the GPU
http https://Bob:hiccup@ollama-sam.inria.fr/api/generate model=mistral:7b prompt="Hey"

# in streaming mode: CPU
http -S http://ollama.pl.sophia.inria.fr:8080/api/generate model=mistral:7b prompt="Hey" stream:=true

# in streaming mode: GPU
http -S https://Bob:hiccup@ollama-sam.inria.fr/api/generate model=mistral:7b prompt="Hey" stream:=true
```
