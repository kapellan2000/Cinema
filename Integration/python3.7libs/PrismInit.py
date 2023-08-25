import os
import sys
def prismInit(prismArgs=[]):
    root = os.getenv("PRISM_ROOT", "")
    scriptPath = os.path.join(root, "Scripts")
    if scriptPath not in sys.path:
        sys.path.append(scriptPath)
    import PrismCore
    pcore = PrismCore.PrismCore(app="Cinema", prismArgs=prismArgs)
    return pcore

def createPrismCore():
    prismRoot = os.getenv("PRISM_ROOT")
    py_side_p = os.path.join(prismRoot, "PythonLibs","Python3","PySide")
    sys.path.append(py_side_p)
    global pcore

    pcore = prismInit()

    

