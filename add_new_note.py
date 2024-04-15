import json

import flet as ft
import aiosqlite
import main as mn



async def add_note_page(page: ft.Page) -> None:
     page.title = 'To Do List'
     page.window_width = 500
     page.window_height = 700
     page.scroll = 'always'
     
     async def back(e):
          page.controls.clear()
          await mn.main_page(page)
          
          
     async def write_in_db_note(e):
          if text_field.value:
               async with aiosqlite.connect('app.db') as db:
                    async with db.execute("SELECT data FROM app") as rows:
                         data = await rows.fetchone()
                         data: list[str] = json.loads(data[0])
                         
                         data.append(text_field.value)
                         
                    await db.execute("UPDATE app SET data = ?", [json.dumps(data)])
                    await db.commit()
                    
               page.controls.clear()
               await mn.main_page(page)
     
     
     text_field = ft.TextField(
          hint_text='Напиши заметку...',
          border_color='white',
          text_align=ft.TextAlign.CENTER,
          multiline=True
     )
     
     rows = ft.BottomAppBar(
         bgcolor=ft.colors.BLUE,
         shape=ft.NotchShape.CIRCULAR,
         content=ft.Row(
              controls=[
                   ft.IconButton(
                        icon=ft.icons.CHECK,
                        icon_color='white',
                        icon_size=20,
                        on_click=write_in_db_note,
                        tooltip='commit new note'
                    ),
                   ft.Column(expand=True),
                   
                   ft.IconButton(
                        icon=ft.icons.ARROW_LEFT,
                        icon_color='white',
                        icon_size=20,
                        on_click=back,
                        tooltip='back in main menu'
                    )
              ],
              alignment='start'
         ),
         height=70
    )
    
     
     page.add(
          text_field,
          rows
     )