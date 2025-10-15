---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
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

- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

See https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life for more details

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

### wrapping 

in the original definition, the screen is supposed infinite, and so as a means to better approach this on a finite screen, our implementation has the right end of the screen wrapped to the right; and same of course in the vertical direction

### pygame

this demo is implemented with `pygame` but that's not at all mandatory
