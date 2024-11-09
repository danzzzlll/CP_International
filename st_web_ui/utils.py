import io
import os
import plotly.graph_objects as go
import plotly.io as pio
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Функция для сохранения графика Plotly как изображение
def save_plot_as_image(fig, filename):
    """
    Сохраняет график Plotly в изображение с заданным именем файла.

    Параметры:
    fig (plotly.graph_objects.Figure): График, который нужно сохранить.
    filename (str): Имя файла, в который будет сохранен график.

    Эта функция использует библиотеку Kaleido для конвертации графика в изображение.
    """
    pio.kaleido.scope.default_width = 800  # Устанавливаем разрешение изображения
    fig.write_image(filename)


# Функция для создания PDF из изображений
def create_pdf(image_files, output_pdf):
    """
    Создает PDF-файл, который содержит изображения, переданные в списке image_files.

    Параметры:
    image_files (list): Список путей к изображениями, которые будут добавлены в PDF.
    output_pdf (str): Путь к выходному PDF файлу (файл не используется в текущей реализации).

    Возвращает:
    buffer: Буфер с содержимым PDF для дальнейшего использования.
    """
    buffer = io.BytesIO()  # Создаем буфер для хранения PDF
    c = canvas.Canvas(buffer, pagesize=letter)  # Создаем объект Canvas для рисования на страницах PDF
    width, height = letter  # Получаем размеры страницы (letter - стандартный размер)

    # Добавляем каждое изображение на новую страницу PDF
    for image_file in image_files:
        c.drawImage(image_file, 0, height-500, width=width, height=400)  # Настройка размера и позиции изображения
        c.showPage()  # Переход к следующей странице

    c.save()  # Сохраняем PDF в буфер
    buffer.seek(0)  # Перемещаем указатель на начало буфера
    return buffer  # Возвращаем буфер с PDF содержимым


# Функция для генерации PDF и его скачивания
def generate_pdf_and_download(plots):
    """
    Генерирует PDF с графиками и возвращает его в виде потока для скачивания.

    Параметры:
    plots (list): Список объектов графиков Plotly, которые нужно преобразовать в изображения и добавить в PDF.

    Возвращает:
    buffer: Буфер с PDF содержимым.
    """
    image_files = []
    # Сохраняем каждый график как изображение и добавляем в список image_files
    for i, fig in enumerate(plots):
        image_filename = f"plot_{i}.png"
        save_plot_as_image(fig, image_filename)
        image_files.append(image_filename)

    # Создаем PDF и возвращаем его как бинарный поток
    pdf_buffer = create_pdf(image_files, "plots.pdf")

    # Очищаем временные изображения
    for image_file in image_files:
        os.remove(image_file)

    return pdf_buffer  # Возвращаем буфер с PDF


def generate_pdf(plots):
    """
    Генерирует PDF с графиками, но не возвращает его для скачивания. PDF сохраняется на диске.

    Параметры:
    plots (list): Список объектов графиков Plotly, которые нужно преобразовать в изображения и добавить в PDF.
    """
    image_files = []
    # Сохраняем каждый график как изображение и добавляем в список image_files
    for i, fig in enumerate(plots):
        image_filename = f"plot_{i}.png"
        save_plot_as_image(fig, image_filename)
        image_files.append(image_filename)

    # Создаем PDF (но не возвращаем его)
    create_pdf(image_files, "plots.pdf")

    # Очищаем временные изображения
    for image_file in image_files:
        os.remove(image_file)
