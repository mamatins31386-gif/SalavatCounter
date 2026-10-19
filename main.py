
import flet as ft
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("salavat.db")


def init_database():
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS counter (
                id INTEGER PRIMARY KEY,
                count INTEGER NOT NULL DEFAULT 0
            )
        """)
        connection.execute("""
            INSERT OR IGNORE INTO counter (id, count)
            VALUES (1, 0)
        """)


def load_count():
    with sqlite3.connect(DB_FILE) as connection:
        result = connection.execute(
            "SELECT count FROM counter WHERE id = 1"
        ).fetchone()
        return result[0]


def save_count(count):
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            "UPDATE counter SET count = ? WHERE id = 1",
            (count,),
        )


def main(page: ft.Page):
    page.title = "Salavat Counter"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F3F6F4"
    page.padding = 24
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    count = load_count()

    counter_text = ft.Text(
        str(count),
        size=64,
        weight=ft.FontWeight.BOLD,
        color="#176B4D",
    )

    status_text = ft.Text(
        "Salavat Counter",
        size=14,
        color="#60756A",
    )

    def update_count(new_count):
        nonlocal count

        try:
            save_count(new_count)
            count = new_count
            counter_text.value = str(count)
            status_text.value = "Saved successfully"
            status_text.color = "#176B4D"
        except sqlite3.Error:
            status_text.value = "Database error"
            status_text.color = "#B42318"

        page.update()

    def increment(e):
        update_count(count + 1)

    def reset(e):
        update_count(0)

    page.add(
        ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.FAVORITE,
                    size=48,
                    color="#176B4D",
                ),
                ft.Text(
                    "Salavat Counter",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#193B2D",
                ),
                ft.Text(
                    "اللهم صل على محمد وآل محمد",
                    size=22,
                    color="#176B4D",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=12),
                ft.Container(
                    content=counter_text,
                    alignment=ft.Alignment.CENTER,
                    width=220,
                    height=150,
                    bgcolor="#FFFFFF",
                    border_radius=24,
                ),
                ft.Button(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ADD, size=24),
                            ft.Text("Salavat", size=20),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    width=220,
                    height=60,
                    style=ft.ButtonStyle(
                        bgcolor="#176B4D",
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=16),
                    ),
                    on_click=increment,
                ),
                ft.OutlinedButton(
                    content="Reset Counter",
                    width=220,
                    on_click=reset,
                ),
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=18,
            tight=True,
        )
    )


if __name__ == "__main__":
    init_database()
    ft.run(main)
