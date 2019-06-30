import sys, os, shutil
import math

from Class.Transition import Transition
from Class.Drawer import Drawer
from Class.State import State
from Class.Scene import Scene
from Class.View import myview
from Class.IO import IO

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize, QRect, QPoint, QSize, QRectF
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QDrag, QPalette, QImage, QColor, QRegion
from PyQt5.QtWidgets import QMainWindow, QMenu, QToolButton, QApplication, QMessageBox, QWidget, QAction, QGraphicsScene, QGraphicsView, QGraphicsItem, QPushButton, QToolBar, QInputDialog, QFileDialog, QApplication, QDialogButtonBox

##	@package MAinWindow
##	Class derivated from QMAinWindow pyQt5 class
class Window(QMainWindow):

#@note This will have an indented section on its page, nice for method notes and limitations
#@bug Doxygen creates a separate bugs page, very nice for notes-to-self-to-fix-this
#@todo Similar, only to-do instead of a bug
#@author, @date - Put these in the header of the file
#@brief Short description of what the file/method/subroutine does
#@filename Put this in the header of the file - note that case must match the actual filename
#@param [param name] Use this to document parameters to a function
#@retval Use this to document the return value of a function

	##Create the main software window
	def __init__(self):
		#initialisation function
		super().__init__()#attributes QMainWindow properties to the object
		screen = QApplication.desktop()
		screen_size = screen.screenGeometry()
		self.title="O'Tomates Mozarella"
		self.left=50
		self.top=50
		self.width= screen_size.width()
		self.height=screen_size.height()
		self.transitions_temp = list()
		self.grid = False
		#self.refresh_tmp()
		self.num_instance = 0
		self.num_instance_max = 0

		self.preview_flag = False
		self.magnet = False

		self.toolbar_icon_size = self.height / 22
		self.pressedPosition=None

		self.initUI()
		self.something_happened()

	##Init all UI components
	def initUI(self):
		self.setGeometry(self.left,self.top,self.width,self.height)

		self.actions =[]

		#-------Exit Action--------
		self.exitAct = QAction(QtGui.QIcon("Img/exit.png"),"Exit", self)
		self.exitAct.setShortcut("Ctrl+Q")
		self.exitAct.setStatusTip("Exit application")
		self.exitAct.triggered.connect(self.exit)
		self.actions.append(self.exitAct)

		#------Latex export Action--------
		self.latexAct = QAction(QtGui.QIcon("Img/latex.png"),"Export to LaTex", self)
		self.latexAct.setShortcut("Ctrl+Shift+S")
		self.latexAct.setStatusTip("Export to LaTex")
		self.latexAct.triggered.connect(self.latex)
		self.actions.append(self.latexAct)

		#------Open Action--------
		self.openAct = QAction(QtGui.QIcon("Img/open.png"),"Open", self)
		self.openAct.setShortcut("Ctrl+O")
		self.openAct.setStatusTip("Open")
		self.openAct.triggered.connect(self.open)
		self.actions.append(self.openAct)

		#------Save Action--------
		self.saveAct = QAction(QtGui.QIcon("Img/save.png"),"Save", self)
		self.saveAct.setShortcut("Ctrl+S")
		self.saveAct.setStatusTip("Save")
		self.saveAct.triggered.connect(self.save)
		self.actions.append(self.saveAct)

		#------Copy Action--------
		self.copyAct = QAction(QtGui.QIcon("Img/copy.png"),"Copy", self)
		self.copyAct.setShortcut("Ctrl+C")
		self.copyAct.setStatusTip("Copy")
		self.copyAct.triggered.connect(self.copy)
		self.actions.append(self.copyAct)

		#------Paste Action--------
		self.pasteAct = QAction(QtGui.QIcon("Img/paste.png"),"Paste", self)
		self.pasteAct.setShortcut("Ctrl+V")
		self.pasteAct.setStatusTip("Paste")
		self.pasteAct.triggered.connect(self.paste)
		self.actions.append(self.pasteAct)

		#------Undo Action--------
		self.undoAct = QAction(QtGui.QIcon("Img/undo.png"),"Undo", self)
		self.undoAct.setShortcut("Ctrl+Z")
		self.undoAct.setStatusTip("Undo")
		self.undoAct.triggered.connect(self.undo)
		self.actions.append(self.undoAct)

		#------Redo Action--------
		self.redoAct = QAction(QtGui.QIcon("Img/redo.png"),"Redo", self)
		self.redoAct.setShortcut("Ctrl+Y")
		self.redoAct.setStatusTip("Redo")
		self.redoAct.triggered.connect(self.redo)
		self.actions.append(self.redoAct)

		#------Formula Action--------
		self.formulaAct = QAction(QtGui.QIcon("Img/formula.png"),"Preview Formulas", self)
		self.formulaAct.setShortcut("Ctrl+Shift+F")
		self.formulaAct.setStatusTip("Preview Formulas")
		self.formulaAct.triggered.connect(self.formula)
		self.actions.append(self.formulaAct)

		#------Delete Action--------
		self.deleteAct = QAction(QtGui.QIcon("Img/delete.png"),"Delete", self)
		self.deleteAct.setShortcut("Del")
		self.deleteAct.setStatusTip("Delete")
		self.deleteAct.triggered.connect(self.delete)
		self.actions.append(self.deleteAct)

		#------Status Action--------
		self.statusAct = QAction(QtGui.QIcon("Img/status.png"),"show statusBar", self)
		self.statusAct.setShortcut("Ctrl+B")
		self.statusAct.setStatusTip("show statusBar")
		self.statusAct.triggered.connect(self.status)
		self.actions.append(self.statusAct)

		#------Screen Action--------
		self.screenAct = QAction(QtGui.QIcon("Img/screen.png"),"Export to png", self)
		self.screenAct.setShortcut("Ctrl+Alt+S")
		self.screenAct.setStatusTip("Export to png")
		self.screenAct.triggered.connect(self.screenshot)
		self.actions.append(self.screenAct)

		#------AddState Action-----
		self.newstateAct = QAction(QtGui.QIcon("Img/state.png"),"New State", self)
		self.newstateAct.setCheckable(True)
		self.newstateAct.setShortcut("Ctrl+N")
		self.newstateAct.setStatusTip("New State")
		self.newstateAct.triggered.connect(self.newstate)
		self.actions.append(self.newstateAct)

		#------InitialState Action-----
		self.initialstateAct = QAction(QtGui.QIcon("Img/stateinitial.png"),"Set Initial State", self)
		self.initialstateAct.setShortcut("Ctrl+I")
		self.initialstateAct.setStatusTip("Set Initial State")
		self.initialstateAct.triggered.connect(self.initialstate)
		self.actions.append(self.initialstateAct)

		#------FinalState Action-----
		self.finalstateAct = QAction(QtGui.QIcon("Img/statefinal.png"),"Set Final State", self)
		self.finalstateAct.setShortcut("Ctrl+F")
		self.finalstateAct.setStatusTip("Set Final State")
		self.finalstateAct.triggered.connect(self.finalstate)
		self.actions.append(self.finalstateAct)

		#------Name State Action-----
		self.nameAct = QAction(QtGui.QIcon("Img/name.png"),"Set name", self)
		self.nameAct.setShortcut("Ctrl+Space")
		self.nameAct.setStatusTip("Set name")
		self.nameAct.triggered.connect(self.namestate)
		self.actions.append(self.nameAct)

		#------Radius State Action-----
		self.radiusAct = QAction(QtGui.QIcon("Img/radius.png"),"Set radius", self)
		self.radiusAct.setShortcut("Ctrl+R")
		self.radiusAct.setStatusTip("Set radius")
		self.radiusAct.triggered.connect(self.radiusstate)
		self.actions.append(self.radiusAct)

		#------AddTransition Action---
		self.transitionAct = QAction(QtGui.QIcon("Img/transition.png"),"New Transition", self)
		self.transitionAct.setCheckable(True)
		self.transitionAct.setShortcut("Ctrl+T")
		self.transitionAct.setStatusTip("New Transition")
		self.transitionAct.triggered.connect(self.newtransition)
		self.actions.append(self.transitionAct)

		#------Mozzia-----
		self.mozziaAct = QAction(QtGui.QIcon("Img/ia.png"),"Use IA", self)
		self.mozziaAct.setShortcut("Ctrl+Shift+I")
		self.mozziaAct.setStatusTip("Use IA")
		self.mozziaAct.triggered.connect(self.mozzia)
		self.actions.append(self.mozziaAct)

		#------Select All-----
		self.ctrlAAct = QAction("Select All", self)
		self.ctrlAAct.setShortcut("Ctrl+A")
		self.ctrlAAct.setStatusTip("Select All")
		self.ctrlAAct.triggered.connect(self.selectall)
		self.actions.append(self.ctrlAAct)

		#------Genetics -----
		self.geneticAct = QAction(QtGui.QIcon("Img/dna.png"),"Use genetic", self)
		self.geneticAct.setShortcut("Ctrl+G")
		self.geneticAct.setStatusTip("Use genetic")
		self.geneticAct.triggered.connect(self.genetic)
		self.actions.append(self.geneticAct)

		#------straight transition------
		self.straightAct = QAction(QtGui.QIcon("Img/align.png"),"Straight transitions", self)
		self.straightAct.setShortcut("Ctrl+Shift+!")
		self.straightAct.setStatusTip("Straight transitions")
		self.straightAct.triggered.connect(self.transitionsStraight)
		self.actions.append(self.straightAct)

		#-------- Menu Bar ------
		self.menu = self.menuBar()
		file = self.menu.addMenu("File")
		self.menu.addSeparator()
		edit = self.menu.addMenu("Edit")
		self.menu.addSeparator()
		view = self.menu.addMenu("View")
		self.menu.addSeparator()
		keybindings = self.menu.addMenu("Keybindings")

		file.addAction(self.exitAct)
		file.addAction(self.saveAct)
		file.addAction(self.openAct)
		file.addAction(self.latexAct)
		file.addAction(self.screenAct)

		edit.addAction(self.deleteAct)
		edit.addAction(self.copyAct)
		edit.addAction(self.pasteAct)
		edit.addAction(self.undoAct)
		edit.addAction(self.redoAct)
		edit.addAction(self.ctrlAAct)

		view.addAction(self.statusAct)
		view.addAction(self.formulaAct)


		keybindings.addAction(self.newstateAct)
		keybindings.addAction(self.transitionAct)
		keybindings.addAction(self.nameAct)
		keybindings.addAction(self.radiusAct)
		keybindings.addAction(self.geneticAct)
		keybindings.addAction(self.mozziaAct)
		keybindings.addAction(self.initialstateAct)
		keybindings.addAction(self.finalstateAct)
		keybindings.addAction(self.straightAct)

		#----------Main Tool bar-----------
		self.maintoolbar = self.addToolBar("MainToolbar")
		self.maintoolbar.addAction(self.exitAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.latexAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.screenAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.saveAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.openAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.copyAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.pasteAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.undoAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.redoAct)
		self.maintoolbar.addSeparator()
		self.maintoolbar.addAction(self.deleteAct)
		self.maintoolbar.setMovable(False)
		self.maintoolbar.setStyleSheet("background-color: rgb(250, 250, 250)")
		self.maintoolbar.setIconSize(QSize(self.toolbar_icon_size, self.toolbar_icon_size))


		#---------Status Bar ---------
		self.status = self.statusBar()

		#----------Drawing Toolbar---------
		self.drawtoolbar = QToolBar("Draw ToolBar")
		self.addToolBar(Qt.LeftToolBarArea, self.drawtoolbar)
		self.drawtoolbar.addAction(self.newstateAct)
		self.drawtoolbar.addSeparator()
		self.drawtoolbar.addAction(self.transitionAct)
		self.drawtoolbar.addSeparator()
		self.drawtoolbar.addAction(self.nameAct)
		self.drawtoolbar.addSeparator()
		self.drawtoolbar.addAction(self.radiusAct)
		self.drawtoolbar.addSeparator()
		self.drawtoolbar.addAction(self.mozziaAct)
		self.drawtoolbar.addSeparator()
		self.drawtoolbar.addAction(self.geneticAct)
		self.drawtoolbar.setMovable(False)
		self.drawtoolbar.setStyleSheet("background-color: rgb(250, 250, 250)")
		self.drawtoolbar.setIconSize(QSize(self.toolbar_icon_size, self.toolbar_icon_size))

		#--------Graphic scene & view--------
		self.scene = Scene(self)
		self.painter = QPainter()
		self.drawer = Drawer(self.scene, self.painter)
		self.view = myview(self.drawer)
		self.view.setScene(self.scene)
		self.painter.begin(self.view)
		self.view.setStyleSheet("background-color: rgb(250, 250, 250)")
		self.view.setDragMode(QGraphicsView.RubberBandDrag)
		self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
		self.setCentralWidget(self.view)
		self.view.setRenderHint(QPainter.Antialiasing)

		self.scene.selectionChanged.connect(self.actualize_enabled)
		#self.drawer.somth_changed.connect(self.something_happened)

		#--------Interactions with States--------
		self.setWindowTitle(self.title + " - " + self.drawer.label)

		self.show()

	#-------------SelectAll method------------
	##Select all items in the area
	def selectall(self):
		for item in self.scene.items():
			item.setSelected(True)

	#-------------Exit method------------
	##Leave the software properly
	def exit(self):
		message =QMessageBox.question(self,"Projet Automate","Do you really want to quit ?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if message == QMessageBox.Yes :
			self.refresh_tmp()
			shutil.rmtree(".tmp/.otmt/"+str(os.getpid())+"/")
			self.close()

	#-------------Save method------------
	##Save current the project
	def save(self):
		(file_path, file_format) = QFileDialog.getSaveFileName(self,'Save file', self.drawer.label+"."+self.drawer.manager.format_extension, self.drawer.manager.formats)

		if(file_path != ''):
			self.drawer.save(file_path, verbose=True)
			filename = file_path.split("/")
			filename = filename[len(filename)-1]
			filename = filename[0:len(filename)-len("."+self.drawer.manager.format_extension)] #without extension
			self.drawer.setLabel(filename)
			self.setWindowTitle(self.title + " - " + self.drawer.label)
			message = QMessageBox.about(self,"Projet Automate","Your project has been saved !")
			self.refresh_tmp()
			self.num_instance = 0
			self.num_instance_max=0

	#----------Open method-----------------
	##Open .otmt file and put it or add it to the current the project
	def open(self):
		ask = QMessageBox.question(self,"Projet Automate","Do you want to clear the actual project ?")
		if(ask==QMessageBox.Yes):
			self.drawer.clears()
			self.view.resetTransform()
			self.view.resetCachedContent()
		file_path, file_format = QFileDialog.getOpenFileName(self,'Open file', self.drawer.label+"."+self.drawer.manager.format_extension, self.drawer.manager.formats)

		if(file_path != ''):
			self.drawer.load(file_path)
			filename = file_path.split("/")
			filename = filename[len(filename)-1]
			filename = filename[0:len(filename)-len("."+self.drawer.manager.format_extension)] #without extension
			self.drawer.setLabel(filename)
			self.setWindowTitle(self.title + " - " + self.drawer.label)
			print(self.drawer)
			self.something_happened()

	##Take a screenshot of the current project and export it to png file
	def screenshot(self):
		self.scene.clearSelection()
		image = QImage(self.centralWidget().size(),QtGui.QImage.Format_ARGB32_Premultiplied)
		painter = QPainter()
		painter.begin(image)
		painter.eraseRect(self.centralWidget().rect())
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		self.centralWidget().render(painter)
		painter.end()
		(file_path, file_format) = QFileDialog.getSaveFileName(self,'Save file', self.drawer.label+'.png', ".png")
		if(file_path != ''):
			if(image.save(file_path, "PNG",100)):
				message = QMessageBox.about(self,self.drawer.label,"Screenshot saved")


	#----------Export LaTeX method---------
	##	latex()
	#	Export to TikZ (LaTeX) format a saved .otmt file
	#	Use a QFileDialog
	def latex(self):
		(file_path, file_format) = QFileDialog.getSaveFileName(self,'Export to LaTex', self.drawer.label+".tex", ".tex")

		if(file_path != ''):
			self.drawer.export(file_path)
			message = QMessageBox.about(self,"Projet Automate","Your project has been exported to LaTeX !")
		else:
			message = QMessageBox.about(self,"Projet Automate","You didn't provided a name !")

	#----------Copy method-----------------
	##Copy current selected items
	def copy(self):
		self.scene.copiedItems = []
		for item in self.scene.selectedItems():
			self.scene.copiedItems.append(item)
		self.scene.clearSelection()
		self.actualize_enabled()

	#----------Paste method-----------------
	##Paste current copied items
	def paste(self):
		states_pasted=dict()
		width = self.view.width
		height = self.view.height
		#Deal first with transitions
		for item in self.scene.copiedItems:
			if isinstance(item,Transition) and item.src in self.scene.copiedItems and item.dest in self.scene.copiedItems:
			#if transition.src and transition.dest are in copiedItems then add Transition
				for state in self.scene.copiedItems:
					if isinstance(state,State):
						if(item.src==state):
						#if item is my src
							if not(item.src.id in states_pasted.keys()):
							#if src not pasted yet, add State
								src = self.drawer.addState(preview=self.preview_flag, magnet=self.magnet)
								src.setLabel(item.src.getLabel())
								if(item.src.isfinal):
									src.setFinal()
								if(item.src.isinitial):
									src.setInitial()
								src.setRadius(item.src.getRadius())
								src.setPos(item.src.x()+width,item.src.y()+height)
								src.magnetized(self.magnet,width,height)
								src.setSelected(True)
								states_pasted[item.src.id]=src
							else:
							#else use already pasted one
								src = states_pasted[item.src.id]
						if(item.dest==state):
						#if item is my dest
							if not(item.dest.id in states_pasted.keys()):
							#if dest not pasted yet, add State
								dest = self.drawer.addState(preview=self.preview_flag, magnet=self.magnet)
								dest.setLabel(item.dest.getLabel())
								if(item.dest.isfinal):
									dest.setFinal()
								if(item.src.isinitial):
									dest.setInitial()
								dest.setRadius(item.dest.getRadius())
								dest.setPos(item.dest.x()+width,item.dest.y()+height)
								dest.magnetized(self.magnet,width,height)
								dest.setSelected(True)
								states_pasted[item.dest.id]=dest
							else:
							#else use already pasted one
								dest=states_pasted[item.dest.id]

				new_transition = self.drawer.addTransition(src, dest, preview=self.preview_flag)
				if(new_transition != None):
					new_transition.setLabel(item.getLabel())
					new_transition.setInflection_dy(item.getInflection_dy())
					new_transition.setInflection_dx(item.getInflection_dx())
					new_transition.setSelected(True)

		for state in self.scene.copiedItems:
			if isinstance(state,State) and (not(state.id in states_pasted.keys())):
				new_state = self.drawer.addState(preview=self.preview_flag, magnet=self.magnet)
				new_state.setLabel(state.getLabel())
				if(state.isfinal):
					new_state.setFinal()
				if(state.isinitial):
					new_state.setInitial()
				new_state.setRadius(state.getRadius())
				new_state.setPos(state.x()+width,state.y()+height)
				new_state.setSelected(True)
				new_state.magnetized(self.magnet,width,height)
		self.something_happened()


	#----------Insert Formula method-----------------
	##Insert a Formula
	def formula(self):
		if self.preview_flag:
			self.preview_flag = False
		else:
			self.preview_flag = True
		for item in self.scene.items():
			item.preview_flag = self.preview_flag
			item.setLabel(item.label)

	#----------Delete method-----------------
	##Delete selected items
	def delete(self):
		self.drawer.deleteSelected()
		self.view.resetTransform()
		self.view.resetCachedContent()
		self.something_happened()

	#----------Status method-----------------
	##Toggle visibility fo status bar
	def status(self):
		if self.status.isVisible():
			self.status.hide()
		else :
			self.status.show()
		self.something_happened()

	#-----------Add State method-----------------
	##Add state to the drawer
	def makenewstate(self,pos):
		self.drawer.addState(preview=self.preview_flag, magnet=self.magnet,pos=pos)
		if(self.magnet):#if magnetized
			self.magnetize()
		self.something_happened(stopStateMode=False, stopTransitionMode=False)

	##Manage the state creation
	def newstate(self):
		if self.newstateAct.isChecked():
			QApplication.setOverrideCursor(Qt.CrossCursor)
			self.newstateAct.setChecked(True)
			self.scene.setPressed(True)
			if self.transitionAct.isChecked() :
				QApplication.restoreOverrideCursor()
				self.scene.setSelectionModeTransition(False)
				self.transitionAct.setChecked(False)
				self.transitions_temp.clear()
				self.view.resetCachedContent()
		else:
			QApplication.restoreOverrideCursor()
			self.newstateAct.setChecked(False)
			self.scene.setPressed(False)


	#-----------Toggle Init State method-----------------
	##Toggle initial state of a state
	def initialstate(self):
		self.drawer.setInitialSelected()
		self.something_happened()

	#-----------Toggle Final State method-----------------
	##Toggle final state of a state
	def finalstate(self):
		self.drawer.setFinalSelected()
		self.something_happened()

	#-----------Create a straight transition between 2 states-----------------
	##Set a curved transition to straight
	def transitionsStraight(self):
		self.drawer.straightSelected()
		self.something_happened()

	#----------Name state method-----------------
	##Set name of a selected state
	def namestate(self):
		name = QInputDialog.getText(self,'Name Input','')
		self.drawer.setStateLabel(name[0])
		self.something_happened()

	#----------Radius state method-----------------
	##Set radius name of a selected state
	def radiusstate(self):
		value = QInputDialog.getInt(self,'Radius Input',"",50,0,800)
		if value[1]:
			self.drawer.setRadiusSelected(value[0])
			self.update()
		self.something_happened()


	#----------Show Grid method-----------------
	##Toggle visibility of grid
	def showgrid(self):
		self.grid = False if (self.grid) else True
		self.view.setGrid(self.grid)
		#self.gridAct.setChecked(self.grid)
		self.something_happened()

	#----------Magnetize_Changed method-----------------
	##Handle magnetization change of grid
	def magnetize_changed(self):
		if(self.magnet):
			self.magnet = False
		else:
			self.magnet = True
		self.something_happened()
		self.magnetize()

	#----------Magnetize Grid method-----------------
	##Toggle magnetization of grid
	def magnetize(self):
		width = self.view.width
		height = self.view.height
		for item in self.scene.items():
			if isinstance(item,State):
				item.magnetized(self.magnet,width,height)

	#----------Resize Grid method-----------------
	##Resize grid
	def resizeGrid(self):
		value = QInputDialog.getInt(self,'GridSize Input',"",self.view.width,0,800)
		if value[1]:
			self.view.width = value[0]
			self.view.height = value[0]
			self.update()
			self.magnetize()
		self.something_happened()


	#----------Add Transition method-----------------
	##Add transition between 2 states
	def newtransition(self):
		if self.newstateAct.isChecked():
			QApplication.restoreOverrideCursor()
			self.newstateAct.setChecked(False)
			self.scene.setPressed(False)
			self.view.resetCachedContent()
		transitioned = self.scene.selectedItems()
		if (len(transitioned) != 2 or type(transitioned[0])!=State or type(transitioned[1])!=State) and self.transitionAct.isChecked():
			self.scene.clearSelection()
			self.scene.setSelectionModeTransition(self.transitionAct.isChecked())
			QApplication.setOverrideCursor(Qt.CrossCursor)
			print(self.scene.getSelectionModeTransition())
		elif not self.transitionAct.isChecked():
			self.scene.setSelectionModeTransition(False)
			QApplication.restoreOverrideCursor()
			self.transitions_temp.clear()
		else :
			self.transitionAct.setChecked(False)
			message =QMessageBox.question(self,"Projet Automate","Do you want your transition to go from "+transitioned[0].getLabel()+" to "+transitioned[1].getLabel()+ " ?")
			if message == QMessageBox.Yes :
				self.drawer.addTransition(transitioned[0],transitioned[1],preview=self.preview_flag)
			else:
				self.drawer.addTransition(transitioned[1],transitioned[0],preview=self.preview_flag)
			self.something_happened()

	##Manage selected items when creating transition (press btn "create transition" then select first ans second state)
	def manage_transition_mode(self):
		transitioned = self.scene.selectedItems()
		if 3>len(transitioned)>0 and self.drawer.getNumberState()>=2 and isinstance(transitioned[0],State):
				self.transitions_temp.append(transitioned[0])
				if len(self.transitions_temp) >= 2:
					self.drawer.addTransition(self.transitions_temp[0],self.transitions_temp[1],preview=self.preview_flag)
					self.transitions_temp.clear()
					self.something_happened(stopTransitionMode=False, stopStateMode=False)
		self.scene.clearSelection()

	#----------Genetic Algorithm-------------
	##Automate position of current project with Genetic Algorithm
	def genetic(self):
		ask=QMessageBox.question(self,"Projet Automate","Do you want to use Genetic Algorithm ?")
		if ask==QMessageBox.No:
			return
		self.disable_all()
		if(self.preview_flag):
			self.formula()
			self.drawer.autoPosition()
			self.formula()
		else:
			self.drawer.autoPosition()
		self.enable_all()
		self.something_happened()

	#----------mozzia method-----------------
	##Automate position of current project with MozIA AI...
	def mozzia(self):
		self.something_happened()
		states_to_change=[]
		i=0
		for item in self.scene.selectedItems():
			if isinstance(item,State):
				if i<=6:
					states_to_change.append(item)
					i+=1
				else:
					message = QMessageBox.about(self,"Projet Automate","You must select at least 3 states and max 6 states")
					break
		if i>=3:
			self.disable_all()
			self.drawer.aiAlignStates(states_to_change)
			self.enable_all()
			self.something_happened()

	##Handle actions done, used for undo/redo
	def something_happened(self, stopTransitionMode=True, stopStateMode=True):
		#print("Something happened")
		self.num_instance +=1
		self.save_tmp(self.num_instance)
		if(self.num_instance_max < self.num_instance):
			self.num_instance_max = self.num_instance
		if stopTransitionMode == True :
			QApplication.restoreOverrideCursor()
			self.scene.setSelectionModeTransition(False)
			self.transitionAct.setChecked(False)
			self.transitions_temp.clear()
			self.view.resetCachedContent()
		if stopStateMode == True :
			QApplication.restoreOverrideCursor()
			self.newstateAct.setChecked(False)
			self.scene.setPressed(False)
			self.view.resetCachedContent()
		self.scene.update()
		self.update()
		self.actualize_enabled()

	## Enable or Disable functionnalities for a given state of App
	def actualize_enabled(self):
		self.magnetize()
		if(self.num_instance-1 <= 0):
			self.undoAct.setDisabled(True)
		else:
			self.undoAct.setEnabled(True)
		if(self.num_instance+1 > self.num_instance_max):
			self.redoAct.setDisabled(True)
		else:
			self.redoAct.setEnabled(True)

		if(len(self.scene.copiedItems)==0):
			self.pasteAct.setDisabled(True)
		else:
			self.pasteAct.setEnabled(True)

		if(len(self.drawer.states)==0):
			self.transitionAct.setDisabled(True)
		else:
			self.transitionAct.setEnabled(True)

		if(len(self.scene.selectedItems())==0):
			self.copyAct.setDisabled(True)
			self.deleteAct.setDisabled(True)
			self.radiusAct.setDisabled(True)
			self.nameAct.setDisabled(True)
			self.mozziaAct.setDisabled(True)

		elif(len(self.scene.selectedItems())>=1):
			self.copyAct.setEnabled(True)
			self.deleteAct.setEnabled(True)
			self.nameAct.setEnabled(True)
			if(len(self.scene.stateSelected())>=1):
				self.radiusAct.setEnabled(True)
			if(len(self.scene.stateSelected())>=3 and len(self.scene.stateSelected())<=6):
				self.mozziaAct.setEnabled(True)
			else:
				self.mozziaAct.setDisabled(True)

	## Disable all action
	def disable_all(self):
		for act in self.actions:
			act.setDisabled(True)

	## Enable all action
	def enable_all(self):
		for act in self.actions:
			act.setEnabled(True)
		self.actualize_enabled()

	##Ctrl+Z
	def undo(self):
		#print("CURRENT INSTANCE : ", self.num_instance)
		print("INSTANCE MAX : ", self.num_instance_max)
		self.num_instance -=1
		if(self.num_instance <= 0):
			self.num_instance = 0
			#print("CANNOT UNDO ALREADY AT 0")
			return
		#print("LOADING INSTANCE : ", self.num_instance)
		self.drawer.clears()
		self.view.resetTransform()
		self.view.resetCachedContent()
		self.open_tmp(self.num_instance)
		self.magnetize()
		self.actualize_enabled()

	##Ctrl+Y
	def redo(self):
		#print("CURRENT INSTANCE : ", self.num_instance)
		print("INSTANCE MAX : ", self.num_instance_max)
		self.num_instance +=1
		if(self.num_instance > self.num_instance_max):
			self.num_instance = self.num_instance_max
			#print("CANNOT LOAD ALREADY MAX")
			return
		#print("LOADING INSTANCE : ", self.num_instance)
		self.drawer.clears()
		self.view.resetTransform()
		self.view.resetCachedContent()
		self.open_tmp(self.num_instance)
		self.magnetize()
		self.actualize_enabled()


	#---- Save in tmp/.otmt ----
	##Save current project in a temporary file
	def save_tmp(self, number, verbose=False):
		(file_path, file_format) = (".tmp/.otmt/"+str(os.getpid())+"/"+str(number)+".otmt",".otmt")
		if(file_path != ''):
			self.drawer.save(file_path)

	#---- Load the last saved_tmp file ----
	##Open current project from a temporary file
	def open_tmp(self,number):
		(file_path, file_format) = (".tmp/.otmt/"+str(os.getpid())+"/"+str(number)+".otmt",".otmt")
		if(file_path != ''):
			self.scene.clears()
			self.view.resetTransform()
			self.view.resetCachedContent()
			self.drawer.load(file_path)
			self.view.scale(self.drawer.zoom,self.drawer.zoom)

	#---- Refresh tmp/.otmt ----
	##Refresh temporary files for undo/redo
	def refresh_tmp(self):
		shutil.rmtree(".tmp/.otmt/"+str(os.getpid())+"/")
		if not os.path.isdir(".tmp/.otmt/"+str(os.getpid())+"/"):
			os.makedirs(".tmp/.otmt/"+str(os.getpid())+"/")

	##Handle Keybindings
	def contextMenuEvent(self, event):
		#------ShowGrid Action-----
		self.gridAct = QAction("show grid", self)
		self.gridAct.setShortcut("Ctrl+G")
		self.gridAct.setStatusTip("Show Grid")
		self.gridAct.setCheckable(True)
		if(self.grid):
			self.gridAct.setChecked(True)
		else:
			self.gridAct.setChecked(False)
		self.gridAct.triggered.connect(self.showgrid)

		#------Magnetize Action-----
		self.magnetAct = QAction("magnetize", self)
		self.magnetAct.setShortcut("Ctrl+M")
		self.magnetAct.setStatusTip("Magnetize")
		self.magnetAct.setCheckable(True)
		if(self.magnet):
			self.magnetAct.setChecked(True)
		else:
			self.magnetAct.setChecked(False)
		self.magnetAct.triggered.connect(self.magnetize_changed)

		#------ResizeGrid Action-----
		self.resizeGridAct = QAction("resize grid", self)
		self.resizeGridAct.setShortcut("Ctrl+Shift+R")
		self.resizeGridAct.setStatusTip("Resize grid")
		self.resizeGridAct.triggered.connect(self.resizeGrid)

		cmenu = QMenu("view context menu", self)
		cmenu.addAction(self.gridAct)
		cmenu.addAction(self.magnetAct)
		cmenu.addAction(self.resizeGridAct)
		cmenu.addAction(self.formulaAct)
		cmenu.popup(self.mapToGlobal(event.pos()))

##A class to handle zoom feature
class myview(QGraphicsView):

	##Init zoom feature
	def __init__(self, Drawer, gridactivate = False):
		super().__init__()
		self.drawer = Drawer
		self.width = 100
		self.height = 100
		self.grid = gridactivate
		self.view_menu = QMenu(self)
		self.zoom=1
		self.getpress=False

	##Affiche la grille
	def drawBackground(self, painter, rect):
		if (self.grid):
			gr = rect.toRect()
			start_x = gr.left() + self.width - (gr.left() % self.width)
			start_y = gr.top() + self.height - (gr.top() % self.height)
			painter.save()
			painter.setPen(QtGui.QColor(60, 70, 80).lighter(90))
			painter.setOpacity(1.2)

			for x in range(start_x, gr.right(), self.width):
				painter.drawLine(x, gr.top(), x, gr.bottom())

			for y in range(start_y, gr.bottom(), self.height):
				painter.drawLine(gr.left(), y, gr.right(), y)
			painter.restore()
		self.update()

	#----------Zoom method-----------------
	##Handle Wheel event
	def wheelEvent(self, event):
		"""
		We can zoom in/ zoom out the GraphicsView by using wheelButton of the mouse.
		"""
		# Zoom Factor
		zoomInFactor = 1.1
		zoomOutFactor = 1 / zoomInFactor

		# Zoom
		if event.angleDelta().y() > 0:
			zoomFactor = zoomInFactor
		else:
			zoomFactor = zoomOutFactor
		factor = self.transform().scale(zoomFactor, zoomFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
		if factor < 0.15 or factor > 3:
			return
		self.scale( zoomFactor, zoomFactor )
		self.drawer.zoom *= zoomFactor

	##Set view of the grid
	def setGrid(self, gridactivate):
		self.grid = gridactivate
		self.update()

#---- create tmp dir if doesn't exists -----
if not os.path.isdir(".tmp/.otmt/"+str(os.getpid())+"/"):
	os.makedirs(".tmp/.otmt/"+str(os.getpid())+"/")

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())
