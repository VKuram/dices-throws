@echo off

echo 🚀 Запускаем приложение...

if not exist "main.py" (
    echo ❌ Файл main.py не найден!
    pause
    exit /b 1
)

start /B python main.py

timeout /t 1 /nobreak >nul

echo Приложение запущено. Открываем браузер...
start "" "http://127.0.0.1:5000/"

echo.
echo Для остановки нажмите Ctrl+C в этом окне.
echo.

pause >nul