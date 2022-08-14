from curses import echo
import os
import openai
from torch import true_divide
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider
import sys
import PySide6
from PySide6 import QtCore
from PyQt6.QtCore import Qt
import random

#Implement use of randomness from file into the info given to the AI for response

#Makes the setting menu using similar methods to main window but does not show it
class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label2 = QLabel("Maximum answer length")
        self.label2.setStyleSheet(
        "font-size: 20px;"
        )
        self.label5 = QLabel("(In characters; whole positive numbers between 1-4000 only):")
        self.textbox2 = QLineEdit("")
        self.textbox2.setMinimumSize(50, 20)
        self.textbox2.setMaximumSize(50, 20)
        self.textbox2.resize(50,20)

        self.button2 = QtWidgets.QPushButton("Submit")
        self.button2.setMinimumSize(50, 20)
        self.button2.setMaximumSize(50, 20)
        self.button2.resize(50, 20)

        self.labelSuccess = QLabel("\n")
        self.labelSuccessMessage = QLabel("\n")

        #Slider to determine randomness, labels are separate
        self.label3 = QLabel("Answer Randomness")
        self.label3.setStyleSheet(
        "font-size: 20px;"
        )
        self.label6 = QLabel("(Lower number = More Logical; Higher Number = More Creative):")
        self.slider = QSlider(PySide6.QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(0,10)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setMinimumSize(300, 20)
        self.slider.setMaximumSize(300, 20)
        self.label4 = QLabel("0       1       2       3      4       5      6       7       8       9      10")
        self.spacing = QLabel("\n\n")


        self.button3 = QtWidgets.QPushButton("Exit")
        self.button3.setMinimumSize(40, 20)
        self.button3.setMaximumSize(40, 20)
        self.button3.resize(40, 20)

        layout.addWidget(self.label2)
        layout.addWidget(self.label5)
        layout.addWidget(self.textbox2)
        layout.addWidget(self.button2)
        layout.addWidget(self.labelSuccess)
        layout.addWidget(self.labelSuccessMessage)
        layout.addWidget(self.label3)
        layout.addWidget(self.label6)
        layout.addWidget(self.slider)
        layout.addWidget(self.label4)
        layout.addWidget(self.spacing)
        layout.addWidget(self.button3)
        self.setWindowTitle("Settings")
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.value_changed)
        self.button2.clicked.connect(self.updateRLength)
        self.button3.clicked.connect(self.settingsClose)

    #Updates the rLength file with the new token length, then closes settings window
    @QtCore.Slot()
    def updateRLength(self):
      f = open("rLength.txt", "w")
      f.write(f"{self.textbox2.text()}")
      f.close()
      self.labelSuccess.setText("Success!")
      self.labelSuccess.setStyleSheet(
        "font-size: 20px;"
        )
      self.labelSuccessMessage.setText("(Please close then reopen settings\n menu to update answer length again)\n")
    
    def value_changed(self, i):
      f = open("randomVal.txt", "w")
      if i == 10 or i == 0:
        f.write(str(i))
      else:
        f.write("0." + str(i))
      f.close()

    def settingsClose(self):
      self.close()

#Makes and orders widgets and parameters for the main window
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        #Sets up the buttons
        self.button = QtWidgets.QPushButton("Submit")
        self.button.setMinimumSize(50, 20)
        self.button.setMaximumSize(50, 20)
        self.button.resize(50, 20)

        self.settingsButton = QtWidgets.QPushButton("Settings")
        self.settingsButton.setMinimumSize(50, 25)
        self.settingsButton.setMaximumSize(50, 25)
        self.settingsButton.resize(50, 30)

        #Set up the text groups
        self.text = QtWidgets.QLabel("",
                                     alignment=QtCore.Qt.AlignCenter)
        self.title = QtWidgets.QLabel("Question:",
                                     alignment=QtCore.Qt.AlignCenter)
        self.title.setStyleSheet(
        "font-size: 20px;"
        )

        #Sets up textbox and defines its dimensions
        self.textbox = QLineEdit("")
        self.textbox.setMinimumSize(400, 60)
        self.textbox.setMaximumSize(400, 60)
        self.textbox.resize(400,80)

        #Adds the widgets in the order they'll appear on the page
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.settingsButton)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.text)
        self.setWindowTitle("AI Student Help")

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
widget.resize(400, 300)
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

#Opens and sets the stylesheet
with open("style.qss", "r") as f:
  _style = f.read()
  app.setStyleSheet(_style)

#Runs the app with the program halting if the app is closed
sys.exit(app.exec())