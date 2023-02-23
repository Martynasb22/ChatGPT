import sys
import openai
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QTextEdit)


class ChatGPT(QWidget):
    def __init__(self):
        super().__init__()

        # Nustatome OpenAI API rakto reikšmę
        openai.api_key = "TAVO API RAKTAS"

        # Sukuriame GUI elementus
        self.label_input = QLabel("Įveskite savo klausimą:")
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.send_request)  # Reaguojame į Enter klavišo paspaudimą
        self.label_output = QLabel("ChatGPT atsakymas:")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.btn_send = QPushButton("Siųsti")
        self.btn_send.clicked.connect(self.send_request)
        self.btn_exit = QPushButton("Išeiti")
        self.btn_exit.clicked.connect(QApplication.instance().quit)

        # Sudedame GUI elementus į tėvinį langą
        vbox = QVBoxLayout()
        hbox_input = QHBoxLayout()
        hbox_output = QHBoxLayout()
        hbox_buttons = QHBoxLayout()
        hbox_input.addWidget(self.label_input)
        hbox_input.addWidget(self.input)
        hbox_output.addWidget(self.label_output)
        hbox_output.addWidget(self.output)
        hbox_buttons.addWidget(self.btn_send)
        hbox_buttons.addWidget(self.btn_exit)
        vbox.addLayout(hbox_input)
        vbox.addLayout(hbox_output)
        vbox.addLayout(hbox_buttons)
        self.setLayout(vbox)

        # Nustatome langą
        self.setWindowTitle("ChatGPT by Martynas")
        self.setFixedSize(600, 500)
        
        self.show()

    def send_request(self):
        # Siunčiame klausimą į OpenAI API ir gauname atsakymą
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self.input.text(),
            temperature=0.7,
            max_tokens=2048,
            n=1,
            stop=None,
            stream=True  # gaunamas atsakymas dalimis gyvai
        )

        # Atspausdiname atsakymą GUI lange ir į konsolę
        text = ""
        for chunk in response:
            text += chunk.choices[0].text
            if chunk.choices[0].text.endswith(".") or chunk.choices[0].text.endswith("?") or chunk.choices[
                0].text.endswith("!"):
                self.output.append(text.strip())
                print(text.strip(), flush=True)
                text = ""

        # Išvalome įvedimo lauką
        self.input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_gpt = ChatGPT()
    sys.exit(app.exec_())