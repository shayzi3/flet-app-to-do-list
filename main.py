import asyncio
import json

import flet as ft
import aiosqlite

from datetime import datetime as dt


async def main(page: ft.Page) -> None:
     page.title = 'To Do List'
     page.window_width = 500
     page.window_height = 700
     
     # * If user push on new_text_in_app that delete all vidgets and starting func add_new_note
     async def in_add_new_note(e) -> None:
          page.controls.clear()
          await add_new_note(page)
          
          
     async def appbar_after_textbutton(e) -> None:
          ...
     
     # TODO: Checking in db have notes or no at user.
     async with aiosqlite.connect('app.db') as db:
          async with db.execute("SELECT data FROM app") as row:
               rows = await row.fetchone()
               rows = json.loads(rows[0])
        
        
     # ! If not notes, app show 'Empty' or show u notes.   
     show_notes_row = None  
    
     if not rows:
          show_notes_row = ft.Row(
               controls=[
                    ft.Text(
                         value='So empty:( Add a new note!',
                         text_align='start',
                         color='white'
                    )
               ]
          )
          
     elif rows:
          list_: list[ft.TextButton] = []
          for i in rows:
               list_.append(
                    ft.TextButton(
                         text=i,
                         icon=ft.icons.NOTE,
                         on_click=appbar_after_textbutton
                    )
               )
               
          show_notes_row = ft.Column(
               controls=list_,
               alignment='start'
          )
                    
     
     # ? Button for add new note
     new_text_in_app_row = ft.Row(
          controls=[
               ft.IconButton(
                    icon=ft.icons.ADD,
                    icon_size=20,
                    bgcolor='orange',
                    icon_color='white',
                    on_click=in_add_new_note,
                    tooltip='add new note',
               )
          ],
          alignment='end',
          vertical_alignment='end'
     )
     
     page.add(
          show_notes_row,
          new_text_in_app_row
     )
     
     
async def add_new_note(page: ft.Page) -> None:
     page.title = 'To Do List'
     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
     page.vertical_alignment = ft.MainAxisAlignment.START
     page.window_width = 500
     page.window_height = 700
     
     async def back(e):
          page.controls.clear()
          await main(page)
          
          
     async def write_in_db_not(e):
          if text_field.value:
               async with aiosqlite.connect('app.db') as db:
                    async with db.execute("SELECT data FROM app") as rows:
                         data = await rows.fetchone()
                         data: list[str] = json.loads(data[0])
                         
                         data.append(text_field.value)
                         print(data)
                         
                    await db.execute("UPDATE app SET data = ?", [json.dumps(data)])
                    await db.commit()
               page.controls.clear()
               await main(page)
     
     
     text_field = ft.TextField(
          label='Text',
          border_color='orange',
          text_align=ft.TextAlign.CENTER,
          multiline=True
     )
    
    
     rows = ft.Row(
          controls=[
               ft.IconButton(
                    icon=ft.icons.CHECK,
                    icon_color='white',
                    bgcolor='orange',
                    icon_size=30,
                    on_click=write_in_db_not,
                    tooltip='commit new note'
               ),
               ft.IconButton(
                    icon=ft.icons.ARROW_LEFT,
                    icon_color='white',
                    bgcolor='orange',
                    icon_size=30,
                    on_click=back,
                    tooltip='back in main menu'
               )
          ]
     )
     
     page.add(
          text_field,
          rows
     )
     
     


# ! Creates db for tracking of notes.
async def create_db() -> bool:
     async with aiosqlite.connect('app.db') as db:
          await db.execute("""CREATE TABLE IF NOT EXISTS app(
               data TEXT
               )""")
          await db.commit()
          
          await db.execute("INSERT INTO app VALUES(?)", [json.dumps([])])   # TODO: Load list in db.
          await db.commit()
     return True


if __name__ == '__main__':
     ft.app(main)