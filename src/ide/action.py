tree_view = dict()


async def plus_click(e):
    global tree_view
    #txt_number.value = str(int(txt_number.value) + 1)
    tree_view['box'].value = str(int(tree_view['box'].value) + 1)
    #e.control.icon_size = 2
    #print('FATTO',dir(e.control),e.target,e.name,e.page,e.data,e.control)
    print(id(tree_view))
    await e.page.update_async()

async def men_click(e):
    global tree_view
    #txt_number.value = str(int(txt_number.value) + 1)
    tree_view['box'].value = str(int(tree_view['box'].value) - 1)
    #e.control.icon_size = 2
    #print('FATTO',dir(e.control),e.target,e.name,e.page,e.data,e.control)
    await e.page.update_async()