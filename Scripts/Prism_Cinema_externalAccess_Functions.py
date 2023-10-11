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
import platform

#try:
#    from PySide2.QtCore import *
#    from PySide2.QtGui import *
#    from PySide2.QtWidgets import *
#except:
#    from PySide.QtCore import *
#    from PySide.QtGui import *
    
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_Cinema_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.core.registerCallback("getPresetScenes", self.getPresetScenes, plugin=self.plugin)
    @err_catcher(name=__name__)
    def getAutobackPath(self, origin):
        #allOri  = ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'addEntityAction', 'backupScenefile', 'connectEntityDlg', 'copySceneFile', 'core', 'createAsset', 'createAssetFolder', 'createCategory', 'createDefaultCat', 'createDepartment', 'createEntity', 'createPresetScene', 'createSceneFromPreset', 'createShot', 'createVersionFromAutoBackup', 'createVersionFromAutoBackupDlg', 'createVersionFromCurrentScene', 'deleteShot', 'entityActions', 'entityDlg', 'entityFolders', 'filterAssets', 'filterOmittedAssets', 'getAsset', 'getAssetActions', 'getAssetDescription', 'getAssetFoldersFromPath', 'getAssetNameFromPath', 'getAssetPathFromAssetName', 'getAssetPaths', 'getAssetRelPathFromPath', 'getAssetSubFolders', 'getAssets', 'getAutobackPath', 'getCategories', 'getCleanEntity', 'getConnectedEntities', 'getCurrentDependencies', 'getDefaultTasksForDepartment', 'getDependencies', 'getEmptyAssetFolders', 'getEntityName', 'getEntityPreview', 'getEntityPreviewPath', 'getHighestVersion', 'getMetaData', 'getPresetScenes', 'getPresetScenesFromFolder', 'getScenePreviewPath', 'getScenefileData', 'getScenefileInfoPath', 'getScenefiles', 'getSequences', 'getShotActions', 'getShotName', 'getShotRange', 'getShots', 'getShotsFromSequence', 'getSteps', 'getTaskData', 'getTaskDataPath', 'getTaskNames', 'getTypeFromPath', 'getUniqueEntities', 'indexOf', 'ingestScenefiles', 'isAssetOmitted', 'isAssetPathOmitted', 'isEntityOmitted', 'isShotOmitted', 'isValidAssetName', 'isValidScenefilename', 'omitEntity', 'omittedEntities', 'orderDepartments', 'orderTasks', 'refreshOmittedEntities', 'removeEntityAction', 'renameSequence', 'renameShot', 'setAssetDescription', 'setComment', 'setConnectedEntities', 'setDescription', 'setEntityPreview', 'setMetaData', 'setScenePreview', 'setScenefileInfo', 'setShotRange', 'setTaskData']
        #for i in allOri:
        #    try:
        #        print(i)
        #        print(getattr(origin, i)())
        #        
        #    except Exception as e:
        #        pass
        #print(origin.getShots()[1][0]['path'].split("03_Production")[0])

        
        autobackpath = origin.getShots()[1][0]['path'].split("03_Production")[0]


        fileStr = "Cinema Scene File ("
        for i in self.sceneFormats:
            fileStr += "*%s " % i

        fileStr += ")"

        return autobackpath, fileStr

    @err_catcher(name=__name__)
    def copySceneFile(self, origin, origFile, targetPath, mode="copy"):
        pass

    @err_catcher(name=__name__)
    def onProjectCreated(self, origin, projectPath, projectName):
        pass
    def getPresetScenes(self, presetScenes):
        presetDir = os.path.join(self.pluginDirectory, "Presets")
        scenes = self.core.entities.getPresetScenesFromFolder(presetDir)
        presetScenes += scenes
