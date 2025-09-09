#!/bin/bash

if [ ! -f "main.py" ]; then
    echo "❌ Файл main.py не найден!"
    exit 1
fi

python main.py &

APP_PID=$!

echo "Ожидание запуска сервера...
"
sleep 1

if kill -0 $APP_PID 2>/dev/null; then
    echo "Приложение запущено. Открываем браузер...
"
    xdg-open http://127.0.0.1:5000/ 2>/dev/null || \
    open http://127.0.0.1:5000/ 2>/dev/null || \
    echo "⚠️  Не удалось автоматически открыть браузер. Откройте вручную: http://127.0.0.1:5000/"
else
    echo "❌ Приложение не запустилось."
    exit 1
fi

wait $APP_PID 2>/dev/null