import flet as ft


class CalcController:
    def __init__(self, app):
        self.app = app
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
        data = e.control.content
        print(f"Button clicked with data = {data}")

        if self.app.result.value == "Error" or data == "AC":
            self.app.result.value = "0"
            self.app.history.value = ""
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            # защита от добавления второй точки в число
            if data == "." and "." in self.app.result.value and not self.new_operand:
                return
            if self.app.result.value == "0" or self.new_operand:
                self.app.result.value = data
                self.new_operand = False
            else:
                self.app.result.value = self.app.result.value + data

            # формирование history
            if self.operand1 == 0:
                self.app.history.value = self.app.result.value
            else:
                self.app.history.value = (
                    f"{self.format_number(self.operand1)} "
                    f"{self.operator} "
                    f"{self.app.result.value}"
                )

        elif data in ("+", "-", "*", "/"):
            res = self.calculate(
                self.operand1, float(self.app.result.value), self.operator
            )
            self.app.result.value = str(res)
            self.operator = data

            if self.app.result.value == "Error":
                self.operand1 = 0
                self.app.history.value = ""
            else:
                self.operand1 = float(self.app.result.value)
                self.app.history.value = (
                    f"{self.format_number(self.operand1)} {self.operator}"
                )
            self.new_operand = True

        elif data in ("="):
            # Защита от нажатия знака = до ввода второго числа
            if self.new_operand:
                return

            val1 = self.format_number(self.operand1)
            val2 = self.app.result.value
            op = self.operator

            res = self.calculate(
                self.operand1, float(self.app.result.value), self.operator
            )
            self.app.result.value = str(res)

            if self.app.result.value != "Error":
                self.app.history.value = f"{val1} {op} {val2} = {self.app.result.value}"

            else:
                self.app.history.value = ""

            self.reset()

        elif data in ("%"):
            current_value = float(self.app.result.value)

            # запоминаем данные для history
            val1 = self.format_number(self.operand1)
            val2 = self.format_number(current_value)
            op = self.operator

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
                self.app.history.value = ""
            else:
                self.app.result.value = str(self.format_number(res))

                # формируем history
                if self.operand1 != 0 and op in ("+", "-", "*", "/"):
                    self.app.history.value = (
                        f"{val1} {op} {val2}% = {self.app.result.value}"
                    )

                else:
                    # Если операции не было (просто ввели 10 и нажали %),
                    # выводим: 10% = 0.1
                    self.app.history.value = f"{val2}% = {self.app.result.value}"
            self.reset()

        elif data in ("+/-"):
            if self.app.result.value == "0":
                return
            res = float(self.app.result.value) * -1
            self.app.result.value = str(self.format_number(res))

            if self.operand1 == 0:
                self.app.history.value = self.app.result.value

            else:
                self.app.history.value = (
                    f"{self.format_number(self.operand1)} "
                    f"{self.operator} {self.app.result.value}"
                )

            # Обновляем сам визуальный контейнер
        self.app.update()

    def handle_keyboard(self, e: ft.KeyboardEvent):
        key = e.key.lower().replace("numpad ", "")
        # Отладка
        print(f"Физическая клавиша нажата: {key} (Shift: {e.shift})")

        class FakeControl:
            def __init__(self, content):
                self.content = content

        class FakeEvent:
            def __init__(self, content):
                self.control = FakeControl(content)

        if e.shift:
            if key == "5":
                clean_key = "%"
            elif key == "8":
                clean_key = "*"
            elif key == "=":
                clean_key = "+"
            else:
                clean_key = key
            # Отладка
            print(f"Если нажата shift {key} меняем на {clean_key}")

        else:
            translations = {
                "add": "+",
                "subtract": "-",
                "multiply": "*",
                "divide": "/",
                "decimal": ".",
            }
            clean_key = translations.get(key, key)
            # Отладка
            print(f"Замена в словаре {key} на {clean_key}")

        if clean_key in (
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0",
            ".",
            "+",
            "-",
            "*",
            "/",
            "%",
        ):
            self.button_clicked(FakeEvent(clean_key))

        elif clean_key in ("enter", "="):
            self.button_clicked(FakeEvent("="))
        elif key in ("escape", "delete"):
            self.button_clicked(FakeEvent("AC"))
        elif key == "backspace":
            if self.app.result.value != "Error" and len(self.app.result.value) > 1:
                self.app.result.value = self.app.result.value[:-1]
            else:
                self.app.result.value = "0"
            self.app.update()
