import json

import flet as ft
import aiosqlite
import main as mn


async def change_note_page(page: ft.Page, data_note: str) -> None:
     page.title = 'To Do List'
     page.window_width = 500
     page.window_height = 700
     page.scroll = 'always'
     
     async def update_data_note(e):
          async with aiosqlite.connect('app.db') as db:
               async with db.execute("SELECT data FROM app") as rows:
                    rows = await rows.fetchone()
                    rows: list[str] = json.loads(rows[0])
                    
               rows.remove(data_note)
               rows.append(text.value)
               
               await db.execute("UPDATE app SET data = ?", [json.dumps(rows)])
               await db.commit()
               
          page.controls.clear()
          await mn.main_page(page)
          
     async def back(e):
          page.controls.clear()
          await mn.main_page(page)
          
          
     
     text = ft.TextField(
          value=data_note,
          border_color='white',
          text_align=ft.TextAlign.START,
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
                         on_click=update_data_note,
                         tooltip='commit your change'
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
               alignment=ft.MainAxisAlignment.CENTER,
               vertical_alignment=ft.CrossAxisAlignment.END
          ),
          height=70
     )
     
     
     page.add(
          text,
          rows
     )
