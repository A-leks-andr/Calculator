import flet as ft


class CalcController:
    def __init__(self, app):
        self.app =  app
        self.reset()


    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num


    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)


    def button_clicked(self, e):
        data = e if isinstance(e, str) else e.control.content
        print(f"Button clicked with data = {data}")

        if self.app.result.value == "Error" or data == "AC":
            self.app.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.app.result.value == "0" or self.new_operand:
                self.app.result.value = data
                self.new_operand = False
            else:
                self.app.result.value = self.app.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.app.result.value = str(
                self.calculate(
                    self.operand1, float(self.app.result.value), self.operator
                )
            )
            self.operator = data
            if self.app.result.value == "Error":
                self.operand1 = 0
            else:
                self.operand1 = float(self.app.result.value)
            self.new_operand = True

        elif data in ("="):
            self.app.result.value = str(
                self.calculate(
                    self.operand1, float(self.app.result.value), self.operator
                )
            )
            self.reset()

        elif data in ("%"):
            current_value = float(self.app.result.value)

            if self.operand1 != 0 and self.operator in ("+", "-"):
                val = self.operand1 / 100 * current_value
                res = self.calculate(self.operand1, val, self.operator)
            elif self.operand1 != 0 and self.operator in ("*", "/"):
                if self.operator == "/" and current_value == 0:
                    res = "Error"
                else:
                    val = current_value / 100
                    res = self.calculate(self.operand1, val, self.operator)
            else:
                res = current_value / 100

            if res == "Error":
                self.app.result.value = "Error"
            else:
                self.app.result.value = str(self.format_number(res))
            self.reset()

        elif data in ("+/-"):
            if self.app.result.value == "0":
                return
            res = float(self.app.result.value) * -1
            self.app.result.value = str(self.format_number(res))

            # Обновляем сам визуальный контейнер
        self.app.update()

    def handle_keyboard(self, e: ft.KeyboardEvent):
        key = e.key
        if key in (
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
            ".", "+", "-", "*", "/", "%",
        ):
            self.button_clicked(key)
        elif key in ("Enter", "="):
            self.button_clicked("=")
        elif key in ("Escape", "Delete"):
            self.button_clicked("AC")
        elif key == "Backspace":
            if self.app.result.value != "Error" and len(self.app.result.value) > 1:
                self.app.result.value = self.app.result.value[:-1]
            else:
                self.app.result.value = "0"
            self.app.update()