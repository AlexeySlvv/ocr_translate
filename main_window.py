from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QTextEdit,
    QGridLayout,
    QFileDialog,
    QComboBox,
    QMessageBox,
)

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap

from ocr_translate import available_langs, translate_text, argos_packages


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # image
        self.sauce_btn = QPushButton("Open image")
        self.sauce_btn.clicked.connect(self.on_sauce_open_clicked)
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.on_start_clicked)

        self.sauce_ledit = QLineEdit()
        self.sauce_ledit.setReadOnly(True)

        self.ocr_lang_cbox = QComboBox()
        self.ocr_lang_cbox.addItems(sorted(available_langs))
        self.tr_from_cbox = QComboBox()
        self.tr_to_cbox = QComboBox()
        self.tr_from_cbox.addItems(sorted(list(set(p["from_code"] for p in argos_packages()))))
        self.tr_to_cbox.addItems(sorted(list(set(p["to_code"] for p in argos_packages()))))

        self.ocr_text_tedit = QTextEdit()
        self.tr_text_tedit = QTextEdit()
        self.image_lbl = QLabel()

        layout = QGridLayout()

        layout.addWidget(self.sauce_btn, 0, 0)
        layout.addWidget(self.sauce_ledit, 0, 1, 1, 2)
        layout.addWidget(self.ocr_lang_cbox, 0, 3)
        layout.addWidget(self.tr_from_cbox, 0, 4, 1, 1)
        layout.addWidget(self.tr_to_cbox, 0, 6, 1, 1)

        layout.addWidget(self.image_lbl, 1, 0, 2, 4)
        layout.addWidget(self.ocr_text_tedit, 1, 4, 2, 2)
        layout.addWidget(self.tr_text_tedit, 1, 6, 2, 2)

        layout.addWidget(self.start_btn, 3, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def on_sauce_open_clicked(self):
        filter = "Images (*.jpg *.jpeg *.png *.bmp)"
        file_name, _ = QFileDialog.getOpenFileName(filter=filter)
        self.sauce_ledit.setText(file_name)
        self.image_lbl.setPixmap(QPixmap(file_name))

    def on_start_clicked(self):
        self.setCursor(Qt.CursorShape.BusyCursor)

        filename = self.sauce_ledit.text()
        ocr_text = self.ocr_lang_cbox.currentText()
        tr_from = self.tr_from_cbox.currentText()
        tr_to = self.tr_to_cbox.currentText()
        
        ocr_text, tr_text = translate_text(filename, ocr_text, tr_from, tr_to)

        self.ocr_text_tedit.setText(ocr_text)
        self.tr_text_tedit.setText(tr_text)

        self.setCursor(Qt.CursorShape.ArrowCursor)

        QMessageBox.information(self, "Ocr", "Done!")
