def test_keyboard_digits_and_ops(controller, fake_keyboard_event):
    """Проверка ввода обычных клавиш"""
    controller.handle_keyboard(fake_keyboard_event("5"))
    assert controller.app.result.value == "5"

    controller.handle_keyboard(fake_keyboard_event("add"))
    assert controller.app.history.value == "5 +"


def test_keyboard_shift_combinations(controller, fake_keyboard_event):
    """Проверка комбинаций со Shift (+ и %)"""
    controller.app.result.value = "200"
    controller.handle_keyboard(fake_keyboard_event("=", shift=True))
    controller.app.result.value = "10"
    controller.handle_keyboard(fake_keyboard_event("5", shift=True))
    assert controller.app.result.value == "220"


def test_keyboard_backspace(controller, fake_keyboard_event):
    """Проверка удаления символов через Backspace"""
    controller.app.result.value = "55"
    controller.handle_keyboard(fake_keyboard_event("backspace"))
    assert controller.app.result.value == "5"


def test_keyboard_clear_and_escape(controller, fake_keyboard_event):
    """Проверка клавиш Escape и Delete для сброса"""
    controller.app.result.value = "55"
    controller.handle_keyboard(fake_keyboard_event("escape"))
    assert controller.app.result.value == "0"

    controller.app.result.value = "99"
    controller.handle_keyboard(fake_keyboard_event("delete"))
    assert controller.app.result.value == "0"


def test_keyboard_backspace_on_zero(controller, fake_keyboard_event):
    """Проверка Backspace, если на экране уже горит 0 или одиночная цифра"""
    controller.app.result.value = "5"
    controller.handle_keyboard(fake_keyboard_event("backspace"))
    assert controller.app.result.value == "0"

    controller.handle_keyboard(fake_keyboard_event("backspace"))
    assert controller.app.result.value == "0"


def test_keyboard_enter(controller, fake_keyboard_event):
    """Проверка клавиши Enter как аналога знака Равно"""
    controller.handle_keyboard(fake_keyboard_event("1"))
    controller.handle_keyboard(fake_keyboard_event("0"))
    controller.handle_keyboard(fake_keyboard_event("+"))
    controller.handle_keyboard(fake_keyboard_event("5"))
    controller.handle_keyboard(fake_keyboard_event("enter"))
    assert controller.app.result.value == "15"
