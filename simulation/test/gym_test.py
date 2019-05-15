import sys

from enum import Enum
import json
import subprocess
import os
import ast

class SimulationState(Enum):
    CREATE_SCENE = 0
    REMOVE_OBJECT = 1

SimulationControllerState = {
  'simulationID': 0,
  'simulationState': 0,
  'imageWidth': 512,
  'imageHeight': 512,
  'removedObjectIndex': 0
}

def writeControllerAsJSON(controller, filepath):
    controllerJSON = json.dumps(controller, sort_keys=False)
    with open(filepath, 'w') as outfile:
        outfile.write(controllerJSON)

def readInitialStableConfigurationObjectCount(filePath):
    sceneJSONStr = ''
    with open(filePath, 'r') as inFile:
        sceneJSONStr = inFile.read()

    sceneDict = ast.literal_eval(sceneJSONStr)
    return len(sceneDict['objectStates'])


simulation_count = 10

unity_call_str = './what-if-test.app/Contents/MacOS/what-if-test -batchmode'

controller_json_filepath = 'controller.json'
initial_stable_json_path = 'InitialStable.json'

dataBaseFolder = 'Data'


for i in range(simulation_count):
    #Create initial stable configuration
    SimulationControllerState['simulationID'] = i
    SimulationControllerState['simulationState'] = 0

    writeControllerAsJSON(SimulationControllerState, controller_json_filepath)

    p1 = subprocess.Popen([unity_call_str], shell=True, stdout=subprocess.PIPE)
    p1.wait()

    simulationFolder = os.path.join(os.path.join(dataBaseFolder, str(i).zfill(4)), initial_stable_json_path)

    noObjects = readInitialStableConfigurationObjectCount(simulationFolder)
    print(noObjects, " objects are created")

    for j in range(noObjects):
        SimulationControllerState['simulationState'] = 1
        SimulationControllerState['removedObjectIndex'] = j

        writeControllerAsJSON(SimulationControllerState, controller_json_filepath)

        p2 = subprocess.Popen([unity_call_str], shell=True, stdout=subprocess.PIPE)
        p2.wait()





