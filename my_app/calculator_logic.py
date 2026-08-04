import flet as ft


class CalcController:
    def __init__(self, app):
        self.app = app
        self.reset()

    def reset(self):
        self.operator = ""
        self.operand1 = 0
        self.new_operand = True

    def format_number(self, num):
        if isinstance(num, str):
            return num
        rounded_num = round(num, 12)
        if rounded_num % 1 == 0:
            return int(rounded_num)
        else:
            return rounded_num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "✕":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def button_clicked(self, e):
        data = e.control.content

        # 1. Мгновенный сброс или очистка после ошибки
        if self.app.result.value == "Error" or data == "AC":
            self.app.result.value = "0"
            self.app.history.value = ""
            self.reset()
            return

        # 2. Обработка кнопки Backspace (⌫)
        if data == "⌫":
            # Защиты: сразу после знака действия или
            # если второе число стёрто до "0"
            if (self.operator and self.new_operand) or (
                self.operator and self.app.result.value == "0"
            ):
                return

            # Сценарий: стирание после знака равенства "="
            if "=" in self.app.history.value:
                self.app.result.value = self.app.result.value[:-1]

                if not self.app.result.value or self.app.result.value == "0":
                    self.app.result.value = "0"
                    self.app.history.value = ""
                else:
                    self.app.history.value = self.app.result.value

            elif self.app.result.value in ("Error", "0") or not self.app.result.value:
                self.app.result.value = "0"
                self.app.history.value = ""

            else:
                self.app.result.value = self.app.result.value[:-1]

                if not self.app.result.value:
                    self.app.result.value = "0"

                if self.operator:
                    self.app.history.value = (
                        f"{self.format_number(self.operand1)} "
                        f"{self.operator} {self.app.result.value}"
                    )
                else:
                    self.app.history.value = self.app.result.value

        # 3. Обработка ввода цифр и точки
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            # защита от добавления второй точки в число
            if data == "." and "." in self.app.result.value and not self.new_operand:
                return

            if self.app.result.value == "0" or self.new_operand:
                self.app.result.value = "0." if data == "." else data
                self.new_operand = False
            else:
                self.app.result.value += data

            # Формирование истории
            if self.operator:
                self.app.history.value = (
                    f"{self.format_number(self.operand1)} "
                    f"{self.operator} {self.app.result.value}"
                )

            else:
                self.app.history.value = self.app.result.value

        # 4. Обработка математических знаков
        elif data in ("+", "-", "✕", "/"):
            # Защита от деления нуля
            if self.app.result.value == "0" and data == "/":
                return

            if self.operator:
                res = self.calculate(
                    self.operand1, float(self.app.result.value), self.operator
                )
                self.app.result.value = str(res)

                if self.app.result.value == "Error":
                    self.app.history.value = ""
                    self.reset()
                    return

                else:
                    self.operand1 = float(self.app.result.value)

            else:
                self.operand1 = float(self.app.result.value)

            self.operator = data
            self.app.history.value = (
                f"{self.format_number(self.operand1)} {self.operator}"
            )
            self.new_operand = True

        # 5. Обработка знака равенства (=)
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

        # 6. Обработка процентов (%)
        elif data in ("%"):
            current_value = float(self.app.result.value)
            val1 = self.format_number(self.operand1)
            val2 = self.format_number(current_value)
            op = self.operator

            if self.operand1 != 0 and self.operator in ("+", "-"):
                val = self.operand1 / 100 * current_value
                res = self.calculate(self.operand1, val, self.operator)

            elif self.operand1 != 0 and self.operator in ("✕", "/"):
                if self.operator == "/" and current_value == 0:
                    res = "Error"
                else:
                    res = self.calculate(
                        self.operand1, current_value / 100, self.operator
                    )
            else:
                res = current_value / 100

            if res == "Error":
                self.app.result.value = "Error"
                self.app.history.value = ""
            else:
                self.app.result.value = str(self.format_number(res))

                # формируем history
                if self.operand1 != 0 and op in ("+", "-", "✕", "/"):
                    self.app.history.value = (
                        f"{val1} {op} {val2}% = {self.app.result.value}"
                    )
                else:
                    # Если операции не было (просто ввели 10 и нажали %),
                    # выводим: 10% = 0.1
                    self.app.history.value = f"{val2}% = {self.app.result.value}"
            self.reset()

        # 7. Обработка смены знака (+/-)
        elif data in ("+/-"):
            if self.app.result.value == "0":
                return
            res = float(self.app.result.value) * -1
            self.app.result.value = str(self.format_number(res))
            self.new_operand = False

            if self.operator:
                self.app.history.value = (
                    f"{self.format_number(self.operand1)} "
                    f"{self.operator} {self.app.result.value}"
                )
            else:
                self.app.history.value = self.app.result.value

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
                clean_key = "✕"
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
                "multiply": "✕",
                "divide": "/",
                "decimal": ".",
                "*": "✕",
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
            "✕",
            "/",
            "%",
        ):
            self.button_clicked(FakeEvent(clean_key))

        elif clean_key in ("enter", "="):
            self.button_clicked(FakeEvent("="))
        elif key in ("escape", "delete"):
            self.button_clicked(FakeEvent("AC"))
        elif key == "backspace":
            self.button_clicked(FakeEvent("⌫"))
