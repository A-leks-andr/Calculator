# Переменные для удобства
PYTHON = uv run python
FLET = uv run flet
TESTS = uv run pytest tests/

.PHONY: run check format clean

# Запуск калькулятора с автообновлением
run:
	$(FLET) run calc.py -r

# Проверка кода линтером Ruff и исправление импортов
check:
	uv run ruff check . --fix

# Форматирование кода по стандарту Ruff
format:
	uv run ruff format .

# Очистка кэша
clean:
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist .ruff_cache rmdir /s /q .ruff_cache
	@if exist build rmdir /s /q build
	@echo Cache and build folders cleaned successfully!

# Сборка калькулятора в exe.файл
build:
	uv run flet pack calc.py --name "My Calculator" --icon calc.ico


# Тесты
test:
	$(TESTS)

cov:
	uv run pytest --cov=calculator_logic tests/ --cov-report=term-missing