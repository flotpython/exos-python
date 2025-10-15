---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# the game of life

+++

## the rules

+++

Conway's game of life is a simulation that observes the following rules  
each cell has a total of 8 neighbours; depending on the number of cells alive among these 8:

- if 0 or 1: the center cell dies (famine)
- 2 or 3: the cell survives
- 4 or more: the cell dies (overpopulation)

+++

## your mission

+++

your job is fairly simple, you are to write a program that implements these; it could look like the following screenshot - but you are free to go for any other tooling / format / etc..

+++

```{image} media/game-of-life.gif
:align: center
:width: 60%
```

+++

## notes

in no particular order

- in the original definition, the screen is supposed infinite, and so as a means to better approach this on a finite screen, our implementation has the right end of the screen wrapped to the right; and same of course in the vertical direction

- this demo is implemented with `pygame` but that's not at all mandatory
