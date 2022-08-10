from curses import echo
import os
import openai
from torch import true_divide
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys
import random

#Create a file storage for AI presets

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Please enter maximum prompt reply length (In characters; whole positive numbers between 1-4000 only):")
        self.textbox2 = QLineEdit("")
        self.textbox2.setMinimumSize(50, 20)
        self.textbox2.setMaximumSize(50, 20)
        self.textbox2.resize(50,20)
        self.button2 = QtWidgets.QPushButton("Submit")

        layout.addWidget(self.label)
        layout.addWidget(self.textbox2)
        layout.addWidget(self.button2)
        self.setLayout(layout)

        self.button2.clicked.connect(self.updateRLength)

    @QtCore.Slot()
    def updateRLength(self):
      f = open("rLength.txt", "w")
      f.write(f"{self.textbox2.text()}")
      f.close()
      self.close()

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()


        self.hello = "Testing"

        self.button = QtWidgets.QPushButton("Submit")
        self.settingsButton = QtWidgets.QPushButton("Settings")
        self.text = QtWidgets.QLabel("AI Text Here",
                                     alignment=QtCore.Qt.AlignCenter)
        self.title = QtWidgets.QLabel("Prompt:",
                                     alignment=QtCore.Qt.AlignCenter)

        self.textbox = QLineEdit("")
        self.textbox.setMinimumSize(800, 100)
        self.textbox.setMaximumSize(800, 100)
        self.textbox.resize(800,100)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.settingsButton)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
        self.settingsButton.clicked.connect(self.settings)

    @QtCore.Slot()
    def magic(self):
      promptMessage = f"{self.textbox.text()}"
      self.text.setText("Response: " + "\n" + AICall(promptMessage))

    def settings(self):
        self.w = AnotherWindow()
        self.w.show()


app = QtWidgets.QApplication([])

widget = MyWidget()
widget.resize(800, 600)
widget.show()

#Gets the user's basic parameters for text completion/generation.
# promptLength = int(input("How long you would like your response? (In character length; 1-4000) "))
# promptRandomness = float(("0." + input("How random would you like your prompt? (1-10) ")))
# promptMessage = input("Prompt: ")

def AICall(promptMessage):
  #Sets my OpenAI unique key, account reqiured to submit prompts
  openai.api_key = "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"

  f = open("rLength.txt", "r")
  tokenMax = (int(f.read()))
  print(tokenMax)

  #Send the pre-set information to the OpenAI server to return the text completion
  response = openai.Completion.create(
    model="text-davinci-002",
    prompt=promptMessage,
    temperature=0.7,
    max_tokens= tokenMax,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  f.close()

  #This eliminates all the outside information that is given as a response by the OpenAI completion and converts reponse to a string
  response = response["choices"][0]["text"]
  response = str(response)
  return response
sys.exit(app.exec())