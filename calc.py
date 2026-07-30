import flet as ft

from calculator_logic import CalcController
from class_button import ActionButton, DigitButton, ExtraActionButton


@ft.control
class CalculatorApp(ft.Container):
    def init(self):
        self.logic = CalcController(self)

        self.width = 450
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        self.history = ft.Text(value="", color=ft.Colors.GREY_500, size=20)
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=30)

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
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.logic.button_clicked),
                        DigitButton(content="8", on_click=self.logic.button_clicked),
                        DigitButton(content="9", on_click=self.logic.button_clicked),
                        ActionButton(content="*", on_click=self.logic.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.logic.button_clicked),
                        DigitButton(content="5", on_click=self.logic.button_clicked),
                        DigitButton(content="6", on_click=self.logic.button_clicked),
                        ActionButton(content="-", on_click=self.logic.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.logic.button_clicked),
                        DigitButton(content="2", on_click=self.logic.button_clicked),
                        DigitButton(content="3", on_click=self.logic.button_clicked),
                        ActionButton(content="+", on_click=self.logic.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            content="0", expand=2, on_click=self.logic.button_clicked
                        ),
                        DigitButton(content=".", on_click=self.logic.button_clicked),
                        ActionButton(content="=", on_click=self.logic.button_clicked),
                    ]
                ),
            ]
        )


def main(page: ft.Page):
    page.title = "Мой калькулятор"

    # Центрируем калькулятор внутри окна
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.window.width = 500
    page.window.height = 410

    calc = CalculatorApp()
    page.window.resizable = False
    page.add(calc)

    focus_box = ft.TextField(width=0, height=0, opacity=0, autofocus=True)
    page.add(focus_box)

    page.on_keyboard_event = calc.logic.handle_keyboard

    page.update()
    focus_box.focus()


ft.run(main)
