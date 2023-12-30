import flet as ft
import os
import work_space as WorkSpace


def builder_root(path,view,event=None):
    print("::",path)
    for root, dirs, files in os.walk(path):
        print(root)
        for file in files:
            view.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(root+'/'+file)),
                        ft.DataCell(ft.Text("6 hours ago")),
                    ],on_select_changed=event
                ))

def builder(page,hh,insp,lista):
    open = ft.Container(alignment = ft.alignment.top_center,bgcolor=ft.colors.BLUE_100,expand=1,content=ft.ListView([],expand=True))

    dire = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Last Change")),
            ],
            #show_checkbox_column=True,
            rows=[],
            expand=1,
            
        )
    
    tests = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Last Change")),
            ],
            #show_checkbox_column=True,
            rows=[],
            expand=1,
            
        )

    run_debug = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Last Change")),
            ],
            #show_checkbox_column=True,
            rows=[],
            expand=1, 
    )

    doc = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Last Change")),
            ],
            #show_checkbox_column=True,
            rows=[],
            expand=1, 
    )

    async def button_clicked_doc(e):
        file = ""

        print(type(e))
        for x in doc.rows:
            print(e.target,x.uid)
            if e.target == x.uid:
                print(dir(x.cells[0]))
                print(x.cells[0].content.value)
                file = x.cells[0].content.value
                
        print(dir(dire.rows))
        print("-->",type(e.target))
        print(f"row select changed: {e.data}")
        #hh.tabs = []
        #print(page,hh)

        tab = ft.Tab(
                text=file,
                icon=ft.icons.INSERT_DRIVE_FILE_SHARP,
                content=WorkSpace.file_builder(file),
        )
        hh.tabs.append(tab)

        #insp.controls.append(WorkSpace.inspector_obj(insp,insp,file))
        
        await page.update_async()
    
    async def button_clicked_examples(e):
        file = ""

        print(type(e))
        for x in run_debug.rows:
            print(e.target,x.uid)
            if e.target == x.uid:
                print(dir(x.cells[0]))
                print(x.cells[0].content.value)
                file = x.cells[0].content.value
                
        print(dir(dire.rows))
        print("-->",type(e.target))
        print(f"row select changed: {e.data}")
        #hh.tabs = []
        #print(page,hh)

        tab = ft.Tab(
                text=file,
                icon=ft.icons.INSERT_DRIVE_FILE_SHARP,
                content=WorkSpace.file_builder(file),
        )
        hh.tabs.append(tab)

        #insp.controls.append(WorkSpace.inspector_obj(insp,insp,file))
        
        await page.update_async()
    
    async def button_clicked_test(e):
        file = ""

        print(type(e))
        for x in tests.rows:
            print(e.target,x.uid)
            if e.target == x.uid:
                print(dir(x.cells[0]))
                print(x.cells[0].content.value)
                file = x.cells[0].content.value
                
        print(dir(dire.rows))
        print("-->",type(e.target))
        print(f"row select changed: {e.data}")
        #hh.tabs = []
        #print(page,hh)

        tab = ft.Tab(
                text=file,
                icon=ft.icons.INSERT_DRIVE_FILE_SHARP,
                content=WorkSpace.file_builder(file),
        )
        hh.tabs.append(tab)

        #insp.controls.append(WorkSpace.inspector_obj(insp,insp,file))
        
        await page.update_async()

    builder_root(os.getcwd()+'/docs',doc,button_clicked_doc)
    builder_root(os.getcwd()+'/examples',run_debug,button_clicked_examples)
    builder_root(os.getcwd()+'/tests',tests,button_clicked_test)

    tree = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    assistant = ft.Text("ChatGPT", size=10)
    
    manufacture =  ft.Card(
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.AUTO_MODE_SHARP),
                            title=ft.Text("pyproject.toml"),
                            subtitle=ft.Text("automating the building."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.BOOKMARK_SHARP),
                            title=ft.Text("README.md"),
                            subtitle=ft.Text("file that provides an introduction to a project."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.LOCAL_POLICE_SHARP),
                            title=ft.Text("LICENSE"),
                            subtitle=ft.Text("file is a document that outlines the terms and conditions for using a particular software package."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.GROUP_SHARP),
                            title=ft.Text("CONTRIBUTING.md"),
                            subtitle=ft.Text("file that provides guidelines for contributing to a project."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PUBLISHED_WITH_CHANGES),
                            title=ft.Text("CHANGELOG.md"),
                            subtitle=ft.Text("file is a document that lists the changes, updates, and fixes made to a project across different versions."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.symmetric(vertical=10),
            )
        )

    manager =  ft.Card(
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.FOLDER_SHARP),
                            title=ft.Text("Explorer"),
                            subtitle=ft.Text("explore project files."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.HELP_SHARP),
                            title=ft.Text("Documentation"),
                            subtitle=ft.Text("accompanies a software, with the aim of explaining what functions the software performs, how it is structured and implemented and how it is used."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.LIST_SHARP),
                            title=ft.Text("Table of Content"),
                            subtitle=ft.Text("file contents table."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ACCOUNT_TREE),
                            title=ft.Text("Source Control"),
                            subtitle=ft.Text("source version control."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PLAY_ARROW),
                            title=ft.Text("Run and Debug"),
                            subtitle=ft.Text("execution and debugging."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.SCIENCE_SHARP),
                            title=ft.Text("Testing"),
                            subtitle=ft.Text("Software testing."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PRECISION_MANUFACTURING),
                            title=ft.Text("Producing"),
                            subtitle=ft.Text("Software manufacture."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.AUTO_AWESOME),
                            title=ft.Text("Assistant AI"),
                            subtitle=ft.Text("AI pair programmer that helps you write better code."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Disability"),
                                    ft.PopupMenuItem(text="Uninstall"),
                                ],
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.symmetric(vertical=10),
            )
        )

    async def extension_folder(e):
        open.content.controls = [dire]
        await e.page.update_async()
    async def extension_content(e):
        open.content.controls = [lista]
        await e.page.update_async()
    async def extension_tree(e):
        open.content.controls = [tree]
        await e.page.update_async()
    async def extension_test(e):
        open.content.controls = [tests]
        await e.page.update_async()
    async def extension_manufacture(e):
        open.content.controls = [manufacture]
        await e.page.update_async()
    async def extension_assistant(e):
        open.content.controls = [assistant]
        await e.page.update_async()
    async def extension_manager(e):
        open.content.controls = [manager]
        await e.page.update_async()
    async def extension_run_debug(e):
        open.content.controls = [run_debug]
        await e.page.update_async()
    async def extension_doc(e):
        open.content.controls = [doc]
        await e.page.update_async()
    

    menu = ft.Container(width=65,alignment=ft.alignment.center,content=ft.ListView([
         ft.IconButton(
                    icon=ft.icons.FOLDER_SHARP,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="Explorer",
                    on_click=extension_folder
                ),
         ft.IconButton(
                    #icon=ft.icons.BOOKMARK_SHARP,
                    icon=ft.icons.LIST_SHARP,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="List of Contents",
                    on_click=extension_content
                ),
        ft.IconButton(
                    icon=ft.icons.ACCOUNT_TREE,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="Source Control",
                    on_click=extension_tree
                ),
        ft.IconButton(
                    icon=ft.icons.HELP_SHARP,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="Documentation",
                    on_click=extension_doc
                ),
        ft.IconButton(
                    icon=ft.icons.EXTENSION_SHARP,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="Extension",
                    on_click=extension_manager
                ),
        ft.IconButton(
                    icon=ft.icons.PLAY_ARROW,
                    #icon=ft.icons.BUG_REPORT_SHARP,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="Run and Debug",
                    on_click=extension_run_debug
                ),
        ft.IconButton(
                    icon=ft.icons.SCIENCE_SHARP,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="Testing",
                    on_click=extension_test
                ),
        ft.IconButton(
                    icon=ft.icons.PRECISION_MANUFACTURING,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="Producing",
                    on_click=extension_manufacture
                ),
        ft.IconButton(
                    icon=ft.icons.AUTO_AWESOME,
                    icon_color="blue400",
                    icon_size=48,
                    tooltip="Assistant AI",
                    on_click=extension_assistant
                )
    ],expand=1, spacing=0, padding=0, auto_scroll=True))
    
    async def button_clicked(e):
        file = ""

        print(type(e))
        for x in dire.rows:
            print(e.target,x.uid)
            if e.target == x.uid:
                print(dir(x.cells[0]))
                print(x.cells[0].content.value)
                file = x.cells[0].content.value
                
        print(dir(dire.rows))
        print("-->",type(e.target))
        print(f"row select changed: {e.data}")
        #hh.tabs = []
        #print(page,hh)

        tab = ft.Tab(
                text=file,
                icon=ft.icons.INSERT_DRIVE_FILE_SHARP,
                content=WorkSpace.file_builder(file),
        )
        hh.tabs.append(tab)

        #insp.controls.append(WorkSpace.inspector_obj(insp,insp,file))
        
        await page.update_async()



    builder_root(os.getcwd(),dire,button_clicked)
    
    open.content.controls = [dire]
    

    return ft.Row([menu,open])