# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2020 Richard Frangenberg
#
# Licensed under GNU GPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


import os
import sys


from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher as err_catcher

import c4d
from c4d import documents, plugins

import time

class Prism_Cinema_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        
        self.importHandlers = {}
        
        self.core.registerCallback(
            "onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self.plugin
        )
        self.core.registerCallback(
            "onStateManagerOpen", self.onStateManagerOpen, plugin=self.plugin
        )
        self.core.registerCallback(
            "onProjectChanged", self.onProjectChanged, plugin=self.plugin
        )
        
        
    @err_catcher(name=__name__)
    def startup(self, origin):
        
        if self.core.uiAvailable:
            
                
            qApp = QApplication.instance()

            if qApp is None:
                qApp = QApplication(sys.argv)

            root = os.path.dirname(self.pluginPath).replace("\\", "/").split("Scripts")[0]
            with (
                open(
                    os.path.join(
                        root,
                        "UserInterfaces",
                        "CinemaStyleSheet",
                        "Cinema.qss",
                    ),
                    "r",
                )
            ) as ssFile:
                ssheet = ssFile.read()

            ssheet = ssheet.replace(
                "qss:",
                os.path.join(
                    root,
                    "UserInterfaces",
                    "CinemaStyleSheet",
                ).replace("\\", "/")
                + "/",
            )

            qApp.setStyleSheet(ssheet)
            appIcon = QIcon(
                os.path.join(
                    self.core.prismRoot, "Scripts", "UserInterfacesPrism", "p_tray.png"
                )
            )
            qApp.setWindowIcon(appIcon)
            
            origin.messageParent = QWidget()
            origin.messageParent.setWindowFlags(origin.messageParent.windowFlags() ^ Qt.WindowStaysOnTopHint)

        origin.timer.stop()

    @err_catcher(name=__name__)
    def autosaveEnabled(self, origin):
        # get autosave enabled
        return False

    @err_catcher(name=__name__)
    def onProjectChanged(self, origin):
        pass

    @err_catcher(name=__name__)
    def sceneOpen(self, origin):
        if hasattr(origin, "asThread") and origin.asThread.isRunning():
            origin.startasThread()
        #origin.sceneUnload()
        #self.updateEnvironment()
        
    @err_catcher(name=__name__)
    def updateEnvironment(self):
        envvars = {
            "PRISM_SEQUENCE": "",
            "PRISM_SHOT": "",
            "PRISM_ASSET": "",
            "PRISM_ASSETPATH": "",
            "PRISM_STEP": "",
            "PRISM_CATEGORY": "",
            "PRISM_USER": "",
            "PRISM_FILE_VERSION": "",
        }

        newenv = {}

        fn = self.core.getCurrentFileName()
        data = self.core.getScenefileData(fn)
        if data["entity"] == "asset":
            newenv["PRISM_SEQUENCE"] = ""
            newenv["PRISM_SHOT"] = ""
            newenv["PRISM_ASSET"] = data["entityName"]
            entityPath = self.core.paths.getEntityBasePath(data["filename"])
            assetPath = self.core.entities.getAssetRelPathFromPath(entityPath)
            newenv["PRISM_ASSETPATH"] = assetPath.replace("\\", "/")
        elif data["entity"] == "shot":
            newenv["PRISM_ASSET"] = ""
            newenv["PRISM_ASSETPATH"] = ""

            sData = self.core.entities.splitShotname(data["entityName"])
            newenv["PRISM_SEQUENCE"] = sData[1]
            newenv["PRISM_SHOT"] = sData[0]
        else:
            newenv["PRISM_SEQUENCE"] = ""
            newenv["PRISM_SHOT"] = ""
            newenv["PRISM_ASSET"] = ""
            newenv["PRISM_ASSETPATH"] = ""

        if data["entity"] != "invalid":
            newenv["PRISM_STEP"] = data["step"]
            newenv["PRISM_CATEGORY"] = data["category"]
            newenv["PRISM_USER"] = getattr(self.core, "user", "")
            newenv["PRISM_FILE_VERSION"] = data["version"]
        else:
            newenv["PRISM_STEP"] = ""
            newenv["PRISM_CATEGORY"] = ""
            newenv["PRISM_USER"] = ""
            newenv["PRISM_FILE_VERSION"] = ""



    @err_catcher(name=__name__)
    def executeScript(self, origin, code, execute=False, logErr=True):
        if logErr:
            try:
                if not execute:
                    return eval(code)
                else:
                    exec(code)
            except Exception as e:
                msg = "\npython code:\n%s" % code
                exec("raise type(e), type(e)(e.message + msg), sys.exc_info()[2]")
        else:
            try:
                if not execute:
                    return eval(code)
                else:
                    exec(code)
            except:
                pass

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin, path=True):
        doc = documents.GetActiveDocument()
        g_dname = doc.GetDocumentName()
        g_path = doc.GetDocumentPath()
        if g_path:
            if path:
                return g_path + "/" + g_dname
            else:
                return g_dname
        else:
            return ""


    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        return self.sceneFormats[0]

    @err_catcher(name=__name__)
    def saveScene(self, origin, filepath, details={}):
        # save scenefile
        doc = documents.GetActiveDocument()
        pt = filepath.replace(filepath.split("/")[-1],"")
        doc.SetDocumentPath(pt)
        if not os.path.exists(pt):
            os.makedirs(pt)
        doc.SetDocumentName(filepath.split("/")[-1])


        file_name, extension = os.path.splitext(os.path.basename(filepath))
        if 'shot' in details:
        
            shot_file_name = details['shot'] + "_" + file_name + extension
        elif 'asset' in details:
            shot_file_name = details['asset'] + "_" + file_name + extension
        else:
            shot_file_name =  file_name + extension
        new_path = os.path.join(os.path.dirname(filepath), shot_file_name)
         
        return documents.SaveDocument(doc, new_path, c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, c4d.FORMAT_C4DEXPORT)
        #return True

    @err_catcher(name=__name__)
    def getImportPaths(self, origin):
        return []

    @err_catcher(name=__name__)
    def getFrameRange(self, origin):
        doc = documents.GetActiveDocument()
        startframe = (doc.GetMinTime().GetFrame(doc.GetFps()))
        endframe = (doc.GetMaxTime().GetFrame(doc.GetFps()))

        return [startframe, endframe]

    @err_catcher(name=__name__)
    def getCurrentFrame(self):
        doc = documents.GetActiveDocument()
        currentFrame = doc.GetTime().GetFrame(doc.GetFps())
        return currentFrame


    @err_catcher(name=__name__)
    def setFrameRange(self, origin, startFrame, endFrame):
        doc = documents.GetActiveDocument()
        doc.SetMinTime(c4d.BaseTime(startFrame/doc.GetFps()))
        doc.SetMaxTime(c4d.BaseTime(endFrame/doc.GetFps()))

    @err_catcher(name=__name__)
    def getFPS(self, origin):
        doc = documents.GetActiveDocument()
        fps = (doc.GetFps())
        return fps

    @err_catcher(name=__name__)
    def setFPS(self, origin, fps):
        doc = documents.GetActiveDocument()
        doc.SetFps(fps)

    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        return "1.0"

    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self, origin):
        # 	origin.sl_preview.mousePressEvent = origin.sliderDrag
        #origin.sl_preview.mousePressEvent = origin.sl_preview.origMousePressEvent
        #origin.mediaBrowser.mediaPlayer.sl_preview.mousePressEvent = (
        #    origin.mediaBrowser.mediaPlayer.sl_preview.origMousePressEvent
        #)
        origin.setStyleSheet("QScrollArea { border: 0px solid rgb(150,150,150); }")
        
    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        # load scenefile
        if (not filepath.endswith(".c4d")):
            return False
        c4d.documents.LoadFile(filepath)
        self.core.sceneOpen()
        return True
        
    @err_catcher(name=__name__)
    def correctExt(self, origin, lfilepath):
        return lfilepath

    @err_catcher(name=__name__)
    def setSaveColor(self, origin, btn):
        btn.setPalette(origin.savedPalette)

    @err_catcher(name=__name__)
    def clearSaveColor(self, origin, btn):
        btn.setPalette(origin.oldPalette)

    @err_catcher(name=__name__)
    def setProject_loading(self, origin):
        pass

    @err_catcher(name=__name__)
    def onPrismSettingsOpen(self, origin):
        pass

    @err_catcher(name=__name__)
    def createProject_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def editShot_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def shotgunPublish_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_addObjects(self, origin, objects=None):
        doc = documents.GetActiveDocument()
        objects = doc.GetSelection()


        if not objects:
            objects = []  # get selected objects from scene

        for i in objects:
            if not i.GetName() in origin.nodes:
                origin.nodes.append(i.GetName())

        origin.updateUi()
        origin.stateManager.saveStatesToScene()

    @err_catcher(name=__name__)
    def getNodeName(self, origin, node):

        if self.isNodeValid(origin, node):
            return node
        else:
            return "invalid"

    @err_catcher(name=__name__)
    def selectNodes(self, origin):
        doc = documents.GetActiveDocument()
        if origin.lw_objects.selectedItems() != []:
            nodes = []
            ind = 0
            for i in origin.lw_objects.selectedItems():
                node = origin.nodes[origin.lw_objects.row(i)]
                if self.isNodeValid(origin, node):
                    #nodes.append(node)
                    sObj = doc.SearchObject(node)
                    if ind == 0:
                         doc.SetActiveObject(sObj, mode=c4d.SELECTION_NEW)
                    else:
                         doc.SetActiveObject(sObj, mode=c4d.SELECTION_ADD)
                    ind +=1
            c4d.EventAdd()
            # select(nodes)






    @err_catcher(name=__name__)
    def isNodeValid(self, origin, handle):
        doc = documents.GetActiveDocument()
        myObject = doc.SearchObject(handle)
        if myObject:
            return True
        else:
            return False

    @err_catcher(name=__name__)
    def get_all_objects(self, op, filter, output):
        arr = []
        while op:
            if filter(op):
                output.append(op.GetName())
                arr.append(op)
            self.get_all_objects(op.GetDown(), filter, output)
            op = op.GetNext()
        return output, arr




    @err_catcher(name=__name__)
    def getCamNodes(self, origin, cur=False):
        sceneCams = []  # get cams from scene

        doc = documents.GetActiveDocument()
        sceneCams, obj = self.get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(c4d.Ocamera), [])
        #if cur:
         #   sceneCams = ["Current View"] + sceneCams

        return sceneCams

    @err_catcher(name=__name__)
    def getCamName(self, origin, handle):

        if handle == "Current View":
            doc = documents.GetActiveDocument()
            selectedCamera = doc.GetActiveBaseDraw().GetSceneCamera(doc)
            nodes = (selectedCamera.GetName())
            return nodes
        else:
            return str(handle)


    @err_catcher(name=__name__)
    def selectCam(self, origin):
        if self.isNodeValid(origin, origin.curCam):
            select(origin.curCam)

    @err_catcher(name=__name__)
    def sm_export_startup(self, origin):
        #origin.l_convertExport.setVisible(False)
        origin.l_additionalOptions.setVisible(False)
        origin.chb_additionalOptions.setVisible(False)
        #origin.chb_convertExport.setVisible(False)
        #origin.w_convertExport.setVisible(False)
        origin.w_additionalOptions.setVisible(False)

    # 	@err_catcher(name=__name__)
    # 	def sm_export_setTaskText(self, origin, prevTaskName, newTaskName):
    # 		origin.l_taskName.setText(newTaskName)

    @err_catcher(name=__name__)
    def sm_export_removeSetItem(self, origin, node):
        pass

    @err_catcher(name=__name__)
    def sm_export_clearSet(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_updateObjects(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_exportShotcam(self, origin, startFrame, endFrame, outputName):
        result = self.sm_export_exportAppObjects(
            origin,
            startFrame,
            endFrame,
            (outputName + ".abc"),
            nodes=[origin.curCam],
            expType=".abc",
        )
        result = self.sm_export_exportAppObjects(
            origin,
            startFrame,
            endFrame,
            (outputName + ".fbx"),
            nodes=[origin.curCam],
            expType=".fbx",
        )
        return result

    @err_catcher(name=__name__)
    def sm_export_exportAppObjects(
        self,
        origin,
        startFrame,
        endFrame,
        outputName,
        scaledExport=False,
        nodes=None,
        expType=None,
    ):

        if expType is None:
            expType = origin.getOutputType()
        if expType == ".c4d":
            chosenExportMethod = 900000
        elif expType == ".abc":
            chosenExportMethod = 900002
        elif expType == ".obj":
            chosenExportMethod = 900014
        elif expType == ".fbx":
            chosenExportMethod = 900009
        #elif expType == "ShotCam":
        #   chosenExportMethod = 900002

        # dict with menu id, formatending, command-code
        fileFormatDict = {900000: [".c4d", 1001026],
                      900001: [".3ds", 1001038],
                      900002: [".abc", 1028082],
                      900003: [".xml", 1016440],
                      900004: [".bullet", 180000105],
                      900005: [".dae", 1022316],
                      900006: [".dae", 1025755],
                      900007: [".x", 1001047],
                      900008: [".dxf", 1001036],
                      900009: [".fbx", 1026370],
                      900010: [".ai", 1012074],
                      900011: [".stl", 1001021],
                      900012: [".vdb", 1039865],
                      900013: [".wrl", 1001034],
                      900014: [".obj", 1030178]}

        doc = documents.GetActiveDocument()
        objList = []
        for x in origin.nodes:
            objList.append(doc.SearchObject(x))


        #myObject = doc.SearchObject("Cube")#select

        if origin.chb_wholeScene.isChecked():
            objList, obj = self.get_all_objects(doc.GetFirstObject(), lambda x: x, [])

        else:
            objList = doc.GetSelection()


        if chosenExportMethod in fileFormatDict:
            # create folder, if not present
            #if not os.path.exists(setupFolder):
             #   os.makedirs(setupFolder)
            fileFormatEnding = fileFormatDict[chosenExportMethod][0]
            cmdNr = fileFormatDict[chosenExportMethod][1]
            tmpList = []

            for obj in objList:
                # check type
                if isinstance(obj, c4d.BaseObject) or origin.chb_wholeScene.isChecked():
                    if expType == ".obj":
                        for i in range(startFrame, endFrame + 1):
                            if origin.chb_wholeScene.isChecked():
                                obj = ""
                                for obj in objList:
                                    tmpList.insert(0, obj)
                            else:
                                tmpList.insert(0, obj)
                            # create temp doc and insert selected obj into it
                            theTempDoc = documents.IsolateObjects(doc, tmpList)
                            # some list-stuff
                            fps = doc.GetFps()
                            # Set current frame
                            time = c4d.BaseTime(i, fps)
                            doc.SetTime(time)
                            
                            foutputName = outputName.replace("####", format(i, "04")).replace("\\","/")

                            documents.SaveDocument(theTempDoc, foutputName, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, cmdNr)
                            # some list-stuff
                            if origin.chb_wholeScene.isChecked():
                                obj = ""
                                for obj in objList:
                                    tmpList.remove(obj)
                            else:
                                tmpList.remove(obj)
                            # kill temp doc
                            documents.KillDocument(theTempDoc)
                        outputName = foutputName
                    if expType == ".fbx":
                        foutputName = outputName.replace("\\","/")
                        backup_options = {}
                        export_options = {c4d.FBXEXPORT_LIGHTS: 1,
                                          c4d.FBXEXPORT_CAMERAS: 0,
                                          c4d.FBXEXPORT_SPLINES: 1,
                                          # Geometry and Materials
                                          c4d.FBXEXPORT_SAVE_NORMALS: 1,
                                          #c4d.FBXEXPORT_TEXTURES: 1,
                                          c4d.FBXEXPORT_EMBED_TEXTURES: 1,
                                          c4d.FBXEXPORT_FBX_VERSION: c4d.FBX_EXPORTVERSION_NATIVE,
                                          # cancel all these one
                                          c4d.FBXEXPORT_PLA_TO_VERTEXCACHE: 0,
                                          c4d.FBXEXPORT_SAVE_VERTEX_MAPS_AS_COLORS: 0,
                                          c4d.FBXEXPORT_TRIANGULATE: 0,
                                          c4d.FBXEXPORT_SDS_SUBDIVISION: 1,
                                          c4d.FBXEXPORT_ASCII: 0}
                        export_options[c4d.FBXEXPORT_TRACKS] = 1
                        if origin.chb_wholeScene.isChecked():
                            export_options[c4d.FBXEXPORT_SELECTION_ONLY] = 0
                        else:
                            export_options[c4d.FBXEXPORT_SELECTION_ONLY] = 1
                        if startFrame == endFrame:
                            export_options[c4d.FBXEXPORT_BAKE_ALL_FRAMES] = 0
                        else:
                            export_options[c4d.FBXEXPORT_BAKE_ALL_FRAMES] = 1
                        options = plugins.FindPlugin(cmdNr, c4d.PLUGINTYPE_SCENESAVER)
                        
                        for key in export_options:
                            if options[key] != export_options[key]:
                                backup_options[key] = options[key]
                            options[key] = export_options[key]
                            
                        backup_start = doc.GetMinTime()
                        backup_end = doc.GetMaxTime()
                        self.core.setFrameRange(startFrame, endFrame)
                        
  
                        # FBX Export
                        documents.SaveDocument(doc, foutputName,
                                               c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, cmdNr)
                
                        # restore options
                        for key in backup_options:
                            if backup_options[key]:
                                options[key] = backup_options[key]
                        doc.SetMinTime(backup_start)
                        doc.SetMaxTime(backup_end)  
            
                    if expType == ".abc":
                        # Get Alembic export plugin, 1028082 is its ID
                        plug = plugins.FindPlugin(cmdNr, c4d.PLUGINTYPE_SCENESAVER)

                        foutputName = outputName.replace("\\","/")

                        op = {}
                        # Send MSG_RETRIEVEPRIVATEDATA to Alembic export plugin
                        if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):


                            # BaseList2D object stored in "imexporter" key hold the settings
                            abcExport = op["imexporter"]


                            # Change Alembic export settings
                            abcExport[c4d.ABCEXPORT_FRAME_START] = startFrame
                            abcExport[c4d.ABCEXPORT_FRAME_END] = endFrame
                            abcExport[c4d.ABCEXPORT_FRAME_STEP] = 1
                            abcExport[c4d.ABCEXPORT_SUBFRAMES] = 1
                            if origin.chb_wholeScene.isChecked():
                                abcExport[c4d.ABCEXPORT_SELECTION_ONLY] = False
                                print("select only")
                            else:
                                abcExport[c4d.ABCEXPORT_SELECTION_ONLY] = True
                            abcExport[c4d.ABCEXPORT_PARTICLES] = True
                            abcExport[c4d.ABCEXPORT_PARTICLE_GEOMETRY] = True

                            # Finally export the document
                            if documents.SaveDocument(doc, foutputName, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, cmdNr):
                                print(foutputName)
                            else:
                                print ("Export failed!")
                            outputName = foutputName
                if origin.chb_wholeScene.isChecked():
                    break
                            
            if expType == ".c4d":
                

                foutputName = outputName.replace("\\","/")

                # save scenefile
                doc = documents.GetActiveDocument()
                if origin.chb_wholeScene.isChecked(): 
                    documents.SaveDocument(doc, foutputName, c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, c4d.FORMAT_C4DEXPORT)
                else:
                


                    # Create a new document to hold the selected object(s)
                    export_doc = c4d.documents.BaseDocument()
                    export_doc.SetDocumentName("Exported Objects")
                    for obj in objList:
                        # Clone the selected object(s) and add it to the export document
                        cloned_obj = obj.GetClone(c4d.COPYFLAGS_0)
                        export_doc.InsertObject(cloned_obj)
                        
                    # Save the export document to the specified file path
                    c4d.documents.SaveDocument(export_doc, foutputName, c4d.SAVEDOCUMENTFLAGS_0, 1001026)
                    # Delete the export document
                    c4d.documents.KillDocument(export_doc)  
                        
                outputName = foutputName
                




        return outputName
    #def sm_createStatePressed(self, origin, stateType):
    #    pass
    @err_catcher(name=__name__)
    def sm_export_preDelete(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_unColorObjList(self, origin):
        origin.lw_objects.setStyleSheet(
            "QListWidget { border: 3px solid rgb(50,50,50); }"
        )

    @err_catcher(name=__name__)
    def sm_export_typeChanged(self, origin, idx):
        if idx == ".c4d":
            origin.chb_wholeScene.setChecked(True)
            origin.chb_wholeScene.setDisabled(False)
        else:
            origin.chb_wholeScene.setChecked(False)
            origin.chb_wholeScene.setDisabled(False)
    @err_catcher(name=__name__)
    def sm_export_preExecute(self, origin, startFrame, endFrame):
        warnings = []

        return warnings

    @err_catcher(name=__name__)
    def sm_export_loadData(self, origin, data):
        pass

    @err_catcher(name=__name__)
    def sm_export_getStateProps(self, origin, stateProps):
        stateProps.update()

        return stateProps

    @err_catcher(name=__name__)
    def sm_render_isVray(self, origin):
        return False

    @err_catcher(name=__name__)
    def sm_render_setVraySettings(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_render_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_render_getRenderLayer(self, origin):
        rlayerNames = []

        return rlayerNames

    @err_catcher(name=__name__)
    def sm_render_refreshPasses(self, origin):
        #origin.gb_passes.setVisible(False)
        origin.b_addPasses.setVisible(False)
        origin.lw_passes.setVisible(False)
        
        #self.tw_passes.itemChanged.connect(self.setPassData)
        #pass

    

    @err_catcher(name=__name__)
    def sm_render_openPasses(self, origin, item=None):
        pass

    @err_catcher(name=__name__)
    def removeAOV(self, aovName):
        pass

    @err_catcher(name=__name__)
    def sm_render_preSubmit(self, origin, rSettings):
        rSettings["outputName"] = rSettings["outputName"].replace("\\beauty","")
        if origin.chb_resOverride.isChecked():
            doc = c4d.documents.GetActiveDocument()
            rd = doc.GetActiveRenderData()
            rd[c4d.RDATA_XRES] = float(origin.sp_resWidth.value())
            rd[c4d.RDATA_YRES] = float(origin.sp_resHeight.value())

    @err_catcher(name=__name__)
    def sm_render_name(self):


        # Get the current document
        doc = c4d.documents.GetActiveDocument()

        # Get the active render data
        render_data = doc.GetActiveRenderData()

        # Get the render settings from the render data
        render_settings = render_data.GetDataInstance()
        print(render_settings)
        # Get the current render settings
        current_render = render_settings.GetLong(c4d.RDATA_RENDERENGINE)

        # Print the current render engine
        print("Current render engine:", current_render)
        return sm_render_name

    @err_catcher(name=__name__)
    def sm_render_startLocalRender(self, origin, outputName, rSettings):

        doc = documents.GetActiveDocument()
        if rSettings["startFrame"] is None:
            frameChunks = [[x, x] for x in rSettings["frames"]]
        else:
            frameChunks = [[rSettings["startFrame"], rSettings["endFrame"]]]

        try:
            rdata = doc.GetActiveRenderData()
            rdata[c4d.RDATA_PATH] = rSettings["outputName"].replace("\\beauty","")
            if origin.gb_passes.isChecked():
                try:
                    octane = rdata.GetFirstVideoPost()
                    octane[c4d.SET_PASSES_ENABLED] = True
                    octane[c4d.SET_PASSES_SAVEPATH] = rSettings["outputName"].replace("\\beauty","")
                    octane[c4d.RDATA_PROJECTFILE] = False
                except:
                    pass
                rdata()[c4d.RDATA_MULTIPASS_SAVEIMAGE] = True
                rdata[c4d.RDATA_MULTIPASS_FILENAME] = rSettings["outputName"].replace("\\beauty","")
            else:
                try:
                    octane = rdata.GetFirstVideoPost()
                    octane[c4d.SET_PASSES_ENABLED] = False
                    octane[c4d.SET_PASSES_SAVEPATH] = ""
                except:
                    pass
                rdata()[c4d.RDATA_MULTIPASS_SAVEIMAGE] = False
                rdata[c4d.RDATA_MULTIPASS_FILENAME] = ""
                
            rdata[c4d.RDATA_FRAMEFROM] = c4d.BaseTime( rSettings["startFrame"], doc.GetFps())
            rdata[c4d.RDATA_FRAMETO] = c4d.BaseTime( rSettings["endFrame"],  doc.GetFps())
            #rdata[c4d.RDATA_MULTIPASS_SAVEIMAGE] = False #turns off save multipass
            rdata[c4d.RDATA_FRAMESTEP] = 1
            c4d.CallCommand(12099)

            return "Result=Success"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            erStr = "%s ERROR - sm_default_imageRender %s:\n%s" % (
                time.strftime("%d/%m/%y %X"),
                origin.core.version,
                traceback.format_exc(),
            )
            self.core.writeErrorLog(erStr)
            return "Execute Canceled: unknown error (view console for more information)"

    @err_catcher(name=__name__)
    def sm_render_undoRenderSettings(self, origin, rSettings):
        pass

    @err_catcher(name=__name__)
    def sm_render_getDeadlineParams(self, origin, dlParams, homeDir):
        pass

    @err_catcher(name=__name__)
    def getCurrentRenderer(self, origin):
        return "Renderer"

    @err_catcher(name=__name__)
    def getCurrentSceneFiles(self, origin):
        curFileName = self.core.getCurrentFileName()
        scenefiles = [curFileName]
        return scenefiles

    @err_catcher(name=__name__)
    def sm_render_getRenderPasses(self, origin):
        return []

    @err_catcher(name=__name__)
    def sm_render_addRenderPass(self, origin, passName, steps):
        pass

    @err_catcher(name=__name__)
    def sm_render_preExecute(self, origin):
        warnings = []

        return warnings

    @err_catcher(name=__name__)
    def sm_render_fixOutputPath(self, origin, outputName, singleFrame=False):
        return outputName

    @err_catcher(name=__name__)
    def getProgramVersion(self, origin):
        return "1.0"

    @err_catcher(name=__name__)
    def sm_render_getDeadlineSubmissionParams(self, origin, dlParams, jobOutputFile):
        dlParams["Build"] = dlParams["build"]
        dlParams["OutputFilePath"] = os.path.split(jobOutputFile)[0]
        dlParams["OutputFilePrefix"] = os.path.splitext(
            os.path.basename(jobOutputFile)
        )[0]
        dlParams["Renderer"] = self.getCurrentRenderer(origin)

        if origin.chb_resOverride.isChecked() and "resolution" in dlParams:
            resString = "Image"
            dlParams[resString + "Width"] = str(origin.sp_resWidth.value())
            dlParams[resString + "Height"] = str(origin.sp_resHeight.value())

        return dlParams

    @err_catcher(name=__name__)
    def deleteNodes(self, origin, handles, num=0):
        if (num + 1) > len(handles):
            return False
        doc = documents.GetActiveDocument()
        if type(handles) is list:
            for i in handles:
                mat_thumbs = doc.SearchObject(i)
                if mat_thumbs:
                    mat_thumbs.Remove()
                    c4d.EventAdd()
        else:
            mat_thumbs = doc.SearchObject(handles)
            if mat_thumbs:
                mat_thumbs.Remove()
                c4d.EventAdd()

    @err_catcher(name=__name__)
    def sm_import_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_import_disableObjectTracking(self, origin):
        self.deleteNodes(origin, [origin.setName])


    def get_userData(self, obj):

        for userDataId, bc in obj.GetUserDataContainer():
            currentName = bc.GetString(c4d.DESC_NAME)#User Data Name
            if currentName == "Prism":
                cycleBC = bc.GetContainer(c4d.DESC_CYCLE)
                id = (userDataId[1].id)
                return(obj[c4d.ID_USERDATA,id])
            else:
                return 

        #obj = doc.GetActiveObject()    # Here you get selected/active object from scene

        #for id, bc in obj.GetUserDataContainer():

         #   print("User Data ID: " + str(id))
          #  print("User Data Value: " + str(op[id]))
           # print("User Data Name: " + bc[c4d.DESC_NAME])


    @err_catcher(name=__name__)
    def sm_import_importToApp(self, origin, doImport, update, impFileName):
        if not os.path.exists(impFileName):
            QMessageBox.warning(
                self.core.messageParent,
                "ImportFile",
                "File doesn't exist:\n\n%s" % impFileName,
            )
            return

        fileName = os.path.splitext(os.path.basename(impFileName))
        importOnly = True
        applyCache = False
        updateCache = False
        doGpuCache = False
        importedNodes = []
        action = 1
        
        doc =documents.GetActiveDocument()
        #obj = doc.GetActiveObjectsFilter(True, type=1025766, instanceof=False)# OPTIMIZE !!!
        menu = False
        if doc.GetFirstObject():
            sceneCams, obj = self.get_all_objects(doc.GetFirstObject(), lambda x: x.CheckType(c4d.Oxref), [])
            
            for i in obj:
                if self.get_userData(i):

                    if self.get_userData(i).split("_v0")[0]==fileName[0].split("_v0")[0]:
                        menu = True
                        break
                        
        if menu and update==False:
            msg = QMessageBox(QMessageBox.Question, "Delete state", "Do you want to replace all?", QMessageBox.Yes)#16384
            msg.addButton("Replace selected", QMessageBox.AcceptRole)#0
            msg.addButton("Import", QMessageBox.NoRole)#1
            msg.setParent(self.core.messageParent, Qt.Window)
            action = msg.exec_()



        if importOnly:
            #origin.preDelete(
            #    baseText="Do you want to delete the currently connected objects?\n\n"
            #)

            if update==False and action == 1:
                #if fileName[1] == ".fbx":
                #    mel.eval("FBXImportMode -v merge")
                #    mel.eval("FBXImportConvertUnitString  -v cm")

                kwargs = {
                    "i": True,
                    "returnNewNodes": True,
                    "importFunction": self.basicImport
                }

                if fileName[1] in self.importHandlers:
                    kwargs.update(self.importHandlers[fileName[1]])

                result = kwargs["importFunction"](impFileName, kwargs)
                if result and result["result"]:
                    importedNodes = result["nodes"]
                else:
                    importedNodes = []
                    if result:
                        if "error" not in result:
                            return

                        error = str(result["error"])
                    else:
                        error = ""

                    msg = "An error occured while importing the file:\n\n%s\n\n%s" % (
                        impFileName,
                        error,
                    )
                    self.core.popup(msg, title="Import error")

            #elif action == 16384:

             #   doc =documents.GetActiveDocument()
             #   obj = doc.GetActiveObjectsFilter(True, type=1025766, instanceof=False)# OPTIMIZE !!!
             #   for i in obj:
             #       print(self.get_userData(i))

            elif action == 0 or update==True or action == 16384: 
                
                updateCache = True
                importedNodes = []
                doc =documents.GetActiveDocument()
                
                

                
                if update==True:
                
                    ind = 0
                    for i in origin.nodes:
                            sObj = doc.SearchObject(i)
                            if ind == 0:
                                 doc.SetActiveObject(sObj, mode=c4d.SELECTION_NEW)
                            else:
                                 doc.SetActiveObject(sObj, mode=c4d.SELECTION_ADD)
                            ind =1
                    #self.selectNodes(origin.nodes)

                if action == 16384: # replace all
                    obj = doc.GetActiveObjectsFilter(True, type=1025766, instanceof=False)
                else:
                    obj = doc.GetSelection()
                for i in obj:
                    namespace = os.path.basename(impFileName).split(".")[0]
                    #namespace = i.GetName()
                    
                    n_id=0

                    while (doc.SearchObject(namespace + "_"+ str('{:04d}'.format(n_id)))):
                        n_id += 1
                    namespace_id = namespace + "_" + str('{:04d}'.format(n_id))
                    i.SetName(namespace_id)
                    
                    status = i.SetParameter(c4d.ID_CA_XREF_FILE, impFileName, c4d.DESCFLAGS_SET_USERINTERACTION)
                    importedNodes.append(namespace_id)
                    for userDataId, bc in i.GetUserDataContainer():
                        currentName = bc.GetString(c4d.DESC_NAME)
                        if currentName == "Prism":
                            cycleBC = bc.GetContainer(c4d.DESC_CYCLE)
                            id = (userDataId[1].id)
                            i()[c4d.ID_USERDATA,id] = namespace
                            
                        c4d.EventAdd()


#        for i in importedNodes:
#            cams = cmds.listCameras()
#            if i in cams:
#                cmds.camera(i, e=True, farClipPlane=1000000)

        if origin.chb_trackObjects.isChecked():
            origin.nodes = importedNodes
        else:
            origin.nodes = []

        # buggy
        # cmds.select([ x for x in origin.nodes if self.isNodeValid(origin, x)])
        #self.validateSet(origin.setName)
        #if self.isNodeValid(self, origin.setName):
        #    cmds.delete(origin.setName)

        #if len(origin.nodes) > 0:
        #    origin.setName = cmds.sets(name="Import_%s_" % fileName[0])
        #for node in origin.nodes:
        #    cmds.sets(node, include=origin.setName)
        result = len(importedNodes) > 0

        rDict = {"result": result, "doImport": doImport}

        rDict["mode"] = "ApplyCache" if (applyCache or updateCache) else "ImportFile"
        return rDict


    def basicImport(self, filepath, kwargs):
        del kwargs["importFunction"]

        try:
            
            namespace = os.path.basename(filepath).split(".")[0]  #eds_report.csv

            #if self.isNodeValid(origin, origin.curCam)

            doc = documents.GetActiveDocument()
            c4d.CallCommand(12112)
            objects = doc.GetSelection()
            #c4d.documents.MergeDocument(doc, filepath, 1);


            xref = c4d.BaseObject(c4d.Oxref)
            doc.InsertObject(xref)
            xref.SetParameter(c4d.ID_CA_XREF_FILE, filepath, c4d.DESCFLAGS_SET_USERINTERACTION)
            xref.SetParameter(c4d.ID_CA_XREF_NAMESPACE, "", c4d.DESCFLAGS_SET_USERINTERACTION)
            n_id=0

            while (doc.SearchObject(namespace + "_"+ str('{:04d}'.format(n_id)))):
                n_id += 1
            namespace_id = namespace + "_" + str('{:04d}'.format(n_id))
            xref.SetName(namespace_id)
            c4d.EventAdd()
            
            
            c4d.CallCommand(12112)
            importedNew = doc.GetSelection()
            importedNodes = []
            for item in importedNew:
                if not item in objects:
                    importedNodes.append(item.GetName())



            #obj = doc.GetActiveObject()    # Here you get selected/active object from scene
            obj = doc.SearchObject(namespace_id)

            bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STRING) # Create default container
            bc[c4d.DESC_NAME] = "Prism" # Rename the entry

            element = obj.AddUserData(bc) # Add userdata container
            obj[element] = str(namespace) # Assign a value
            c4d.EventAdd() # Update




        except Exception as e:
            result = {"result": False, "error": e}
            return result
        result = {"nodes": importedNodes,"result": True}

        return result



    @err_catcher(name=__name__)
    def sm_import_updateObjects(self, origin):
        if origin.setName == "":
            return

        prevSel = cmds.ls(selection=True, long=True)
        cmds.select(clear=True)
        try:
            # the nodes in the set need to be selected to get their long dag path
            cmds.select(origin.setName)
        except:
            pass

        origin.nodes = cmds.ls(selection=True, long=True)
        try:
            cmds.select(prevSel)
        except:
            pass
            
    @err_catcher(name=__name__)
    def sm_import_removeNameSpaces(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_import_unitConvert(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_playblast_startup(self, origin):
        frange = self.getFrameRange(origin)
        origin.sp_rangeStart.setValue(frange[0])
        origin.sp_rangeEnd.setValue(frange[1])

    @err_catcher(name=__name__)
    def sm_playblast_createPlayblast(self, origin, jobFrames, outputName):
        doc = documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
        outputName = outputName.replace("####.","")
        rd[c4d.RDATA_SAVEIMAGE] = True
        rd[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_PREVIEWHARDWARE
        rd[c4d.RDATA_PATH] = outputName
        rd[c4d.RDATA_FORMAT] = c4d.FILTER_MOVIE
        #rd[c4d.RDATA_FRAMESEQUENCE] = 0
        rd[c4d.RDATA_FRAMEFROM] = c4d.BaseTime( jobFrames[0], doc.GetFps())
        rd[c4d.RDATA_FRAMETO] = c4d.BaseTime( jobFrames[1], doc.GetFps())


        # Creates a Multi Pass Bitmaps that will store the render result
        bmp = c4d.bitmaps.MultipassBitmap(int(rd[c4d.RDATA_XRES]), int(rd[c4d.RDATA_YRES]), c4d.COLORMODE_RGB)
        if bmp is None:
            raise RuntimeError("Failed to create the bitmap.")

        # Adds an alpha channel
        bmp.AddChannel(True, True)

        # Renders the document
        render_flags = (c4d.RENDERFLAGS_PREVIEWRENDER | c4d.RDATA_SHOWHUD | c4d.RENDERFLAGS_NODOCUMENTCLONE)

        c4d.documents.RenderDocument(doc, rd.GetData(), bmp, render_flags)

        # Displays the render in the Picture Viewer
        #c4d.bitmaps.ShowBitmap(bmp)
    @err_catcher(name=__name__)
    def sm_playblast_preExecute(self, origin):
        warnings = []

        return warnings

    @err_catcher(name=__name__)
    def sm_playblast_execute(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_playblast_postExecute(self, origin):
        pass

    @err_catcher(name=__name__)
    def onStateManagerOpen(self, origin):
        origin.b_description.setMinimumWidth(30)
        origin.b_description.setMaximumWidth(30)
        origin.b_preview.setMinimumWidth(30)
        origin.b_preview.setMaximumWidth(30)
        #self.outputFormats = [
        #    ".exr",
        #    ".png",
        #    ".jpg",
        #    ".psd",
        #]
        #origin.cb_format.addItems()
    @err_catcher(name=__name__)

    def sm_userData(self, data, name, opr):
        doc = documents.GetActiveDocument()
        data_id = None
        for id, bc in doc.GetUserDataContainer():

            # Retrieves the current name we iterates
            currentName = bc.GetString(c4d.DESC_NAME)
            # If the name is the same return True
            if currentName == name:
                data_id = id[1].id
                break
        if opr=="w":
            if data_id:
                #aaa = doc[c4d.ID_USERDATA,1]
                doc[c4d.ID_USERDATA,data_id] = data
            else:
                obj = doc

                bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STRING) # Create default container
                bc[c4d.DESC_NAME] = name # Rename the entry
                bc.SetInt32(c4d.DESC_CUSTOMGUI, c4d.CUSTOMGUI_STRINGMULTI) # Set user data gui

                element = obj.AddUserData(bc) # Add userdata container
                obj[element] = data # Assign a value
                c4d.EventAdd() # Update
        elif opr=="r":
            if data_id:
                return (doc[c4d.ID_USERDATA,data_id])
            else:
                return(None)
        else:
            return(None)
    def sm_saveStates(self, origin, buf):
        self.sm_userData(buf,"PrismStates","w")

    @err_catcher(name=__name__)
    def sm_saveImports(self, origin, importPaths):
        self.sm_userData(importPaths,"PrismImports","w")

    @err_catcher(name=__name__)
    def sm_readStates(self, origin):
        #stateData = hou.node("/obj").userData("PrismStates")
        
        stateData = self.sm_userData("","PrismStates","r")
        if stateData is not None:
            return stateData

    @err_catcher(name=__name__)
    def sm_deleteStates(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_getExternalFiles(self, origin):
        extFiles = []
        return [extFiles, []]

    @err_catcher(name=__name__)
    def sm_createRenderPressed(self, origin):
        origin.createPressed("Render")