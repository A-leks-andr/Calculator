import pytest

from calculator_logic import CalcController


class MockApp:
    def __init__(self):
        class MockField:
            def __init__(self, default_value=""):
                self.value = default_value

        self.result = MockField("0")
        self.history = MockField("")

    def update(self):
        pass


class FakeEvent:
    def __init__(self, content):
        class MockControl:
            def __init__(self, c):
                self.content = c

        self.control = MockControl(content)


class FakeKeyboardEvent:
    def __init__(self, key, shift=False):
        self.key = key
        self.shift = shift


@pytest.fixture
def controller():
    app = MockApp()
    return CalcController(app)


# Регистрируем наши вспомогательные классы в глобальном пространстве pytest,
# чтобы использовать их в других файлах как фикстуры-фабрики
@pytest.fixture
def fake_event():
    return FakeEvent


@pytest.fixture
def fake_keyboard_event():
    return FakeKeyboardEvent
