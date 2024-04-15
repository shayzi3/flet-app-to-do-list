import json

import flet as ft
import aiosqlite
import main as mn

from datetime import datetime as dt

from numba import prange


async def change_note_page(page: ft.Page):
     page.title = 'To Do List'
     page.window_width = 500
     page.window_height = 700
     page.scroll = 'always'
     
     
     async def search(e):
          if text.value:
               page.controls.clear()
               await change_note_page(page)
               
               async with aiosqlite.connect('app.db') as db:
                    async with db.execute("SELECT data FROM app") as row:
                         row = await row.fetchone()
                         row: list[str] = json.loads(row[0])
                         
               result = []
               split_ = text.value.split()
               for index in prange(len(row)):
                    for item in prange(len(split_)):
                         
                         if split_[item].lower() in row[index].lower():
                              delete = ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_size=15, on_click=..., icon_color='white', data=row[index])
                              change = ft.IconButton(icon=ft.icons.CREATE_OUTLINED, icon_size=15, on_click=..., icon_color='white', data=row[index])
               
                              result.append(
                                   ft.CupertinoListTile(
                                        subtitle=ft.Text(dt.now().strftime('%A, %d %B %Y %I: %M %p')),
                                        title=ft.Text(row[index]),
                                        leading=ft.Icon(name=ft.icons.NOTE, color='white'),
                                        trailing=ft.Row(
                                             controls=[
                                                  delete,
                                                  change
                                             ]
                                        )
                                   )
                              )
                              
               if not result:
                    result = 'Nothing found'
                    show_notes_row = ft.CupertinoListTile(
                         ft.Text(result),
                         leading=ft.Icon(name=ft.icons.CLEAR, color='white')
                    )

               else:
                    show_notes_row = ft.Column(
                         controls=result,
                         alignment='center'
                    )
               
               page.add(
                    show_notes_row
               )
                              
          
     async def back(e):
          page.controls.clear()
          await mn.main_page(page)
     
     
     text = ft.TextField(
          hint_text='Write a word or letter',
          border_color='white',
          text_align=ft.TextAlign.CENTER,
          multiline=True,
          height=63
     )
     
     appbar = ft.BottomAppBar(
          shape=ft.NotchShape.CIRCULAR,
          bgcolor=ft.colors.BLUE,
          content=ft.Row(
               controls=[
                    ft.IconButton(icon=ft.icons.SEARCH, icon_color='white', icon_size=20, on_click=search),
                    ft.Column(expand=True),
                    ft.IconButton(icon=ft.icons.ARROW_LEFT, icon_color='white', icon_size=20, on_click=back)
               ]
          ),
          height=70
     )
     
     page.add(
          text,
          appbar
     )
     
     