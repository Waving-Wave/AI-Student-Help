from curses import echo
import os
import openai
from torch import true_divide
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys
import random

#Update comments

#Makes the setting menu using similar methods to main window but does not show it
class AnotherWindow(QWidget):
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

    #Updates the rLength file with the new token length, then closes settings window
    @QtCore.Slot()
    def updateRLength(self):
      f = open("rLength.txt", "w")
      f.write(f"{self.textbox2.text()}")
      f.close()
      self.close()

#Makes and orders widgets and parameters for the main window
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        #Sets up the buttons and display text
        self.button = QtWidgets.QPushButton("Submit")
        self.settingsButton = QtWidgets.QPushButton("Settings")
        self.text = QtWidgets.QLabel("AI Text Here",
                                     alignment=QtCore.Qt.AlignCenter)
        self.title = QtWidgets.QLabel("Prompt:",
                                     alignment=QtCore.Qt.AlignCenter)

        #Sets up textbox and defines its dimensions
        self.textbox = QLineEdit("")
        self.textbox.setMinimumSize(800, 100)
        self.textbox.setMaximumSize(800, 100)
        self.textbox.resize(800,100)

        #Adds the widgets in the order they'll appear on the page
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.settingsButton)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        #Sets up the link between the buttons and the functions they call
        self.button.clicked.connect(self.magic)
        self.settingsButton.clicked.connect(self.settings)

    #This function uses the submitted prompt and gets a response using the AICall function
    @QtCore.Slot()
    def magic(self):
      promptMessage = f"{self.textbox.text()}"
      self.text.setText("Response: " + "\n" + AICall(promptMessage))

    #Shows the (already defined) settings screen
    def settings(self):
        self.w = AnotherWindow()
        self.w.show()

#Defines the app and sets the main screen to show upon running the app
app = QtWidgets.QApplication([])

widget = MyWidget()
widget.resize(800, 600)
widget.show()

#Called by 'magic' to get the AI response to display
def AICall(promptMessage):
  #Sets my OpenAI unique key, account reqiured to submit prompts
  openai.api_key = "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"

  #Opens the rLength files and reads it, setting the tokenMax to the value
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
  #Closes the opened file
  f.close()

  #This eliminates all the outside information that is given as a response by the OpenAI completion and converts reponse to a string
  response = response["choices"][0]["text"]
  response = str(response)
  return response

#Runs the app with the program halting if the app is closed
sys.exit(app.exec())