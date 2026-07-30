def test_basic_math(controller):
    """Проверка базовых математических операций"""
    assert controller.calculate(2, 3, "+") == 5
    assert controller.calculate(10, 4, "-") == 6
    assert controller.calculate(3, 4, "*") == 12
    assert controller.calculate(10, 2, "/") == 5
    assert controller.calculate(5, 0, "/") == "Error"


def test_format_number(controller):
    """Проверка отсечения некрасивых .0 у целых чисел"""
    assert controller.format_number(5.0) == 5
    assert controller.format_number(5.5) == 5.5
