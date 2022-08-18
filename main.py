from curses import echo
import os
from tracemalloc import start
import openai
from torch import true_divide
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider, QTextEdit
import sys
import PySide6
from PySide6 import QtCore
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal
import time

global startTime
global timeLimit
timeLimit = 100000000000000000000000.0
startTime = time.time()


#Make a second python file to run the timer seperate from this file? If not, timer may need to be scrapped


#Makes a worker thread to make a subprocess processing separte from the main file to prevent freeze when
#using the timer (to prevent copying)
class Worker(QObject):
    finished = pyqtSignal()

    def run(self):
        for i in range(30):
            time.sleep(1)
            print(i)
        self.finished.emit()

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

        #These labels are blank now but act as spacing until the button is pressed,
        #after that they change to a success message
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
        
        #Opens the file to get the random value, it's set to 0 by default, the sets the slider to the last num given
        f = open("randomVal.txt", "r")
        randomnessVal = (float(f.read()))
        if randomnessVal == 0 or randomnessVal == 10:
          randomnessVal = int(randomnessVal)
        else:
          randomnessVal = str(randomnessVal)
          randomnessVal = randomnessVal[2]
          randomnessVal = int(randomnessVal)
        f.close()

        self.slider.setValue(randomnessVal)
        self.slider.setTickInterval(1)
        self.slider.setMinimumSize(300, 20)
        self.slider.setMaximumSize(300, 20)
        self.label4 = QLabel("0       1       2       3      4       5      6       7       8       9      10")
        #Spacing labels are used to introduce space between widgets,
        #this limits use of anchoring which makes the program less flexible
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
        self.spacing2 = QLabel("\n\n AI Answer:", alignment=QtCore.Qt.AlignCenter)
        self.text = QTextEdit("", alignment=QtCore.Qt.AlignCenter)
        self.text.setReadOnly(True)
        self.text.setMaximumWidth(415)

        self.title = QLabel("Question:", alignment=QtCore.Qt.AlignCenter)
        self.title.setStyleSheet(
        "font-size: 20px;"
        )
        self.title.setMaximumWidth(415)

        #Sets up textbox and defines its dimensions
        self.textbox = QLineEdit("")
        self.textbox.setMinimumSize(400, 30)
        self.textbox.setMaximumSize(400, 30)
        self.textbox.resize(400,80)

        #Adds the widgets in the order they'll appear on the page, along with other parameters around the window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setMinimumWidth(425)
        self.setMaximumWidth(425)
        self.layout.addWidget(self.settingsButton)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.spacing2)
        self.layout.addWidget(self.text)
        self.setWindowTitle("AI Student Help")

        #Sets up the link between the buttons and the functions they call
        self.button.clicked.connect(self.magic)
        self.settingsButton.clicked.connect(self.settings)


    #This function uses the submitted prompt and gets a response using the AICall function
    @QtCore.Slot()
    def magic(self):
      promptMessage = f"{self.textbox.text()}"
      self.text.setText(AICall(promptMessage))
      #Create a QThread object
      self.thread = QThread()
      #Create a worker object
      self.worker = Worker()
      #Move worker to the thread
      self.worker.moveToThread(self.thread)
      #Connect signals and slots
      self.thread.started.connect(self.worker.run)
      self.worker.finished.connect(self.thread.quit)
      self.worker.finished.connect(self.worker.deleteLater)
      self.thread.finished.connect(self.thread.deleteLater)
      #Start the thread
      self.thread.start()

      #Resets
      self.button.setEnabled(False)
      self.thread.finished.connect(
          lambda: self.button.setEnabled(True)
      )
      self.thread.finished.connect(
          lambda: self.text.setText("")
      )

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

  #Opens the rLength and randomVal files and reads it, setting the variables to the value
  f = open("rLength.txt", "r")
  tokenMax = (int(f.read()))
  f.close()

  f = open("randomVal.txt", "r")
  randomnessVal = (float(f.read()))
  if randomnessVal == 10.0:
    randomnessVal = 1.0
  f.close()
  

  #Send the pre-set information to the OpenAI server to return the text completion
  # response = openai.Completion.create(
  #   model="text-davinci-002",
  #   prompt = promptMessage,
  #   temperature = randomnessVal,
  #   max_tokens = tokenMax,
  #   top_p=1,
  #   frequency_penalty=0,
  #   presence_penalty=0
  # )

  #This eliminates all the outside information that is given as a response by the OpenAI completion and converts reponse to a string
  # response = response["choices"][0]["text"]
  # response = str(response)
  response = "testing"
  return response

#Opens and sets the stylesheet
with open("style.qss", "r") as f:
  _style = f.read()
  app.setStyleSheet(_style)

#Runs the app with the program halting if the app is closed
sys.exit(app.exec())