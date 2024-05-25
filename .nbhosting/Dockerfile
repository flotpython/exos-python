# --------
# using scipy, it's kinda big but that should not be a problem
# base-notebook lacks at least numpy, widgets, so...
FROM nbhosting/minimal-notebook

# NOTE
# we cannot use jupyter nbextension enable/disable
# because we provide our own nbconfig/notebook.json
# and that is where is stored the enabled/disabled extensions
RUN true \
 && pip install jupyterlab notebook jupytext jupyterlab-myst \
 && pip install jupyterlab-courselevels \
 && pip install nbautoeval ipythontutor \
 && pip install numpy pandas matplotlib ipywidgets ipympl \
 && pip install folium \
 && apt-get install -y graphviz && pip install graphviz \
 && true
