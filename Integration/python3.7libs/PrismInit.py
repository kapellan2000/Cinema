import os
import sys


def prismInit(prismArgs=[]):
    if "PRISM_ROOT" in os.environ:
        prismRoot = os.environ["PRISM_ROOT"]
        if not prismRoot:
            return
    else:
        prismRoot = PRISMROOT


    #os.environ['QT_API'] = 'pyside6'
    #sys.path.insert(0,"C:/ProgramData/Prism2/plugins/Cinema/Integration/python3.7libs/PySide6")
    #sys.path.insert(0,"c:/Program Files/Prism2/PythonLibs/CrossPlatform")
    #from qtpy import QtWidgets
    sys.path.insert(0,"C:/ProgramData/Prism2/plugins/Cinema/Integration/python3.7libs/PySide")
    from PySide2 import QtWidgets

    

    qapp = QtWidgets.QApplication.instance()
    
    
    if not qapp:
        QtWidgets.QApplication(sys.argv)

    scriptDir = os.path.join(prismRoot, "Scripts")

    if scriptDir not in sys.path:
        sys.path.append(scriptDir)

    import PrismCore

    global pcore
    pcore = PrismCore.PrismCore(app="Cinema", prismArgs=prismArgs)
    return pcore



    

