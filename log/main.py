import flet as ft
from log.api import API
from log.database.models import LogInfo, Message
import datetime


class Record(ft.UserControl):
    def __init__(self, info: LogInfo):
        super().__init__()
        self.info = info

        # Sub-controls of the Record
        self.date_time = ft.Text(
            str(self.info.date_time.strftime("%d %B, %Y @ %I:%M:%S %p")),
            color=ft.colors.ON_SECONDARY_CONTAINER,
            style=ft.TextStyle(
                size=15,
                weight=ft.FontWeight.BOLD,
                decoration=ft.TextDecoration.UNDERLINE,
            ),
        )
        self.message = ft.Text(self.info.message.content, size=20)

        self.controls = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[self.date_time],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Row(
                        controls=[self.message],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
            ),
            padding=10,
            border=ft.border.all(1, ft.colors.ON_BACKGROUND),
            border_radius=8,
            margin=ft.margin.only(bottom=10),
        )

    def build(self):
        return self.controls


api = API()


def main(page: ft.Page):
    page.title = "😸 Cat Log - A minimalist journal"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.auto_scroll = True
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.CREATE,
        on_click=lambda e: page.open(entry_dialog),
    )

    def theme_changer(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        theme_switcher.icon = (
            ft.icons.DARK_MODE
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.icons.LIGHT_MODE
        )
        page.update()

    theme_switcher = ft.IconButton(ft.icons.DARK_MODE, on_click=theme_changer)

    page.appbar = ft.AppBar(
        title=ft.Text("😸 Cat Log", weight=ft.FontWeight.BOLD, size=25),
        center_title=True,
        elevation=10,
        actions=[theme_switcher],
    )
    page.theme_mode = ft.ThemeMode.LIGHT

    # Layout for displaying records
    records = [Record(info) for info in api.read_all()]

    # If there are no records, show a message
    if len(records) == 0:
        records = [
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "No Log Entries to show now",
                                    style=ft.TextThemeStyle.HEADLINE_LARGE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "Please add one by clicking the button in the bottom right corner of the App",
                                    style=ft.TextThemeStyle.HEADLINE_SMALL,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]

    contents = ft.Column(
        controls=records,
        scroll=ft.ScrollMode.AUTO,
        auto_scroll=True,
    )

    def __close_dialog():
        page.close(entry_dialog)
        page.update()

    # Function to handle the addition of a new entry
    def _on_entry_add(e: ft.ControlEvent):
        message_content = message_input.value
        if message_content.strip():
            new_log = LogInfo(
                date_time=datetime.datetime.now(),
                message=Message(content=message_content),
            )
            api.add(new_log)  # Assuming API has an 'add' method to save the log

            # Refresh the records list with the newly added log
            new_record = Record(new_log)

            # Clear the initial "No Log Entries" message if it's present
            if len(contents.controls) == 1 and isinstance(contents.controls[0], ft.Row):
                contents.controls.clear()

            contents.controls.append(new_record)
            message_input.value = ""  # Clear input
            __close_dialog()
            page.update()

    def _on_entry_cancel(e: ft.ControlEvent):
        __close_dialog()

    # Input form for adding new entry
    message_input = ft.TextField(
        label="Log Message",
        multiline=True,
        autofocus=True,
    )

    entry_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please add Entry"),
        content=message_input,
        actions=[
            ft.TextButton("Add", on_click=_on_entry_add),
            ft.TextButton("Cancel", on_click=_on_entry_cancel),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Add existing records to the page
    page.add(contents)


ft.app(target=main)
