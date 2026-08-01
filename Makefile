# Переменные для удобства
PYTHON = uv run python
FLET = uv run flet
TESTS = uv run pytest tests/
export FLET_FLUTTER_SDK_ROOT = C:\flet_cache\flutter
export PUB_CACHE = C:\flet_cache\pub
export ANDROID_HOME =

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
	$(FLET) run my_app/calc.py -r

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
	uv run pytest --cov=my_app tests/ --cov-report=term-missing --cov-report=xml

# Сборка калькулятора в exe.файл
build:
	uv run flet pack my_app/calc.py --name "My Calculator" --icon calc.ico

build-android:
	uv run flet build apk my_app --project "My Calculator" --product "Calculator" --module-name calc

build-ios:
	uv run flet build ios --project "My Calculator" --product "Calculator"

# Очистка кэша
clean:
	$(call RM_CMD,__pycache__)
	$(call RM_CMD,.ruff_cache)
	$(call RM_CMD,build)
	$(CLEAN_MSG)




