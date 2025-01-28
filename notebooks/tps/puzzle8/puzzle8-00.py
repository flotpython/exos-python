import flet as ft

def main(page):
    page.title = "My first GUI"
    page.window.width = 400
    page.window.height = 200
    page.window.resizable = False

    page.add(
        ft.Column(
            [
                ft.Text("line 1"),
                ft.Row(
                    [
                        ft.Text("line 2 gauche"),
                        ft.Text("line 2 droit")
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                ft.Text("line 3"),
            ],
        )
    )

ft.app(main)
