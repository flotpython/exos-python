# flotpython exos: pure Python

this repo contains exercises and TPs that [complement the Python MOOC](https://www.fun-mooc.fr/en/cours/python-3-des-fondamentaux-aux-concepts-avances-du-langage/)

excluded are the auto-corrected exercises mentioned in the MOOC
[these are bundled with the main course repo](https://github.com/flotpython/course)

in the present repo we try to gather all the other, generally more informal,
material for **practising pure Python** (for numpy etc. see the other repo
<https://github.com/flotpython/exos-ds>)

## there is no runtime tool here !

also note that, as opposed to the auto-corrected exercises mentioned above,
there is a **deliberate choice to not provide a notebooks infrastructure**  
this is because we want our students to become autonomous, so it means they are
supposed to solve all these problems **on their own laptop**, where they are
expected to have acquired the skills for installing and managing a decent
software stack (typically bash + vscode + python + ipython + jupyter)  
the fact that most of the material is written as a notebook is mostly a
convenience, both for authoring (outputs are up-to-date), and of course in cases
where the starting material is a notebook itself  
if you can really not install anything on your laptop, you can in last resort
use [the emergency resources at the bottom of this page](label-lite-tools)

## contents

the material is organized along these rather vague categories:

* `exos`: short, simple one-shot assignments
* `tps`: more elaborate assignments, with several steps, that let students
  achieve something
* `howtos`: more for reading than for practising, that can be recipes to achieve
  some common tasks

as well as, less interesting probably, some low-order categories like `samples`, `reading`, `quizzes`, etc.

**historical note**: in an older version, this repo contained material about both pure Python and the Data Science tools; it has been split in two to ease its maintenance - github slugs are now `flotpython/exos-python` and `flotpython/exos-ds` respectively

## formats & jupytext

as noted above, most of the contents is written as notebooks; all notebooks are
jupytext-encoded using either `py:percent` or `md:myst` formats  
you will **need to `pip install jupytext`** to be able to read those as notebooks  
also all notebooks have their filename prefix ending in `-nb` to help the
distinction between notebooks and pure Python or pure markdown

(label-autoreload)=
## note on autoreload in ipython or notebooks

please read this through if you use IPython or Jupyter on your laptop

### the problem

you are in `ipython` or in a notebook and you do

```
from my_module import my_function
my_function(...)
```

then later on, you modify `my_module.py` under vs-code, and you want to try the
new version; your first idea is to redo the import to load the new version into
your interpreter

when then, **BEWARE** because **a second `import` will not reload the file**  
this is intended, and desirable, because loading a module is costly; so the
interpreter caches its loaded modules, and long story short, you can re-import
as much as you want, you still run the old code !

### the solution

**to work around this situation**: with the trick that follows, you won't even
need to re-import, you will just need to re-run `my_function()` and you will use
the latest version (provided that the new module actually has no error that
prevents it from loading, of course)

you just need to add in a file named

```
~/.ipython/profile_default/ipython_config.py
```

the following lines

```python
c.InteractiveShellApp.exec_lines = []
c.InteractiveShellApp.exec_lines.append('%load_ext autoreload')
c.InteractiveShellApp.exec_lines.append('%autoreload 2')
```

to achieve that, if you have bash-compatible terminal (like for example on
windows: git for bash), you can just cut-and-paste the following snippet to
configure that on your computer:

```bash
mkdir -p ~/.ipython/profile_default
cat >> ~/.ipython/profile_default/ipython_config.py << EOF
c.InteractiveShellApp.exec_lines = []
c.InteractiveShellApp.exec_lines.append('%load_ext autoreload')
c.InteractiveShellApp.exec_lines.append('%autoreload 2')
EOF
```

(label-lite-tools)=
## last resort computing resources

if you really cannot install anything on your laptop, you can use this instead  
this is a best effort, not everything works exactly like on a laptop  

you should first check whether you can effectively save your work; in
particular, keep in mind that the only place where your work is likely to be
saved is .. in the brower itself; so for example using another browser, or *a
fortiori* another computer, will likely make you lose your work

### a browser-based REPL


`````{admonition} browser-hosted IPython console
:class: seealso dropdown

````{div}
```{replite}
:kernel: python
:theme: JupyterLab Light
:width: 100%
:height: 90vh
:prompt: click to start a console
:prompt_color: yellow

# please be patient ...
print("welcome to Python in the browser")

```
````
`````

### a browser-based JupyterLab

`````{admonition} browser-hosted Jupyter Lab
:class: seealso dropdown

````{div}
```{jupyterlite}
:kernel: python
:theme: JupyterLab Light
:width: 100%
:height: 90vh
:prompt: click to start a JuptyerLab
:prompt_color: pink

# please be patient ...
print("welcome to Python in the browser")

```
````
`````
