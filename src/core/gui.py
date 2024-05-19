import sys
tree_view = dict()
import flet as ft
import toml
import xml.etree.ElementTree as ET
sys.path.append('src/ide/')
from action import *
    

def ATTR(root):
    setable = dict({})
    for key in root.attrib:
        if key != 'id':
            match str(key):
                case 'on_click':
                    event = globals()[root.attrib[key]]
                    setable[key] = event
                case 'icon':
                    somemodule = ft.icons
                    icn = getattr(somemodule, root.attrib[key])
                    setable[key] = icn
                case 'height':setable[key] = int(root.attrib[key])
                case 'width':setable[key] = int(root.attrib[key])
                case 'spacing':setable[key] = int(root.attrib[key])
                case 'bgcolor':setable[key] = ft.colors.with_opacity(1, root.attrib[key])
                case 'color':setable[key] = ft.colors.with_opacity(1, root.attrib[key])
                case 'size':setable[key] = int(root.attrib[key])
                case 'expand':
                    if root.attrib[key] == 'True': setable[key] = True
                    else: setable[key] = int(root.attrib[key])
                case _:setable[key] = root.attrib[key]
    return setable

# fabric/build
async def BUILDER(worker,page,file):
    
    with open(file, 'r') as f:
        view = f.read()

    tree = ET.parse(file)

    root = tree.getroot()

    def mount_view(root):
        global tree_view
        print(id(tree_view))
        inn = []
        if len(root) > 0:
            for x in root:
                print(x.tag,x.attrib,len(x))
                inn.append(mount_view(x))

        match root.tag:
            case 'Container':
                setable = ATTR(root)
                item = ft.Container(content=ft.ListView(inn,expand=True),**setable)

                if 'id' in root.attrib:
                    tree_view[root.attrib['id']] = item
                    return tree_view[root.attrib['id']]
                else:return item
            case 'Text':
                setable = ATTR(root)
                item = ft.Text(root.text,**setable)

                if 'id' in root.attrib:
                    tree_view[root.attrib['id']] = item
                    return tree_view[root.attrib['id']]
                else:return item
            case 'Column':
                setable = ATTR(root)
                item = ft.Column(controls=inn,**setable)
                if 'id' in root.attrib:
                    tree_view[root.attrib['id']] = item
                    return tree_view[root.attrib['id']]
                else:return item
            case 'Row':
                #print(inn)
                #alignment=ft.MainAxisAlignment.CENTER
                setable = ATTR(root)
                item = ft.Row(controls=inn,**setable)
                if 'id' in root.attrib:
                    tree_view[root.attrib['id']] = item
                    return tree_view[root.attrib['id']]
                else:return item
            case 'IconButton': 
                setable = ATTR(root)
                #on_click=event
                item = ft.IconButton(**setable)
                if 'id' in root.attrib:
                    tree_view[root.attrib['id']] = item
                    return tree_view[root.attrib['id']]
                else:return item
            case 'TextField': 
                setable = ATTR(root)
                item = ft.TextField(value=root.text,**setable)
                if 'id' in root.attrib:
                    tree_view[root.attrib['id']] = item
                    return tree_view[root.attrib['id']]
                else:return item

    view = mount_view(root)

    return await page.add_async(view,)


# main gui
async def main(page: ft.Page):
    with open('pyproject.toml', 'r') as f:
        config = toml.load(f)

    page.title = config['gui']['title']
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    print(config['gui']['dir'])

    await BUILDER("null",page,config['gui']['dir'])