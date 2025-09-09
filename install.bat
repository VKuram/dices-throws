@echo off
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Ошибка при установке зависимостей.
    exit /b 1
) else (
    echo ✅ Зависимости успешно установлены!
)