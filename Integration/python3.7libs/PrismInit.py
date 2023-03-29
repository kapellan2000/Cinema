import os
import sys
#import inspect
def prismInit(prismArgs=[]):
    root = os.getenv("PRISM_ROOT", "")
    print("RRRRRRRRRRr")
    print(root)
    scriptPath = os.path.join(root, "Scripts")
    if scriptPath not in sys.path:
        sys.path.append(scriptPath)
    for i in sys.path:
        print(i)
    import PrismCore
    pcore = PrismCore.PrismCore(app="Cinema", prismArgs=prismArgs)
    return pcore


def createPrismCore():
    print("9999")
    #prismRoot = os.getenv("PRISM_ROOT")

    #py_side_p = prismRoot + "/PythonLibs/Python37/PySide"
    #py_side_p = prismRoot + "/Plugins/Apps/Cinema/Integration/python3.9libs/PySide"
    #sys.path.append(py_side_p)
    py_side_p ="c:/ProgramData/Prism2/plugins/Cinema/Integration/python3.9libs/PySide"
    #py_side_p = prismRoot + "/PythonLibs/Python39/PySide"
    sys.path.append(py_side_p)
    global pcore

    pcore = prismInit()

    

