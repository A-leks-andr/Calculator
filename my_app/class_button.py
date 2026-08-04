from dataclasses import field

import flet as ft


@ft.control
class CalcButton(ft.Button):
    width: int = field(default_factory=lambda: 60)
    height: int = field(default_factory=lambda: 60)

    style: ft.ButtonStyle = field(
        default_factory=lambda: ft.ButtonStyle(
            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
            shape=ft.CircleBorder(),
            padding=0,
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
