import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

from RSA_oop import RSA
from md4_oop import MD4

my_RSA = RSA()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        ##drobiazki
        self.document_path = ''
        self.prv_path = ''
        self.pub_path = ''
        
        self.setWindowTitle("Aplikacja RSA")
        self.setGeometry(300, 300, 600, 400)

        # Ustawienie tła na inny kolor
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.WindowText, QColor(240, 240, 240))
        self.setPalette(pal)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Wybierz sekcję:")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Zmiana wyglądu przycisków
        button_style = "QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; }"
        self.generate_keys_button = QPushButton("Generuj klucze")
        self.generate_keys_button.setStyleSheet(button_style)
        self.generate_keys_button.clicked.connect(self.generate_keys_section)
        self.layout.addWidget(self.generate_keys_button)

        self.sign_document_button = QPushButton("Podpisz dokument")
        self.sign_document_button.setStyleSheet(button_style)
        self.sign_document_button.clicked.connect(self.sign_document_section)
        self.layout.addWidget(self.sign_document_button)

        self.verify_signature_button = QPushButton("Weryfikuj podpis")
        self.verify_signature_button.setStyleSheet(button_style)
        self.verify_signature_button.clicked.connect(self.verify_signature_section)
        self.layout.addWidget(self.verify_signature_button)

        self.current_section = "main"  # Track the current section

    def generate_keys_section(self):
        self.clear_layout()

        self.label.setText("Generowanie kluczy:")
        self.layout.addWidget(self.label)

        self.generate_private_key_button = QPushButton("Wygeneruj klucz prywatny")
        self.generate_private_key_button.setStyleSheet("QPushButton { background-color: pink; color: white; border-radius: 5px; }")
        self.generate_private_key_button.clicked.connect(self.generate_private_key)
        self.layout.addWidget(self.generate_private_key_button)

        self.generate_public_key_button = QPushButton("Wygeneruj klucz publiczny")
        self.generate_public_key_button.setStyleSheet("QPushButton { background-color: hotpink; color: white; border-radius: 5px; }")
        self.generate_public_key_button.clicked.connect(self.generate_public_key)
        self.layout.addWidget(self.generate_public_key_button)

        self.back_button = QPushButton("Wróć")
        self.back_button.setStyleSheet("QPushButton { background-color: orchid; color: white; border-radius: 5px; }")
        self.back_button.clicked.connect(self.back_to_main_section)
        self.layout.addWidget(self.back_button)

        self.save_keys_button = QPushButton("Zapisz klucze (private, public)")
        self.save_keys_button.setStyleSheet("QPushButton { background-color: mediumorchid; color: white; border-radius: 5px; }")
        self.save_keys_button.clicked.connect(self.save_keys)
        self.layout.addWidget(self.save_keys_button)

        self.current_section = "generate_keys"  # Set the current section

    def sign_document_section(self):
        self.clear_layout()

        self.label.setText("Podpisywanie dokumentu:")
        self.layout.addWidget(self.label)

        self.select_document_button = QPushButton("Wybierz dokument")
        self.select_document_button.setStyleSheet("QPushButton { background-color: lightskyblue; color: white; border-radius: 5px; }")
        self.select_document_button.clicked.connect(self.select_document)
        self.layout.addWidget(self.select_document_button)
        
        ##
        self.select_prv_button = QPushButton("Zmień klucze (prywatny, publiczny)")
        self.select_prv_button.setStyleSheet("QPushButton { background-color: mediumorchid; color: white; border-radius: 5px; }")
        self.select_prv_button.clicked.connect(self.select_prv)
        self.layout.addWidget(self.select_prv_button)
        ##

        self.sign_button = QPushButton("Podpisz")
        self.sign_button.setStyleSheet("QPushButton { background-color: dodgerblue; color: white; border-radius: 5px; }")
        self.sign_button.clicked.connect(self.sign_document)
        self.layout.addWidget(self.sign_button)

        self.back_button = QPushButton("Wróć")
        self.back_button.setStyleSheet("QPushButton { background-color: deepskyblue; color: white; border-radius: 5px; }")
        self.back_button.clicked.connect(self.back_to_main_section)
        self.layout.addWidget(self.back_button)

        self.current_section = "sign_document"

    def verify_signature_section(self):
        self.clear_layout()

        self.label.setText("Weryfikacja podpisu:")
        self.layout.addWidget(self.label)

        self.select_document_button = QPushButton("Wybierz dokument")
        self.select_document_button.setStyleSheet("QPushButton { background-color: plum; color: white; border-radius: 5px; }")
        self.select_document_button.clicked.connect(self.select_document)
        self.layout.addWidget(self.select_document_button)

        self.verify_button = QPushButton("Weryfikuj")
        self.verify_button.setStyleSheet("QPushButton { background-color: #9C27B0; color: white; border-radius: 5px; }")
        self.verify_button.clicked.connect(self.verify_signature)
        self.layout.addWidget(self.verify_button)

        self.back_button = QPushButton("Wróć")
        self.back_button.setStyleSheet("QPushButton { background-color: mediumorchid; color: white; border-radius: 5px; }")
        self.back_button.clicked.connect(self.back_to_main_section)
        self.layout.addWidget(self.back_button)

        self.current_section = "verify_signature"  # Set the current section

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def back_to_main_section(self):


        self.setWindowTitle("Aplikacja RSA")
        self.setGeometry(300, 300, 600, 400)

        # Ustawienie tła na inny kolor
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.WindowText, QColor(240, 240, 240))
        self.setPalette(pal)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Wybierz sekcję:")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Zmiana wyglądu przycisków
        button_style = "QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; }"
        self.generate_keys_button = QPushButton("Generuj klucze")
        self.generate_keys_button.setStyleSheet(button_style)
        self.generate_keys_button.clicked.connect(self.generate_keys_section)
        self.layout.addWidget(self.generate_keys_button)

        self.sign_document_button = QPushButton("Podpisz dokument")
        self.sign_document_button.setStyleSheet(button_style)
        self.sign_document_button.clicked.connect(self.sign_document_section)
        self.layout.addWidget(self.sign_document_button)

        self.verify_signature_button = QPushButton("Weryfikuj podpis")
        self.verify_signature_button.setStyleSheet(button_style)
        self.verify_signature_button.clicked.connect(self.verify_signature_section)
        self.layout.addWidget(self.verify_signature_button)

        self.current_section = "main"


    def generate_private_key(self):
        private_key, _ = my_RSA.generate_keys()
        QMessageBox.information(self, "Klucz prywatny", private_key)

        # Generowanie pola tekstowego do wyświetlania klucza prywatnego
        self.private_key_text = QLabel(private_key)
        self.private_key_text.setStyleSheet("QLabel { background-color: white; border: 1px solid gray; padding: 5px; }")
        self.layout.addWidget(self.private_key_text)




    def generate_public_key(self):
        _, public_key = my_RSA.generate_keys()
        QMessageBox.information(self, "Klucz publiczny", public_key)

        # Generowanie pola tekstowego do wyświetlania klucza publicznego
        self.public_key_text = QLabel(public_key)
        self.public_key_text.setStyleSheet("QLabel { background-color: white; border: 1px solid gray; padding: 5px; }")
        self.layout.addWidget(self.public_key_text)


    def save_keys(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path_prv, _ = file_dialog.getSaveFileName(
            self, "Zapisz klucz prywatny", "", "Plik tekstowy (*.txt);;Wszystkie pliki (*)"
        )
        file_path_pub, _ = file_dialog.getSaveFileName(
            self, "Zapisz klucz publiczny", "", "Plik tekstowy (*.txt);;Wszystkie pliki (*)"
        )
        if file_path_prv and file_path_pub:
            private_key = self.private_key_text.text()
            public_key = self.public_key_text.text()
            try:
                with open(file_path_prv, "w") as file:
                    file.write(f"{private_key}")
                with open(file_path_pub, "w") as file:
                    file.write(f"{public_key}")
                QtWidgets.QMessageBox.information(self, "Zapis kluczy", "Klucze zostały zapisane")
            except IOError:
                QtWidgets.QMessageBox.critical(self, "Błąd zapisu",
                                               "Wystąpił błąd podczas zapisywania kluczy do pliku.")
        else:
            QtWidgets.QMessageBox.information(self, "Zapis kluczy", "Anulowano zapisywanie kluczy do pliku.")
    
    def select_prv(self):
        file_dialog = QFileDialog()
        prv_path, _ = file_dialog.getOpenFileName(self, "Wybierz klucz prywatny")
        self.prv_path = prv_path
        pub_path, _ = file_dialog.getOpenFileName(self, "Wybierz klucz publiczny")
        self.pub_path = pub_path

    def select_document(self):
        file_dialog = QFileDialog()
        document_path, _ = file_dialog.getOpenFileName(self, "Wybierz dokument")
        self.document_path = document_path

        # Wyświetlanie wybranego dokumentu w QPlainTextEdit
        #with open(document_path, "r") as file:
        #    document_content = file.read()
            #self.document_text_edit.setPlainText(document_content)
        # Tutaj można podjąć dalsze działania z wybranym dokumentem, np. przechować ścieżkę do pliku

    def sign_document(self):
        if not self.document_path:
            QMessageBox.warning(self, "Błąd", "Nie wybrano dokumentu.")
            return

        with open(self.document_path) as file:
            data_str = file.read()

        check_sum = MD4.from_string(data_str).output_hash
        
        if not (self.prv_path and self.pub_path):
            s = my_RSA.generate_sign(check_sum)
            pub_string = f"\n{my_RSA.pub[0]} {my_RSA.pub[1]}"
        else:
            with open(self.prv_path) as file: #przypisuje zawartość pliku do zmiennej
                data = file.read().split('\n')
                if len(data) != 2:
                    QMessageBox.information(self,"Podpis dokumentu", "Klucz ma bląd")
                    return None
                new_prv = data[1]
                try:
                    new_prv = tuple( map(int, new_prv.split() ))
                except ValueError:
                    QMessageBox.information(self,"Podpis dokumentu", "Klucz ma bląd")
                    return None
                
            with open(self.pub_path) as file: #przypisuje zawartość pliku do zmiennej
                data = file.read().split('\n')
                if len(data) != 2:
                    QMessageBox.information(self,"Podpis dokumentu", "Klucz ma bląd")
                    return None
                new_pub = data[1]
                try:
                    new_pub = tuple( map(int, new_pub.split() ))
                except ValueError:
                    QMessageBox.information(self,"Podpis dokumentu", "Klucz ma bląd")
                    return None
                pub_string = f"\n{new_pub[0]} {new_pub[1]}"
            s = my_RSA.generate_sign(check_sum, new_prv)

        # Save the signature to a file or display it in a message box
        save_path, _ = QFileDialog.getSaveFileName(self, "Zapisz podpis", "", "Text Files (*.txt);;All Files (*)")
        if save_path:
            ## Zaszyfrowany skrót i klucz publiczny podpisującego są połączone w podpis cyfrowy
            with open(save_path, 'w') as file:
                file.write(str(s)+pub_string)
            QMessageBox.information(self, "Zapisano podpis", f"Podpis został zapisany w pliku:\n{save_path}")
        else:
            QMessageBox.information(self, "Podpis", f"Podpis dokumentu:\n{s}")

    def verify_signature(self):
        #public_key = my_RSA.pub #pobiera klucz publiczny ze zmiennej
        if not self.document_path:
            QMessageBox.warning(self, "Błąd", "Nie wybrano dokumentu.") #patrzy czy jakis dokument został wybrany
            return

        with open(self.document_path) as file: #przypisanie zawartości dokumentu do zmiennej
            data_str = file.read()
        plik = data_str

        file_dialog = QFileDialog()
        document_path, _ = file_dialog.getOpenFileName(self, "Wybierz podpis") #prosi o podanie pliku z podpisem

        self.document_path = document_path
        if not self.document_path:
            QMessageBox.warning(self, "Błąd", "Nie wybrano dokumentu.") #sprawdza czy plik został wybrany
            return None
        
        #przypisuje zawartość pliku do zmiennej
        with open(self.document_path) as file: #przypisuje zawartość pliku do zmiennej
            data = file.read().split('\n')
            if len(data) != 2:
                QMessageBox.information(self,"Weryfikacja podpisu", "Podpis ma bląd")
                return None
            signature, sign_pub = data
        #tworzy hash zawartości pliku podpisanego
        document_hash = MD4.from_string(plik).output_hash 
        
        if not sign_pub.replace(' ', '').isdigit():
            QMessageBox.information(self,"Weryfikacja podpisu", "Podpis ma bląd")
            return None
        sign_pub = tuple( map(int, sign_pub.split() ))

        if signature.isdigit():
            #dekodowanie na hash podpisu pprzy pomocy klucza publiczneoo
            decrypted_signature = RSA.decrypt(int(signature), sign_pub) 
            if decrypted_signature == document_hash:
                #jesli hashe sa sobie równe to podpis jest prawidłowy
                QMessageBox.information(self,"Weryfikacja podpisu", "Podpis poprawny") 
            else:
                #jesli hashe nie sa sobie równe to nieprawidłowy
                QMessageBox.information(self,"Weryfikacja podpisu", "Podpis niepoprawny") 
        else:
            QMessageBox.information(self,"Weryfikacja podpisu", "Podpis ma niepoprawny typ dannych")



if __name__ == "__main__":
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
