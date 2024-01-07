import flet as ft
import os
import aiofiles
import random

def inspector_obj(insp,data,varname):
    colori = ["red", "grey", "orange", "amber", "blue", "indigo",'pink','lime','green','teal','cyan']
    colore_casuale = random.choice(colori)

    async def new(e):
        file = ""

        print(type(e),insp.controls[0].rows)
        for x in insp.controls[0].rows:
            print(e.target,x.uid)
            if e.target == x.uid:
                print(dir(x.cells[0]))
                print(x.cells[0].content.value)
                file = x.cells[1].content.value
                i = getattr(insp,file)
                insp.controls.append(inspector_obj(insp,i,file))
        print(f"row select changed: {e.data}")
        await e.page.update_async()


    rows = []
    for name in dir(data):
        if not name.startswith("_"):
            try:
                i = getattr(data, name)
                rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(type(i),color="white",size=17)),
                        ft.DataCell(ft.Text(name,color="white",size=17)),
                        ft.DataCell(ft.Text(str(i),color="white",size=17)),
                    ]
                    ,on_select_changed=new,
                ))
            except AttributeError:
                pass
                
    return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Type",color="white",size=20)),
                ft.DataColumn(ft.Text("Identifier",color="white",size=20)),
                ft.DataColumn(ft.Text("Content",color="white",size=20)),
            ],
            rows=rows,
            bgcolor=colore_casuale,
            expand=True,
            tooltip=f"{type(data)}:{varname}",
        )

def block(tabelle,data,type="code"):
    
    out = None
    if type == 'code':
        out = ft.TextField(
            multiline=True,
            value=data,
            border="none",
            text_size=20,
        )
    else:
        out = ft.Markdown(
            data,
            selectable=True,
            code_theme="atom-one-dark",
            extension_set="gitHubWeb",
            code_style=ft.TextStyle(font_family="Roboto Mono"),
            on_tap_link=lambda e: page.launch_url(e.data),
        )

    async def action_save(e):
        file = ""
        bottoni = tabelle.tabs[0].content.controls[0].controls[0]
        #box = block.content.controls[0].controls[0]
        try:
            print(dir(tabelle.tabs))
            print(tabelle.selected_index)
            #print()
            f = open(tabelle.tabs[tabelle.selected_index].text, "w")
            first = True
            for block in tabelle.tabs[tabelle.selected_index].content.controls:
                #print(block.controls[0].content.value[-1:])
                if first == True:
                    f.write(block.controls[0].content.value)
                    first = False
                else:
                    f.write('\n'+block.controls[0].content.value)
                #print(block.controls[0].controls.content.value)
            f.close()
        except Exception as e:
            print(e)
        
        #e.control.disabled = True
        await e.page.update_async()

    async def action_delete(e):
        file = ""
        #box = block.content.controls[0].controls[0]
        try:
            print(dir(tabelle.tabs))
            print(tabelle.selected_index)
            
            for block in tabelle.tabs[tabelle.selected_index].content.controls:
                if block.controls[1].content.controls[3].uid == e.target:
                    tabelle.tabs[tabelle.selected_index].content.controls.remove(block)
    

        except Exception as e:
            print(e)
        
        #e.control.disabled = True
        await e.page.update_async()

    async def action_add_top(e):
        file = ""
        #box = block.content.controls[0].controls[0]
        try:
            print(dir(tabelle.tabs))
            print(tabelle.selected_index)
            
            for blockk in tabelle.tabs[tabelle.selected_index].content.controls:
                if blockk.controls[1].content.controls[0].uid == e.target:
                    idx = tabelle.tabs[tabelle.selected_index].content.controls.index(blockk)
                    print(idx)
                    tabelle.tabs[tabelle.selected_index].content.controls.insert(idx,block(tabelle,"","code"))
                    break
    

        except Exception as e:
            print(e)
        
        #e.control.disabled = True
        await e.page.update_async()

    async def action_add_bot(e):
        file = ""
        #box = block.content.controls[0].controls[0]
        try:
            print(dir(tabelle.tabs))
            print(tabelle.selected_index)
            
            for blockk in tabelle.tabs[tabelle.selected_index].content.controls:
                if blockk.controls[1].content.controls[1].uid == e.target:
                    idx = tabelle.tabs[tabelle.selected_index].content.controls.index(blockk)
                    tabelle.tabs[tabelle.selected_index].content.controls.insert(idx+1,block(tabelle,"","code"))
                    break
                    
    

        except Exception as e:
            print(e)
        
        #e.control.disabled = True
        await e.page.update_async()

    zz = ft.Container(padding=6,content=ft.Row(spacing=10,alignment=ft.MainAxisAlignment.END, controls=[
        ft.FilledButton("Top", icon="add", on_click=action_add_top),
        ft.FilledButton("Bottom", icon="add",on_click=action_add_bot),
        ft.FilledButton("Save", icon="save",on_click=action_save),
        ft.FilledButton("Delete", icon=ft.icons.DELETE,on_click=action_delete),
        ]))
    pp = ft.Container(padding=10,content=out,bgcolor=ft.colors.WHITE)

    return ft.Stack([pp,zz])


def file_builder(file,tabs):
    lv = ft.ListView([],expand=True, spacing=10, padding=20)
    #lv.controls.append(ft.Text(f"Line {count}"))
    #async with aiofiles.open(file, mode='r') as f:
        #contents = await f.read()
    print(file)
    with open(file, 'r') as f:
        contenuto = f.read()
        blocchi = []
        name = None
        job_b = ""
        make = False
        lines = contenuto.split('\n')
        for line in lines:
            if ((line.startswith("#") or line.startswith("'''")) and  make == False):
                name = line
                
                if job_b != "" and name != None and make == False:
                    print(line)
                    blocchi.append(job_b)
                    job_b = ""
                    make = False
                
                job_b += name + '\n'
                    
                

                if line.startswith("'''"):
                    #job_b += name + '\n'
                    make = True
                
            elif (line.startswith("'''") and make == True):
                job_b += name + '\n'
                blocchi.append(job_b)
                job_b = ""
                make = False
                
            else:

                job_b += line + '\n'
        if job_b != "":
                    blocchi.append(job_b)
        #blocchi = contenuto.split('#block')
    for blocco in blocchi:
        if blocco.count("'''") == 2:
            g =blocco.replace("'''", '').strip()
            lv.controls.append(block(tabs,g,"s"))
        else:lv.controls.append(block(tabs,blocco.strip()))

    return lv

def builder(page,lista):
    
    items = []

    '''for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            #if file.endswith('.plt'):
            #items.append(file_builder(file))
            pass
                #f = open(file, 'r')'''

    tabs = ft.Tabs(
        indicator_tab_size=True,
        selected_index=1,
        animation_duration=300,
        tabs=[],
        expand=1,
    )

    async def tabchange(e):
        filter = lista.controls[0].controls[0]
        list_view = lista.controls[1]
        list_view.controls.clear()
        #print(tabs.selected_index)
        for item in tabs.tabs[tabs.selected_index].content.controls:
                valore = ""
                for x in item.controls[0].content.value.split('\n'):
                    if x.startswith("#"):
                        valore += "\n" + x
                    elif x.startswith("##"):
                        valore += "\n" + x
                    elif x.startswith("###"):
                        valore += "\n" + x
                if valore == "":
                    valore = item.controls[0].content.value.split('\n')[0]
                if filter.value.strip() != "":
                    if item.controls[0].content.value.count(filter.value.strip()) > 0:
                        list_view.controls.append(ft.Text(str(valore),size=18))
                else:
                    list_view.controls.append(ft.Text(str(valore),size=18))

        await e.page.update_async()

    tabs.on_change=tabchange
    
    
    

    

    '''for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            cont = open(file, 'r')
            items.append(ft.Tab(
                tab_content=ft.Icon(ft.icons.SEARCH),
                content=file_builder(file),
            ))
        break

    zz.tabs = items'''

    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
    }
    
    inspector = ft.Row(spacing=0, controls=[],vertical_alignment=ft.CrossAxisAlignment.START,expand=1)
    inspector.controls.append(inspector_obj(inspector,inspector,'inspector'))

    #dati = ft.Container(content=ft.ListView([inspector],expand=1, spacing=0, padding=0),bgcolor=ft.colors.LIGHT_BLUE_ACCENT_700)
    dati = ft.ListView([inspector], spacing=0, padding=0)

    bottom = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="TERMINAL",
                icon=ft.icons.TERMINAL_SHARP,
                content=ft.Text("This is Tab 3"),
            ),
            ft.Tab(
                text="PORTS",
                icon=ft.icons.IMPORT_EXPORT_OUTLINED,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    async def move_divider_top(e: ft.DragUpdateEvent):
        tot = c.height + e.delta_y
        if tot <= 400 and tot >= 200:
            c.height += e.delta_y
        else:
                if e.delta_y < 0:
                    c.height = 200
                else:
                    c.height = 400
            
        await c.update_async()

    async def move_divider_bottom(e: ft.DragUpdateEvent):
        ass = 0
        if e.delta_y < 0:
            ass = abs(e.delta_y)
        else:
            ass = ass -  abs(e.delta_y)
        #print(bot.height + ass)
        if (e.delta_y < 0 and bot.height < 500) or (e.delta_y > 0 and bot.height > 250):
            tot = bot.height +ass
            if tot >= 250 and tot <= 500:
                bot.height += ass
            else:
                if ass < 0:
                    bot.height = 250
                else:
                    bot.height = 500

        #print(bot.height,e.delta_y,ass)
        await bot.update_async()

    async def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_UP_DOWN
        await e.control.update_async()
    
    c = ft.Container(
        height=100,
        content=dati,
        #expand=True,
        # expand=1,
    )

    bot = ft.Container(
        height=400,
        content=bottom,
        #expand=True,
        # expand=1,
    )

    return  tabs,inspector,ft.Column(
        [
            c,
            ft.GestureDetector(
                content=ft.Divider(thickness=8,color=ft.colors.BLUE_300),
                on_pan_update=move_divider_top,
                on_hover=show_draggable_cursor,
            ),
            ft.Container(
                alignment=ft.alignment.center, expand=1,content=tabs
            ),
            ft.GestureDetector(
                content=ft.Divider(thickness=8,color=ft.colors.BLUE_300),
                on_pan_update=move_divider_bottom,
                on_hover=show_draggable_cursor,
            ),
            bot,
        ],
        spacing=0,
        expand=True
    )