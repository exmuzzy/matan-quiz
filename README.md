# Matan Topics & Python Quiz

Веб-приложение для изучения математического анализа + опросник по Python для 9 класса.

## Компоненты

### Matan Topics (`/matan_topics/`)
Интерактивный список из 419 тем матанализа (матшкола и 1–2 курс) с:
- Чекбоксами для отслеживания изученных тем
- Кнопкой теории (▸) — показывает до 6 абзацев теории по каждой теме в правой панели
- Lazy-loading теории — подгружается при клике, кэшируется
- Сохранением прогресса на сервере

**Разделы:** Множества (35), Последовательности (15), Непрерывность (15), Производные (30), Интегралы (45), Ряды (45), Функции нескольких переменных (30), Кратные интегралы (45), Комплексный анализ (15), Метрические пространства (15), Специальные функции (30), Комбинаторика (35), Теория графов (49), ОДУ (15).

### Python Quiz (`/quiz/`)
Опросник по Python для учеников 9 класса: типы данных, строки, условия, циклы, списки, функции и т.д.

## Стек

- **Backend:** Python 3, Flask
- **Frontend:** Vanilla HTML/CSS/JS (dark theme)
- **Storage:** JSON-файлы на диске
- **Web Server:** Nginx (reverse proxy + static files)

## Установка

```bash
# Зависимости
pip3 install flask

# Запуск
python3 python_quiz.py
# Слушает на 127.0.0.1:5001

# Или через systemd
sudo cp deploy/python-quiz.service /etc/systemd/system/
sudo systemctl enable python-quiz
sudo systemctl start python-quiz
```

## Структура

```
├── python_quiz.py           # Flask-приложение (API + Quiz)
├── matan-topics/
│   └── index.html           # Фронтенд matan topics
├── data/
│   └── theory.json          # Теория по всем 419 темам
├── deploy/
│   ├── nginx.conf           # Конфигурация Nginx
│   └── python-quiz.service  # Systemd unit
└── README.md
```

## API

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/matan_topics/` | GET | Фронтенд (static HTML) |
| `/matan_topics/load?name=X` | GET | Загрузить прогресс пользователя |
| `/matan_topics/save` | POST | Сохранить прогресс |
| `/matan_topics/theory?idx=N` | GET | Получить теорию по теме (до 5 абзацев) |

## Данные теории

Файл `data/theory.json` — словарь `{"0": ["абзац1", ...], "1": [...], ...}`.
Ключ — индекс темы (0-418), значение — массив абзацев (до 6).

Для обновления: отредактируйте `data/theory.json` и перезапустите сервис.
