def test_basic_math(controller):
    """Проверка базовых математических операций"""
    assert controller.calculate(2, 3, "+") == 5
    assert controller.calculate(10, 4, "-") == 6
    assert controller.calculate(3, 4, "✕") == 12
    assert controller.calculate(10, 2, "/") == 5
    assert controller.calculate(5, 0, "/") == "Error"


def test_format_number(controller):
    """Проверка отсечения некрасивых .0 у целых чисел"""
    assert controller.format_number(5.0) == 5
    assert controller.format_number(5.5) == 5.5


def test_backspace_logic(controller, fake_event):
    """Проверка работы кнопки удаления символа ⌫ на экране калькулятора"""

    # Сценарий 1: Стираем одну цифру из многозначного числа
    controller.app.result.value = "125"
    # Передаем символ ⌫ через вашу встроенную фабрику fake_event
    controller.button_clicked(fake_event("⌫"))
    assert controller.app.result.value == "12"
    assert controller.app.history.value == "12"

    # Сценарий 2: Стираем последнюю цифру (должен вернуться "0")
    controller.app.result.value = "7"
    controller.button_clicked(fake_event("⌫"))
    assert controller.app.result.value == "0"
    assert controller.app.history.value == "0"

    # Сценарий 3: Нажатие Backspace, если на экране уже горит "0" или "Ошибка"
    controller.app.result.value = "0"
    controller.button_clicked(fake_event("⌫"))
    assert controller.app.result.value == "0"

    controller.app.result.value = "Error"
    controller.button_clicked(fake_event("⌫"))
    assert controller.app.result.value == "0"


def test_backspace_is_blocked_after_operator(controller, fake_event):
    """Проверка, что кнопка Backspace полностью блокируется, если нажать её
    сразу после знака операции"""

    controller.operand1 = 50.0
    controller.operator = "+"
    controller.app.history.value = "50 +"
    controller.app.result.value = "50"
    controller.new_operand = True

    # Пользователь пытается нажать Backspace (⌫)
    controller.button_clicked(fake_event("⌫"))

    assert controller.app.result.value == "50"
    assert controller.app.history.value == "50 +"
    assert controller.operator == "+"


def test_backspace_after_equals_behavior(controller, fake_event):
    """Проверка пошагового стирания результата после нажатия знака '='"""

    # --- СЦЕНАРИЙ 1: Стираем одну цифру из многозначного результата (Ветка else) ---
    # Имитируем состояние, когда пользователь посчитал пример (5 + 6 = 11)
    controller.app.history.value = "5 + 6 = 11"
    controller.app.result.value = "11"
    controller.operand1 = 0
    controller.operator = ""
    controller.new_operand = True

    # Пользователь нажимает Backspace (⌫) в первый раз
    controller.button_clicked(fake_event("⌫"))

    # Проверяем, что сработал блок else:
    assert controller.app.result.value == "1"  # От 11 осталась только единица
    assert (
        controller.app.history.value == "1"
    )  # Остаток результата продублирован в историю

    # --- СЦЕНАРИЙ 2: Стираем последнюю цифру до нуля (Ветка if) ---
    controller.app.history.value = "5 + 3 = 8"
    controller.app.result.value = "8"
    controller.operand1 = 0
    controller.operator = ""
    controller.new_operand = True

    controller.button_clicked(fake_event("⌫"))

    # Проверяем, что сработал блок if not/== "0":
    assert controller.app.result.value == "0"
    assert controller.app.history.value == ""


def test_result_becomes_new_operand_after_backspace(controller, fake_event):
    """Проверка универсального сценария: стирание результата до нуля,
    ввод нового дробного числа .25 и последующее сложение + 10 ="""

    # 1. Имитируем завершённое вычисление (например, 30 + 33 = 63)
    controller.app.history.value = "30 + 33 = 63"
    controller.app.result.value = "63"
    controller.operand1 = 0
    controller.operator = ""
    controller.new_operand = True

    # 2. Пользователь нажимает Backspace в первый раз (63 -> 6)
    controller.button_clicked(fake_event("⌫"))
    assert controller.app.result.value == "6"
    assert controller.app.history.value == "6"

    # 3. Пользователь нажимает Backspace во второй раз (6 -> 0)
    controller.button_clicked(fake_event("⌫"))
    assert controller.app.result.value == "0"
    assert controller.app.history.value == "0"

    # 4. Пользователь вводит точку "." (0 -> 0.)
    controller.button_clicked(fake_event("."))
    assert controller.app.result.value == "0."
    assert controller.app.history.value == "0."

    # 5. Пользователь вводит "2" и "5" (0. -> 0.25)
    controller.button_clicked(fake_event("2"))
    controller.button_clicked(fake_event("5"))
    assert controller.app.result.value == "0.25"
    assert controller.app.history.value == "0.25"

    # 6. Пользователь нажимает "+" (Готовимся прибавить 10)
    controller.button_clicked(fake_event("+"))
    assert controller.app.result.value == "0.25"
    assert controller.app.history.value == "0.25 +"
    assert controller.operand1 == 0.25
    assert controller.operator == "+"

    # 7. Пользователь вводит "1" и "0" (0.25 + 10)
    controller.button_clicked(fake_event("1"))
    controller.button_clicked(fake_event("0"))
    assert controller.app.result.value == "10"
    assert controller.app.history.value == "0.25 + 10"

    # 8. Финал: нажимаем "=" и получаем 10.25!
    controller.button_clicked(fake_event("="))
    assert controller.app.result.value == "10.25"
    assert controller.app.history.value == "0.25 + 10 = 10.25"
