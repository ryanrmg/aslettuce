# main file to run the program


import subprocess
import urllib2
import Leap
import json
from translate import Translator
from GenerateTrainingSet import GenerateTrainingSet


def getLetter():
     # Create a translation object
    translator = Translator()

    gestureListener = GenerateTrainingSet()

    controller = Leap.Controller()

    classificationResult = translator.classify(gestureListener.captureGesture(controller))

    bashCommand = "say \"" + classificationResult + "\""
    #subprocess.Popen(bashCommand, shell = True)
    return classificationResult


if __name__ == "__main__":
    letter = getLetter()
    print letter