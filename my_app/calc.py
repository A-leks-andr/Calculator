import flet as ft
from calculator_logic import CalcController
from class_button import ActionButton, DigitButton, ExtraActionButton


@ft.control
class CalculatorApp(ft.Container):
    def init(self):
        self.logic = CalcController(self)

        self.max_width = 350
        self.width = None
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        self.history = ft.Text(value="", color=ft.Colors.GREY_500, size=18)
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=28)

        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.history], alignment=ft.MainAxisAlignment.END),
                ft.Row(controls=[self.result], alignment=ft.MainAxisAlignment.END),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            content="AC", on_click=self.logic.button_clicked
                        ),
                        ExtraActionButton(
                            content="+/-", on_click=self.logic.button_clicked
                        ),
                        ExtraActionButton(
                            content="%", on_click=self.logic.button_clicked
                        ),
                        ActionButton(content="/", on_click=self.logic.button_clicked),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.logic.button_clicked),
                        DigitButton(content="8", on_click=self.logic.button_clicked),
                        DigitButton(content="9", on_click=self.logic.button_clicked),
                        ActionButton(content="*", on_click=self.logic.button_clicked),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.logic.button_clicked),
                        DigitButton(content="5", on_click=self.logic.button_clicked),
                        DigitButton(content="6", on_click=self.logic.button_clicked),
                        ActionButton(content="-", on_click=self.logic.button_clicked),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.logic.button_clicked),
                        DigitButton(content="2", on_click=self.logic.button_clicked),
                        DigitButton(content="3", on_click=self.logic.button_clicked),
                        ActionButton(content="+", on_click=self.logic.button_clicked),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="0", on_click=self.logic.button_clicked),
                        DigitButton(content=".", on_click=self.logic.button_clicked),
                        ExtraActionButton(
                            content="⌫", on_click=self.logic.button_clicked
                        ),
                        ActionButton(content="=", on_click=self.logic.button_clicked),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


def main(page: ft.Page):
    page.title = "Мой калькулятор"
    page.adaptive = True
    page.scroll = ft.ScrollMode.ADAPTIVE

    if page.platform in (
        ft.PagePlatform.WINDOWS,
        ft.PagePlatform.MACOS,
        ft.PagePlatform.LINUX,
    ):
        page.window.width = 375
        page.window.height = 580
        page.window.resizable = False

    # Центрируем калькулятор внутри окна
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    calc = CalculatorApp()

    safe_area = ft.SafeArea(content=calc, expand=True)
    page.add(safe_area)

    focus_box = ft.TextField(width=0, height=0, opacity=0, autofocus=True)
    page.add(focus_box)

    page.on_keyboard_event = calc.logic.handle_keyboard

    page.update()
    focus_box.focus()


ft.run(main)
