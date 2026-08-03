def test_digit_input(controller, fake_event):
    """Проверка последовательного ввода цифр с экрана"""
    controller.button_clicked(fake_event("5"))
    assert controller.app.result.value == "5"

    controller.button_clicked(fake_event("7"))
    assert controller.app.result.value == "57"


def test_double_dot_protection(controller, fake_event):
    """Защита от ввода второй точки в одном числе"""
    controller.button_clicked(fake_event("5"))
    controller.button_clicked(fake_event("."))
    controller.button_clicked(fake_event("5"))
    controller.button_clicked(fake_event("."))
    assert controller.app.result.value == "5.5"


def test_clear_button(controller, fake_event):
    """Проверка кнопки сброса AC"""
    controller.app.result.value = "123"
    controller.app.history.value = "5 + 5"
    controller.button_clicked(fake_event("AC"))
    assert controller.app.result.value == "0"
    assert controller.app.history.value == ""


def test_percent_logic_subtraction(controller, fake_event):
    """Тест процентов при вычитании"""
    controller.app.result.value = "200"
    controller.button_clicked(fake_event("-"))
    controller.app.result.value = "10"
    controller.button_clicked(fake_event("%"))
    assert controller.app.result.value == "180"


def test_sign_change(controller, fake_event):
    """Проверка кнопки +/-"""
    controller.app.result.value = "5"
    controller.button_clicked(fake_event("+/-"))
    assert controller.app.result.value == "-5"


def test_error_handling_on_click(controller, fake_event):
    """Проверяем, что при клике на AC или цифру после ошибки экран очищается"""
    controller.app.result.value = "Error"
    controller.button_clicked(fake_event("5"))
    assert controller.app.result.value == "0"
    controller.button_clicked(fake_event("+"))
    assert controller.app.result.value == "0"


def test_operator_chain_multiple(controller, fake_event):
    """Тест длинной цепочки без кнопки Равно: 5 + 6 + 7 = 18"""
    controller.button_clicked(fake_event("5"))
    controller.button_clicked(fake_event("+"))
    controller.button_clicked(fake_event("6"))
    controller.button_clicked(fake_event("+"))  # Здесь должно посчитаться 11
    assert controller.app.result.value == "11"
    controller.button_clicked(fake_event("7"))
    controller.button_clicked(fake_event("="))
    assert controller.app.result.value == "18"


def test_percent_without_operand(controller, fake_event):
    """Тест нажатия % без предварительного ввода знака: 10% = 0.1"""
    controller.app.result.value = "10"
    controller.button_clicked(fake_event("%"))
    assert controller.app.result.value == "0.1"
    assert controller.app.history.value == "10% = 0.1"


def test_percent_division_by_zero_ui(controller, fake_event):
    """Тест защиты от деления на 0% через интерфейс"""
    controller.button_clicked(fake_event("5"))
    controller.button_clicked(fake_event("/"))
    controller.app.result.value = "0"
    controller.button_clicked(fake_event("%"))
    assert controller.app.result.value == "Error"
