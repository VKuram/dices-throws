#!/bin/bash

echo "Установка зависимостей из requirements.txt...
"

pyenv virtualenv 3.10.10 dices
pyenv activate dices
pyenv local dices

if ! command -v pip &> /dev/null; then
    echo "
❌ pip не найден. Установите Python и pip."
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "
❌ Файл requirements.txt не найден."
    exit 1
fi

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "
✅ Зависимости успешно установлены!"
else
    echo "
❌ Ошибка при установке зависимостей."
    exit 1
fi