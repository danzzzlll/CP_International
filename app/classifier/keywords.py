# ключевые слова для матчинга обращения с ними для выделения Типа Оборудования и Точек остановки

class KeyWords:
    type_keywords = {
        'Ноутбук': [
            'перегрев', 'зарядка', 'экран', 'батарея', 'клавиатура', 
            'тачпад',  'включаться', 
            'питание',  'вентиляция', 
            'выключение', 'зависание', 'трещина', 'память', 'диск',
            'неисправность', 'подключение', 'замена', 'экранный', 
            'жёсткий',  'планшет',  'выход', 'ноутбук', 'компьютер', 'ПК'
        ],
        'Сервер': [
            'перезагрузка', 'нагрузка', 'доступ', 'сеть', 
            'запуск',  
            'процессор',  'хранилище',  'резервирование',
            'раздел', 'управление', 
            'серверный',  'контроль',
            'конфигурация', 'подключение', 
            'сеть', 'ошибки', 'сервер'
        ],
        'СХД': [
            'диск', 'хранилище', 'данные', 'массив', 'доступ', 
            'раздел', 'резервный', 'копирование', 'перезапись', 
            'контроллер', 'загрузка',
            'модуль', 'ресурс', 'замена', 'объём', 'файл',
            'данные', 'запись', 
            'сохранение', 'восстановление', 'запрос',
            'блокировка', 'порт', 'система'
        ]
    }

    stop_dot_keywords = {
        'Блок питания': ['зарядный', 'питание', 'заряжаться', 'неисправный', 'подключение', 'разъединение', 'перегрев', 'неработающий', 'адаптер', 'провод', 'блок', 'питание'],
        'Материнская плата': ['плата', 'разъем', 'контакт', 'сгореть', 'перестать', 'работать', 'чип', 'сбой', 'система', 'bios', 'замыкание', 'материнский'],
        'Матрица': ['экран', 'дисплей', 'пятно', 'трещина', 'пиксель', 'мерцать', 'разбитый', 'полоса', 'яркость', 'цветопередача', 'темный', 'матрица'],
        'Вентилятор': ['кулер', 'охлаждение', 'перегрев', 'шум', 'чистка', 'пыль', 'неработать', 'вращение', 'засорение', 'нагрев', 'шуметь', 'вентилятор'],
        'Сервер': ['сеть', 'сбой', 'доступ', 'сервер', 'запрос', 'обработка', 'данные', 'перезагрузка', 'недоступный', 'система', 'узел'],
        'Wi-fi модуль': ['wi-fi'],
        'Диск': ['диск'], 
        'Консультация': ['вопрос', 'совет', 'помощь', 'поддержка', 'консультация', 'обращение', 'решение', 'проблема', 'специалист', 'информация', 'рекомендация'],
        'SFP модуль': ['sfp'],
        'Оперативная память': ['память'],
        'Программное обеспечение': ['обеспечение'],
        'Клавиатура': ['клавиша', 'неработать', 'залипание', 'кнопка', 'отклик', 'сломан', 'замена', 'шлейф', 'раскладка', 'неисправность', 'нажатие', 'клавиатура'],
        'Корпус': ['корпус'],
        'Аккумулятор': ['аккумулятор'],
        'Камера': ['камера'],
        'Wi-fi антенна': ['антенна'],
        'Динамики': ['динамик'],
        'Jack': ['jack']
    }
