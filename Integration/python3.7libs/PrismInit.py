import os
import sys
#import inspect
def prismInit(prismArgs=[]):

    Dir = os.path.join(
        os.path.abspath(
            os.path.join(
                __file__,
                os.pardir,
                os.pardir,
                os.pardir,
                os.pardir,
                os.pardir,
                os.pardir,
                "Scripts",
            )
        )
    )
    if Dir not in sys.path:
        sys.path.append(Dir)

    #prismArgs.append("noUI")
    #prismArgs=[]
    import PrismCore

    pcore = PrismCore.PrismCore(app="Cinema", prismArgs=prismArgs)
    return pcore


def createPrismCore():
    prismRoot = os.getenv("PRISM_ROOT")

    py_side_p = prismRoot + "/PythonLibs/Python37/PySide"
    #py_side_p = prismRoot + "/PythonLibs/Python39/PySide"
    sys.path.append(py_side_p)
    global pcore

    pcore = prismInit()

    

