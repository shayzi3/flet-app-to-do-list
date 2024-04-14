import asyncio
import json

import flet as ft
import aiosqlite
import add_new_note as add
import change_notes as chn

from datetime import datetime as dt



async def main_page(page: ft.Page) -> None:
     page.title = 'To Do List'
     page.window_width = 500
     page.window_height = 700
     page.scroll = 'always'
     
     # * If user push on new_text_in_app that delete all vidgets and starting func add_new_note
     async def in_add_new_note(e) -> None:
          page.controls.clear()
          await add.add_note_page(page)
          
     # ! Function for change note in window appbar
     async def change_note(e) -> None:
          page.controls.clear()
          await chn.change_note_page(page, create.data)
     
     
     # TODO: Function for delete note from db     
     async def delete_note(e) -> None:
          async with aiosqlite.connect('app.db') as db:
               async with db.execute("SELECT data FROM app") as rows:
                    rows = await rows.fetchone()
                    rows: list[str] = json.loads(rows[0])
               
               del rows[rows.index(delete.data)]   # ? Delete note
               
               await db.execute("UPDATE app SET data = ?", [json.dumps(rows)])
               await db.commit()
               
          page.controls.clear()
          await main_page(page)
     
     
     # TODO: Checking in db have notes or no at user.
     async with aiosqlite.connect('app.db') as db:
          async with db.execute("SELECT data FROM app") as row:
               rows = await row.fetchone()
               rows = json.loads(rows[0])
        
        
     # ! If not notes, app show 'Empty' or show u notes.   
     show_notes_row = None  
    
     if not rows:
          # * Text in start "So emptu:( Add a new note!"
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
          list_: list[ft.CupertinoListTile] = []   # ! for keep notes
          now = dt.now()  # TODO: time now
          
         
          for i in rows:
               # ? Delete and change buttons
               delete = ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_size=15, on_click=delete_note, icon_color='white', data=i)
               create = ft.IconButton(icon=ft.icons.CREATE_OUTLINED, icon_size=15, on_click=change_note, icon_color='white', data=i)
               
               # ! Show notes
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
               
          # TODO: Column with notes
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
          alignment=ft.MainAxisAlignment.START
     )
     
     page.add(
          show_notes_row,
          new_text_in_app_row
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
     ft.app(main_page)