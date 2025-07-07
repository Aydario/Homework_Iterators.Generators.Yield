import os
import logging
from datetime import datetime
import functools


def logger(path):
    """Декоратор логирования вызовов функций."""

    def configure_logging():
        """Настройка логгера."""
        logger_ = logging.getLogger(__name__)  # Создаем новый логгер
        logger_.setLevel(logging.INFO)  # Устанавливаем уровень INFO

        logger_.handlers = []  # Очищаем все предыдущие обработчики

        file_handler = logging.FileHandler(
            path,               # Путь к файлу
            encoding='utf-8',   
            delay=True          # Открывает файл только при первой записи
        )
        file_handler.setFormatter(
            logging.Formatter('● [%(asctime)s] - %(message)s')
        )
        logger_.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('● [%(asctime)s] - %(message)s')
        )
        logger_.addHandler(console_handler)

        return logger_

    # Создаем логгер с именем текущего модуля
    logg = configure_logging()

    def __logger(old_function):
        """Декоратор логирования вызовов функций."""

        # Сохраняем данные оригинальной функции
        @functools.wraps(old_function)
        def new_function(*args, **kwargs):
            # Фиксируем время вызова функции
            call_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Подготавливаем аргументы для логирования:
            # 1. Преобразуем позиционные аргументы в строки
            args_repr = [repr(a) for a in args]
            # 2. Преобразуем именованные аргументы в строки вида key=value
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            # 3. Объединяем все аргументы в одну строку через запятую
            arguments = ', '.join(args_repr + kwargs_repr)
            
            # Логируем факт вызова функции
            if not args and not kwargs:
                logg.info(f'Вызов функции {old_function.__name__} без аргументов')
            else:
                logg.info(f'Вызов функции {old_function.__name__} с аргументами: {arguments}')

            try:
                # Выполняем оригинальную функцию
                result = old_function(*args, **kwargs)

                # Логируем успешный результат выполнения
                logg.info(f'Функция {old_function.__name__} вернула: {repr(result)}\n')

                # Возвращаем результат оригинальной функции
                return result

            except Exception as error:
                # Логируем ошибку, если она произошла
                logg.error(f'Ошибка в {old_function.__name__}: {str(error)}\n', exc_info=True)
                raise

        return new_function
    
    return __logger
    