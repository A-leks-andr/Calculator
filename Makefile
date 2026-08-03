# Глобальные переменные окружения для сборщика Android
export FLET_FLUTTER_SDK_ROOT = C:\develop\flutter
export ANDROID_HOME = C:\AndroidSDK
export PUB_CACHE = C:\flet_cache\pub
export GRADLE_USER_HOME = C:\flet_cache\gradle
export ANDROID_USER_HOME = C:\flet_cache\android_user

# Переменные для удобства
PYTHON = uv run python
FLET = uv run flet
TESTS = uv run pytest tests/

.PHONY: run check format clean test build build-android cov

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
	uv run pytest --cov=my_app.calculator_logic tests/ --cov-report=term-missing --cov-report=xml

# Сборка калькулятора в exe.файл
build:
	$(FLET) pack my_app/calc.py --name "My Calculator" --icon my_app/calc.ico

build-android:
	$(FLET) build apk my_app --project "My Calculator" --product "Calculator" --module-name calc --output ../build --icon mu_ap/calc.png

build-ios:
	$(FLET) build ios my_app --project "My Calculator" --product "Calculator" --module-name calc

# Определяем ОС для команды очистки
ifeq ($(OS),Windows_NT)
    RM_CMD = @if exist $(1) rmdir /s /q $(1)
    CLEAN_MSG = @echo Cache and folders cleaned successfully!
else
    RM_CMD = @rm -rf $(1)
    CLEAN_MSG = @echo "Cache and folders cleaned successfully!"
endif

# Очистка кэша
clean:
	$(call RM_CMD,__pycache__)
	$(call RM_CMD,.ruff_cache)
	$(CLEAN_MSG)




