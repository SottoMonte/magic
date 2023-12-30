# GUI
import flet as ft
import status_bar as StatusBar
import work_space as WorkSpace
import app_bar as AppBar
import side_bar as SideBar

# IDE GUI
async def GUI(page: ft.Page):
    page.title = "Flet counter example"
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    #page.window_full_screen = True
    
    content_list = ft.Column([
        ft.Row([
            ft.TextField(
            label="Underlined filled",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text="Enter text here",
            expand=1,
            ),
            ft.IconButton(icon=ft.icons.FORMAT_LIST_NUMBERED_SHARP,icon_color="blue400",icon_size=30,tooltip="Show heading number in the document"),
        ]),
        ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    ])
    
    a,inspector,b = WorkSpace.builder(page,content_list)
    worker_space = ft.Row([
        ft.Container(bgcolor=ft.colors.BLUE_GREY_50, width=380, content=SideBar.builder(page,a,inspector,content_list)),
        ft.Container(bgcolor=ft.colors.GREY_300,expand=1, content=b),
    ],expand=1,spacing=0)
    
    top = ft.Container(bgcolor=ft.colors.LIGHT_BLUE, height=42, content=AppBar.builder(page))
    bottom = ft.Container(bgcolor=ft.colors.LIGHT_BLUE, height=32,  content=StatusBar.builder(page))

    r = ft.Column([
        top,
        ft.Container(bgcolor=ft.colors.GREEN_200,expand=1, content=worker_space),
        bottom,
    ],height=1000,width=2000,spacing=0,expand=True)

    async def page_resize(e):
        r.height= page.window_height
        r.width = page.window_width
        top.width = page.window_width
        bottom.width = page.window_width
        #print("New page size:", page.window_width, page.window_height,r.width)
        await page.update_async()

    page.on_resize = page_resize

    await page.add_async(
        r
    )