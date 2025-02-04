Интерактивное решение для задачи B
==================================

Для участия в интерактивной части финала SDSJ, команды претендующие на приз жюри должны добавить в свое решение интерфейс (HTTP API), позволяющий получать ответы на вопросы в режиме реального времени. 

### Добавление интерфейса в Python-решение

1. Установите в ваш image python-пакет `flask`, в `sberbank/sdsj-python` он уже установлен.
2. Добавьте [`prediction_server.py`](prediction_server.py), заполните содержимое функции `make_answer(paragraph, question)`.
3. Поменяйте в `metadata.json` поле `entry_point` таким образом, чтобы по запуску контейнера запускался сервер на порту 8000.

```json
{
    "image": "sberbank/sdsj-python",
    "entry_point": "python prediction_server.py"
}
```

### Тестирование решения

Запустите контейнер с решением, прокинув порт 8000 из контейнера:
```bash
$ docker run \
    -p 8000:8000 \
    -v `pwd`:/workspace \
    -w /workspace \
    python prediction_server.py
```

Запустите скрипт `test_requests.py`, который сделает несколько тестовых запросов к решению:
```bash
$ python test_requests.py http://localhost:8000
```

Скрипт требует python-пакет `requests`. Он должен успешно отработать и напечатать параграфы, вопросы, ответы и время выполнения запроса.

### Спецификация интерфейса

Контейнер с решением должен слушать HTTP запросы по порту 8000.

На запрос `GET /health` отвечать кодом 200 с любым содержимым. Это необходимо для регулярной проверки работоспособности решения. В случае, если на запрос `/health` нет ответа, либо ответ будет не 200x, контейнер будет перезапущен.

Основной запрос `POST /predict` содержит в теле JSON c параграфом и вопросом:
```json
{
    "paragraph": "Голоцен (начался 11,7 тыс. лет назад и продолжается до сих пор) — типичная межледниковая...",
    "question": "Какие виды животных перестали существовать за последние несколько сотен лет?"
}
```
На него необходимо дать ответ с вида:
```json
{
    "answer": "дронты, эпиорнис"
}
```
имеющий в заголовке `Content-Type: application/json`.

### Ограничения решения

Контейнеры будут запущены с такими же ограничениями как при автоматическом тестировании:
- 8 Гб оперативной памяти
- 2 vCPU
- размер рабочего каталога — 2 Гб

Запросы `/predict` будут делаться строго в один поток. Время ответа жестко ограничено 10 секундами. Однако, рекомендуется давать ответ не более чем за 2-5 секунд.
