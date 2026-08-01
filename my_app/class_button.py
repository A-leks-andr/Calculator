from dataclasses import field

import flet as ft


@ft.control
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)
    style: ft.ButtonStyle = field(
        default_factory=lambda: ft.ButtonStyle(
            text_style=ft.TextStyle(size=22, weight=ft.FontWeight.BOLD),
        )
    )


@ft.control
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.ORANGE
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ExtraActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK
