import json

import flet as ft
import search_note as sc
import aiosqlite


async def information_about_note(page: ft.Page, data: str) -> None:
     page.title = 'To Do List'
     page.window_width = 500
     page.window_height = 700
     page.scroll = 'always'
     
     async def back(e: ft.ControlEvent):
          page.controls.clear()
          await sc.change_note_page_search(page)
          
     async def delete_page(e: ft.ControlEvent):
          async with aiosqlite.connect('app.db') as db:
               async with db.execute("SELECT data FROM app") as rows:
                    rows = await rows.fetchone()
                    rows: list[str] = json.loads(rows[0])
               
               rows.remove(data)
               
               await db.execute("UPDATE app SET data = ?", [json.dumps(rows)])
               await db.commit()
          
          page.controls.clear()
          await sc.change_note_page_search(page)
          
               
     async def load_note(e: ft.ControlEvent):
          if text.value:
               async with aiosqlite.connect('app.db') as db:
                    async with db.execute("SELECT data FROM app") as rows:
                         rows = await rows.fetchone()
                         rows: list[str] = json.loads(rows[0])
                         
                    rows.remove(data)
                    rows.append(text.value)
                    
                    await db.execute("UPDATE app SET data = ?", [json.dumps(rows)])
                    await db.commit()
               
               page.controls.clear()
               await sc.change_note_page_search(page)
               
     text = ft.TextField(
          value=data,
          border_color='white',
          text_align=ft.TextAlign.START,
          multiline=True
     )
     
     appbar = ft.BottomAppBar(
          shape=ft.NotchShape.CIRCULAR,
          bgcolor=ft.colors.BLUE,
          content=ft.Row(
               controls=[
                    ft.IconButton(icon=ft.icons.CHECK, icon_color='white', icon_size=20, on_click=load_note),
                    ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_color='white', icon_size=20, on_click=delete_page),
                    ft.Column(expand=True),
                    ft.IconButton(icon=ft.icons.ARROW_LEFT, icon_color='white', icon_size=20, on_click=back)
               ]
          )
     )
     
     page.add(
          text,
          appbar
     )
     