# Переменные для удобства
PYTHON = uv run python
FLET = uv run flet
TESTS = uv run pytest tests/

.PHONY: run check format clean test build cov

ifeq ($(OS),Windows_NT)
	RM_CMD = @if exist $(1) rmdir /s /q $(1)
	CLEAN_MSG = @echo Cache and build folders cleaned successfully!
else
	RM_CMD = @rm -rf $(1)
	CLEAN_MSG = @echo "Cache and build folders cleaned successfully!"
endif

# Запуск калькулятора с автообновлением
run:
	$(FLET) run calc.py -r

# Проверка кода линтером Ruff и исправление импортов
check:
	uv run ruff check . --fix

# Форматирование кода по стандарту Ruff
format:
	uv run ruff format .

# Тесты
test:
	$(TESTS)

cov:
	uv run pytest --cov=calculator_logic tests/ --cov-report=term-missing

# Сборка калькулятора в exe.файл
build:
	uv run flet pack calc.py --name "My Calculator" --icon calc.ico

# Очистка кэша
clean:
	$(call RM_CMD,__pycache__)
	$(call RM_CMD,.ruff_cache)
	$(call RM_CMD,build)
	$(CLEAN_MSG)




