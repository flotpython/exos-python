"""
just the skeleton as a demonstration of the layout
"""

import flet as ft

def puzzle8():
    """
    returns a Column object suitable for inserting in a Page
    """
    game_widget = ft.Column(
        [
            ### header
            ft.Row([
                # message area
                ft.Text("a message area")
            ]),
            # main area
            ft.GridView(
                # the 9 digits
                [ ft.TextField(str(i)) for i in range(9) ],
                runs_count=3,
            ),
            # footer
            ft.Row([
                # the bottom buttons
                ft.IconButton(ft.Icons.SHUFFLE),
                ft.IconButton(ft.Icons.START),
            ]),
        ]
    )
    return game_widget

def main(page):
    page.title = "Puzzle 8"
    page.window.width = 400
    page.window.resizable = False

    # insert the game widget in the main page
    page.add(puzzle8())

ft.app(main)
