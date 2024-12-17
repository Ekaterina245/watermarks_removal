import cv2
import numpy as np
from pdf2image import convert_from_path
import os
from PIL import Image
from reportlab.pdfgen import canvas
from sys import argv
from sys import exit
from shutil import rmtree

import clean
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QMainWindow

class MyApp(QMainWindow, clean.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        # Настройка интерфейса
        self.initUI()
        self.input_text = ''
        # self.name = 'EVM.pdf'
        # Подключаем кнопку очистки
        self.pushButton.clicked.connect(self.clean)
        self.pushButton_2.clicked.connect(self.delete)

    def initUI(self):
        # Создание QLineEdit
        # Настройка окна
        self.setWindowTitle('Удаление водяных знаков')

        # self.line_edit = QLineEdit(self)
        # self.lineEdit.setGeometry(QtCore.QRect(180, 60, 181, 41))
        # self.lineEdit.setObjectName("lineEdit")
        # self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        # self.plainTextEdit.setGeometry(QtCore.QRect(70, 60, 81, 41))
        # # self.set_button_styles()

    def set_button_styles(self):
        # Применяем стиль для всех кнопок
        button = self.pushButton
        button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border-style: outset;
                border-width: 1px;
                border-color: black;   
                border-radius: 15px; 
                color: black;
            }
            QPushButton:pressed {
                background-color: #b1c3de;  /* Цвет кнопки при нажатии */
            }
            """
        )
    def show_text(self):
        # Получение текста из QLineEdit и отображение его в QMessageBox
        self.input_text = self.lineEdit.text()
        print(self.input_text)
        # QMessageBox.information(self, "Введенный текст", input_text)
        return self.input_text

    def images_to_pdf(self):
        # self.pdf_filename = 'output.pdf'
        # self.pdf_filename = ['output_page_1.jpg', 'output_page_2.jpg', 'output_page_3.jpg', 'output_page_4.jpg', 'output_page_5.jpg',
        #  'output_page_6.jpg']
        print('Имя файла - ', self.pdf_filename)
        # Создание PDF файла
        c = canvas.Canvas(self.pdf_filename)
        print('Список фоток - ', self.image_list)
        for image in self.image_list:
            # Открытие изображения
            print('test/' + image)
            img = Image.open(image)
            width, height = img.size
            print(width, height, img)

            # Установка размера страницы PDF в размер изображения
            c.setPageSize((width, height))

            # Добавление изображения на страницу
            c.drawImage(image, 0, 0, width=width, height=height)

            # Переход на следующую страницу
            c.showPage()

        c.save()

    def clean(self):
        text = self.show_text()
        print(text, type(text))
        # Путь до pdf файла
        try:
            pages = convert_from_path(text, 300)  # 300 - разрешение в DPI

            # Проходимся циклом по всем страницам и сохраняем их как .jpg
            for i, page in enumerate(pages):
                path_val = 'pdf'
                os.makedirs(path_val, exist_ok=True)
                page.save(f'pdf/output_page_{i + 1}.jpg', 'JPEG')

            # Параметры яркости и контрастности
            alpha = 2.7
            beta = -154
            files = os.listdir('pdf')
            self.image_list = []

            # Цикл для очистки фоток от водяных знаков
            for file in files:
                self.image_list.append(file)
                img = cv2.imread(f"pdf/{file}")

                new = alpha * img + beta
                new = np.clip(new, 0, 255).astype(np.uint8)
                # Сохраняем фотку
                path_val = 'test'
                os.makedirs(path_val, exist_ok=True)
                cv2.imwrite(f"test/{file}", new)
                cv2.imwrite(f"{file}", new)

            print(type(self.image_list), self.image_list)
            # Список изображений для конвертации
            # images = ['image1.jpg', 'image2.jpg', 'image3.jpg']  # Замените на ваши файлы изображений
            self.pdf_filename = 'output.pdf'
        except Exception as e:
            print('Ошибка в при преобразовании pdf в jpg и очистке')
            print(f'ex: {e}')
        try:
            self.images_to_pdf()
        except Exception as e:
            print('Ошибка в создании pdf')

    def delete(self):
        names = ['pdf', 'test']
        print(names)
        for path in names:
            os.makedirs(path, exist_ok=True)
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        rmtree(file_path)
                except Exception as e:
                    print(f'Не удалось удалить {file_path}')

        # Получаем путь к директории, где находится текущий скрипт
        current_directory = os.getcwd()
        start = 'output_page'

        # Получаем список файлов, начинающихся с заданного префикса
        filtered_files = [f for f in os.listdir(current_directory) if f.startswith(start)]
        print(filtered_files)

        # Удаляем файлы, начинающиеся с заданного префикса
        for f in os.listdir(current_directory):
            if f.startswith(start):
                file_path = os.path.join(current_directory, f)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        rmtree(file_path)
                except Exception as e:
                    print(f'Ошибка при удалении файла {file_path}: {e}')
    # Функция завершающая работу приложения
    def closeEvent(self, event):
        event.accept()

def main():
    app = QApplication(argv)  # Новый экземпляр QApplication
    window = MyApp()  # Создаём объект класса MyApp
    window.show()  # Показываем окно
    # Запускает бесконечный цикл
    exit(app.exec_())

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()







