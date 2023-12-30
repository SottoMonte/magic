import flet as ft

def builder(page):
    zz = ft.PopupMenuButton(
        content=ft.Text("Main"),
        items=[
            ft.PopupMenuItem(text="Item 1"),
            ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="Check power"),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.HOURGLASS_TOP_OUTLINED),
                        ft.Text("Item with a custom content"),
                    ]
                ),
                on_click=lambda _: print("Button with a custom content clicked!"),
            ),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(
                text="Checked item", checked=False
            ),
        ]
    )

    return ft.Row([ft.Text(""),zz,ft.Text("Blocco:10,Riga:1,Col:10,Spaces:4"),ft.Text("Mode:edit"),ft.Text("ASCII")],spacing=25)