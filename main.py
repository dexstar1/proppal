from fasthtml.common import (
    FT, fast_app, serve, Titled, Form, Fieldset, 
    Input, Button, Article, Header, P, Footer, 
    Small, Em, A, Div, Hr
)
from datetime import datetime
import sqlite3
import os

# Use environment variable for database path
DB_PATH = os.getenv('DB_PATH', "guestbook.db")

# Initialize the app and database
app, rt = fast_app()
DB_PATH = "guestbook.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Constants
MAX_NAME_CHAR = 15
MAX_MESSAGE_CHAR = 50

# CRUD Operations
def get_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, message, date FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()
    conn.close()
    return messages

def add_message(name, message, date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (name, message, date) VALUES (?, ?, ?)", 
                  (name, message, date))
    conn.commit()
    conn.close()

def delete_message(message_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()

def update_message(message_id, name, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE messages SET name = ?, message = ? WHERE id = ?", 
                  (name, message, message_id))
    conn.commit()
    conn.close()

# Render Functions
def render_message(entry):
    return Article(
        Header(f"Name: {entry[1]}"),
        P(f"Message: {entry[2]}"),
        Footer(Small(Em(f"Posted: {entry[3]}"))),
        Div(
            A("Edit",
              href="#",
              hx_get=f"/edit/{entry[0]}",
              hx_target="#form-container",
              hx_swap="innerHTML"),
            A("Delete",
              href="#",
              hx_post=f"/delete/{entry[0]}",
              hx_target="#message-list",
              hx_swap="outerHTML",
              style="color: red;"),
        )
    )

def render_message_list():
    return Div(
        *[render_message(entry) for entry in get_messages()],
        id="message-list"
    )

def create_base_form(action="/add", button_text="Submit"):
    return Form(
        Fieldset(
            Input(
                type='text',
                name='name',
                placeholder='Name',
                required=True,
                maxlength=MAX_NAME_CHAR,
            ),
            Input(
                type='text',
                name='message',
                placeholder='Message',
                required=True,
                maxlength=MAX_MESSAGE_CHAR,
            ),
            Button(button_text, type="submit"),
            role='group',
        ),
        method="post",
        hx_post=action,
        hx_target="#theContent",  # Target the entire body to update both form and list
        hx_swap="innerHTML"
    )

def render_content():
    return Div(
        Div(create_base_form(), id="form-container"),
        Hr(),
        render_message_list(), 
        id="theContent",
    )

# Routes
@rt('/add', methods=['post'])
async def add(req):
    form_data = await req.form()
    name = form_data.get('name')
    message = form_data.get('message')
    if name and message:
        add_message(name, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Return both the reset form and updated message list
    return Div(
        Div(create_base_form(), id="form-container"),
        Hr(),
        render_message_list(), 
        id="theContent",
    )

@rt('/delete/{message_id}', methods=['post'])
async def delete(message_id: int):
    delete_message(message_id)
    return render_message_list()

@rt('/edit/{message_id}', methods=['get'])
async def edit(message_id: int):
    message = [msg for msg in get_messages() if msg[0] == message_id][0]
    form = Form(
        Fieldset(
            Input(
                type='text',
                name='name',
                value=message[1],
                required=True,
                maxlength=MAX_NAME_CHAR,
            ),
            Input(
                type='text',
                name='message',
                value=message[2],
                required=True,
                maxlength=MAX_MESSAGE_CHAR,
            ),
            Button("Update", type="submit"),
            role='group',
        ),
        method="post",
        hx_post=f"/update/{message_id}",
        hx_target="#theContent",  # Target the entire body to update both form and list
        hx_swap="innerHTML"
    )
    return form

@rt('/update/{message_id}', methods=['post'])
async def update(message_id: int, req):
    form_data = await req.form()
    name = form_data.get('name')
    message = form_data.get('message')
    if name and message:
        update_message(message_id, name, message)
        # Return both the reset form and updated message list
        return Div(
            Div(create_base_form(), id="form-container"),
            Hr(),
            render_message_list(), 
            id="theContent",
        )
    return "Error updating message"

@rt('/')
def get():
    return Titled('My Guestbook', render_content())

serve()