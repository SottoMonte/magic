# Import
import sys
sys.path.append('src/core/')
sys.path.append('src/ide/')
import worker
import application
import asyncio
import ide
import flet as ft

'''
# Markdown
![Test image](https://picsum.photos/200/300)
https://www.youtube.com/embed/PHjelW_FwSM?si=_0PNrXJS39GDU7vb
[![](https://markdown-videos-api.jorgenkh.no/youtube/dQw4w9WgXcQ)](https://youtu.be/dQw4w9WgXcQ)
## Flet community

* [Discussions](https://github.com/flet-dev/flet/discussions)
* [Discord](https://discord.gg/dzWXP8SHG8)
* [Twitter](https://twitter.com/fletdev)
* [Email](mailto:hello@flet.dev)
### Code
```
void main() {
  runApp(MaterialApp(
    home: Scaffold(
      body: ft.Markdown(data: markdownData),
    ),
  ));
}
```
'''
# main gui
def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
# test
async def Test(worker:worker):
    
    pass
# main
if __name__ == "__main__":
    app = application.mathemagic("example.cli",sys.argv,{application.INTERFACE.CLI:application.CLI,application.INTERFACE.GUI:ide.GUI})
    #app.JOB(Test)
    app.RUN()