from curses import echo
import os
import openai
from torch import true_divide
from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random

#Create a file storage for AI presets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.hello = "Testing"

        self.button = QtWidgets.QPushButton("Submit")
        self.text = QtWidgets.QLabel("AI Text Here",
                                     alignment=QtCore.Qt.AlignCenter)
        self.title = QtWidgets.QLabel("Prompt:",
                                     alignment=QtCore.Qt.AlignCenter)

        self.textbox = QtWidgets.QTextEdit()
        self.textbox.setMinimumSize(800, 100)
        self.textbox.setMaximumSize(800, 100)
        self.textbox.resize(800,100)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
      #ERROR HERE, FIX NOT RECIEVING STRING
      promptMessage = self.textbox.toPlainText
      self.text.setText(AICall(promptMessage))

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

  #Send the pre-set information to the OpenAI server to return the text completion
  response = openai.Completion.create(
    model="text-davinci-002",
    prompt=promptMessage,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  #This eliminates all the outside information that is given as a response by the OpenAI completion
  print(response["choices"][0]["text"])
  return response
sys.exit(app.exec())