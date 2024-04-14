import asyncio
import json

import flet as ft
import aiosqlite

from datetime import datetime as dt


async def main(page: ft.Page) -> None:
     page.title = 'To Do List'
     page.window_width = 500
     page.window_height = 700
     page.scroll = 'always'
     
     # * If user push on new_text_in_app that delete all vidgets and starting func add_new_note
     async def in_add_new_note(e) -> None:
          page.controls.clear()
          await add_new_note(page)
          
          
     async def appbar(e) -> None:
          ...
          
     async def delete_note(e) -> None:
          async with aiosqlite.connect('app.db') as db:
               async with db.execute("SELECT data FROM app") as rows:
                    rows = await rows.fetchone()
                    rows: list[str] = json.loads(rows[0])
               
               del rows[rows.index(delete.data)]
               
               await db.execute("UPDATE app SET data = ?", [json.dumps(rows)])
               await db.commit()
               
          page.controls.clear()
          await main(page)
     
     
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
          list_: list[ft.CupertinoListTile] = []
          now = dt.now()
          
         
          for i in rows:
               delete = ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_size=15, on_click=delete_note, icon_color='white', data=i)
               create = ft.IconButton(icon=ft.icons.CREATE_OUTLINED, icon_size=15, on_click=appbar, icon_color='white', data=i)
               
               list_.append(
                    ft.CupertinoListTile(
                         subtitle=ft.Text(now.strftime('%A, %d %B %Y %I: %M %p')),
                         title=ft.Text(i),
                         leading=ft.Icon(name=ft.icons.NOTE, color='white'),
                         trailing=ft.Row(
                              controls=[
                                  delete,
                                  create
                              ]
                         )
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
                    icon_color='white',
                    on_click=in_add_new_note,
                    tooltip='add new note',
               )],
          alignment=ft.MainAxisAlignment.END,
          vertical_alignment=ft.CrossAxisAlignment.END
     )
     
     page.add(
          show_notes_row,
          new_text_in_app_row
     )
     
     
async def add_new_note(page: ft.Page) -> None:
     page.title = 'To Do List'
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
                         
                    await db.execute("UPDATE app SET data = ?", [json.dumps(data)])
                    await db.commit()
               page.controls.clear()
               await main(page)
     
     
     text_field = ft.TextField(
          label='Text',
          border_color='white',
          text_align=ft.TextAlign.CENTER,
          multiline=True
     )
    
    
     rows = ft.Row(
          controls=[
               ft.IconButton(
                    icon=ft.icons.CHECK,
                    icon_color='white',
                    icon_size=30,
                    on_click=write_in_db_not,
                    tooltip='commit new note'
               ),
               ft.IconButton(
                    icon=ft.icons.ARROW_LEFT,
                    icon_color='white',
                    icon_size=30,
                    on_click=back,
                    tooltip='back in main menu'
               )
          ],
          alignment='start'
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