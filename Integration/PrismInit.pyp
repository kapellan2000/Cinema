import os
import sys

import c4d
from c4d import gui, plugins, bitmaps

PLUGIN_ID = 1057363
prismRoot = os.getenv("PRISM_ROOT")
if not prismRoot:
	prismRoot = PRISMROOT

pt = prismRoot + "\\Plugins\\Apps\\Cinema\\Integration\\python3.7libs"
if pt not in sys.path:
	sys.path.append(pt)
	
#import PrismInit
# >>>PrismStart
try:
    import PrismInit
    PrismInit.createPrismCore()
except Exception as e:
    print (str(e))
# <<<PrismEnd

menu_prebuild = [
	['File Save...', '1057989', 'prismSave.png'],
	['File Save comment...', '1057990', 'prismSaveComment.png'],
	['Project Browser', '1057991', 'prismBrowser.png'],
	['State Manager', '1057992', 'prismStates.png'],
	['Prism settings', '1057993', 'prismSettings.png'],
]

class callbackPlugin(c4d.plugins.CommandData):
	def __init__(self, callback, *args, **kwargs):
		'''Instantiate the asset options.'''
		super(callbackPlugin, self).__init__(*args, **kwargs)
		self.callback = callback
		
	def _file_save(self):
		PrismInit.pcore.saveScene()

	def _file_save_com(self):
		PrismInit.pcore.saveWithComment()
		
	def _browser(self):
		PrismInit.createPrismCore()
		PrismInit.pcore.projectBrowser()
		
	def _state(self):
		PrismInit.pcore.stateManager()
		
	def _settings(self):
		PrismInit.pcore.prismSettings()
	def Execute(self, doc):

		if self.callback == 'File Save...':
			self._file_save()
		elif self.callback == 'File Save comment...':
			self._file_save_com()
		elif self.callback == 'Project Browser':
			self._browser()
		elif self.callback == 'State Manager':
			self._state()
		elif self.callback == 'Prism settings':
			self._settings()			

		return True



#class TimerMessage(c4d.plugins.MessageData):



class QuadRemesherDialog(c4d.gui.GeDialog):
	pass


class test(c4d.plugins.CommandData):
	dialog = None

	def Execute(self, doc):
		if self.dialog is None:
			self.dialog = QuadRemesherDialog()

		#return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=350, defaulth=200)

	#def RestoreLayout(self, sec_ref):
		#if self.dialog is None:
		#	self.dialog = test2()

		#return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)	
	


if __name__ == "__main__":

	dir, file = os.path.split(__file__)
	icon = bitmaps.BaseBitmap()
	icon.InitWith(os.path.join(dir, "icons", "QuadRemesher_Icon_32.png"))
	#plugins.RegisterCommandPlugin(id=PLUGIN_ID, str="Prism ", help="Prism_pipeline", info=0, dat=test(), icon=icon)
	
	for item in menu_prebuild:
		icon = bitmaps.BaseBitmap()
		icon.InitWith(os.path.join(dir, "icons", item[2]))
		c4d.plugins.RegisterCommandPlugin(
			id=int(item[1]),
			str=item[0],
			info=0,
			help='',
			icon=icon,
			dat=callbackPlugin(callback=item[0])
		)

