from PyQt5.QtGui import QBrush, QPen, QColor, QPolygonF, QImage
from PyQt5.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QMenu, QAction
from PyQt5.QtCore import QPointF, QRectF, Qt, QLineF
import random, math, os
from sympy import preview

#@note This will have an indented section on its page, nice for method notes and limitations
#@bug Doxygen creates a separate bugs page, very nice for notes-to-self-to-fix-this
#@todo Similar, only to-do instead of a bug
#@author, @date - Put these in the header of the file
#@brief Short description of what the file/method/subroutine does
#@filename Put this in the header of the file - note that case must match the actual filename
#@param [param name] Use this to document parameters to a function
#@retval Use this to document the return value of a function

## This is the class dedicated for the states
class State(QGraphicsItem):
	"""A class for managing States."""
	##Initialise the state
	##@param id State's ID
	##@param label State's label
	##@param radius State's radius
	##@param color The color of the state's edge
	##@param background_color The background color of the state
	##@param contour TODO - Unused
	##@param preview LaTex's previsualisation flag
	##@param magnet Bound or unbound the state to the grid
	##@param postion Where to put the when we create it
	def __init__(self, id = 0, label = "", radius = 50, color = (0, 0, 0), background_color = (255, 255, 255), contour = "simple", preview=False, magnet=False, pos=QPointF(0,0)):
		super().__init__()
		self.id = id
		self.transitions = []

		#creates the image preview if not existing
		f = open('.tmp/.otmt/'+str(os.getpid())+'/s'+str(self.id)+'.png',"a+")
		f.close()
		self.preview_flag = preview
		self.prev_image=QImage('.tmp/.otmt/s'+str(self.id)+'.png')

		self.magnet_flag = magnet
		self.magnet_width = 10
		self.magnet_height = 10


		self.label=label
		self.radius = radius
		self.color = color
		self.background_color = background_color
		self.contour = contour
		self.rect = self.boundingRect()
		self.backgroundBrush = QBrush(QColor(self.background_color[0], self.background_color[1], self.background_color[2]))
		self.shapePen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
		self.shapePen.setWidth(10)
		self.isinitial = False
		self.isfinal = False
		self.manualysized = True
		self.setPosition(random.randrange(10, 50), random.randrange(10, 50))
		self.setFlag(QGraphicsItem.ItemIsMovable)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setFlag(QGraphicsItem.ItemIsFocusable)
		self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
		self.setEnabled(QGraphicsItem.ItemPositionHasChanged)
		self.setCursor(Qt.OpenHandCursor)
		self.setSelected(False)
		self.angleinitial = math.pi/4

		self.finalAct = QAction("final")
		self.finalAct.setCheckable(True)
		self.finalAct.triggered.connect(self.setFinal)

		self.initialAct = QAction("initial")
		self.initialAct.setCheckable(True)
		self.initialAct.triggered.connect(self.setInitial)

		self.setPosition(pos.x(),pos.y())

	#CUSTOM QGRAPHICITEM
	def boundingRect(self):
		return QRectF(-self.radius, -self.radius, self.radius*2, self.radius*2)

	##A state is born
	##@param painter A tool to draw the state
	##@param option State's style option
	##@param widget
	def paint(self, painter, option, widget):
		if self.isSelected():
			self.setColor((255,0,0))
		else:
			self.setColor()
		self.shapePen.setWidth(4)
		painter.setPen(self.shapePen)
		painter.setBrush(self.backgroundBrush)
		point = QPointF(0,0)
		painter.drawEllipse(point, self.radius, self.radius)

		if self.isfinal :
			painter.drawEllipse(point, self.radius -5, self.radius -5)
		if(self.preview_flag and len(self.label)>0):
			width = self.prev_image.rect().width()
			centered = QRectF(self.prev_image.rect().x()-self.prev_image.rect().width()/2, self.prev_image.rect().y()-self.prev_image.rect().height()/2, self.prev_image.rect().width(), self.prev_image.rect().height())
			painter.drawImage(centered,self.prev_image)
		else:
			width = painter.drawText(self.boundingRect(), Qt.AlignCenter ,self.label).width()

		if self.isinitial:
			self.initialPoint = QPointF(-self.radius*math.cos(self.angleinitial), -self.radius*math.sin(self.angleinitial))
			arrowSize = 8.0
			destArrowP1 = self.initialPoint + QPointF(math.sin(-self.angleinitial - math.pi / 3) * arrowSize,
														math.cos(-self.angleinitial - math.pi / 3) * arrowSize)
			destArrowP2 = self.initialPoint + QPointF(math.sin(-self.angleinitial - math.pi + math.pi / 3) * arrowSize,
														math.cos(-self.angleinitial - math.pi + math.pi / 3) * arrowSize)
			painter.setBrush(Qt.black)
			painter.drawPolygon(QPolygonF([self.initialPoint, destArrowP1, destArrowP2 ]))
			painter.drawLine(self.initialPoint, self.initialPoint - QPointF(25*math.cos(self.angleinitial),25*math.sin(self.angleinitial)))
		if self.manualysized == False :
			self.setRadius(width/2 + 20)
		for t in self.transitions :
			t.update()

	##Change the transition correspond to new state's position
	def itemChange(self, change, value):
		for t in self.transitions :
			t.update()
		if change == QGraphicsItem.ItemPositionHasChanged:
			#self.scene.something_happened()
			self.setPos(value)
		return super(State, self).itemChange(change, value)

	##
	##@param magnet
	##@param width
	##@param height
	def magnetized(self, magnet, width, height):
		# print("MAGNET OF STATE ",self.id," : ",magnet)
		self.magnet_flag = magnet
		self.magnet_width = width
		self.magnet_height = height

		if(self.magnet_flag):
			x=round(self.x()/self.magnet_width,0)*self.magnet_width
			y=round(self.y()/self.magnet_height,0)*self.magnet_height
			self.setPos(QPointF(x,y))


	# def preview_formulas(self):
	# 	if(self.preview_flag):
	# 		self.preview_flag = False
	# 	else:
	# 		self.preview_flag = True

	##How far do I have to go to go to you?
	##@param st the state we need to calculate the distance to
	##@return the distance, obviously.
	def distanceTo(self,st):
		dx=st.getPosition().x()-self.x()
		dy=st.getPosition().y()-self.y()
		return math.sqrt(dx*dx+dy*dy)

	#SETTERS
	##Modify the state's label
	##@param label state's new label
	def setLabel(self, label=""):
		self.label = label
		self.manualysized = False
		if(self.preview_flag and len(self.label)>0):
			preview('$'+self.label+'$',viewer='file',filename=".tmp/.otmt/"+str(os.getpid())+"/s"+str(self.id)+'.png')
			self.prev_image=QImage(".tmp/.otmt/"+str(os.getpid())+"/s"+str(self.id)+'.png')

		self.update()

	##Modify the state's radius
	##@param radius new state's radius
	def setRadius(self, radius=50):
		self.radius = radius
		self.manualysized = True
		self.update()

	##Modify the state's position
	##@param position new state's position
	def setPosition(self, x,y):
		#self.pos = QPointF(position[0], position[1])
		#self.rect = QRectF(self.pos().x(), self.pos().y(), self.radius, self.radius)
		#self.move(self.pos().x()+position[0], self.pos().y()+position[1])
		self.setPos(x, y)
		for t in self.transitions :
			t.update()

	##Modify the state's color
	##@param color new state's color
	def setColor(self, color=(0, 0, 0)):
		self.color = color
		self.shapePen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
		self.shapePen.setWidth(1.80)

	##Modify the state's background color
	##@param color new state's background color
	def setBackgroundColor(self, color=(0, 0, 0)):
		self.background_color = color
		self.backgroundBrush = QBrush(QColor(self.background_color[0], self.background_color[1], self.background_color[2]))

	##TODO - Unused
	##@param contour new state's contour
	def setContour(self, contour="simple"):
		self.contour = contour

	##Change the type of state to intial state
	def setInitial(self):
		if self.isinitial :
			self.isinitial = False
			self.initialAct.setChecked(False)
		else :
			self.isinitial = True
			self.initialAct.setChecked(True)
		self.update()

	##Change the type of state to final state
	def setFinal(self):
		if self.isfinal :
			self.isfinal = False
			self.finalAct.setChecked(False)
		else :
			self.isfinal = True
			self.finalAct.setChecked(True)
		self.update()

	##Delete all the transition associated to this state
	def removeTransition(self, t):
		if t in self.transitions:
			self.transitions.remove(t)

	#GETTERS
	##We may need to ask for the state's label?
	##@return the state's label
	def getLabel(self):
		return self.label

	##How big is the state?
	##@return the state's radius
	def getRadius(self):
		return self.radius

	##Where is the state's current position?
	##@return the state's current position, duh
	def getPosition(self):
		return self.pos()

	##I am colorblind, I cannot see the color of the state's edge
	##@return the color of state's edge
	def getColor(self):
		return self.color

	##Like I said, I am colorblind! How can I know the color of the background color without this methode?
	##@return the color of state's background
	def getBackgroundColor(self):
		return self.background_color

	##TODO - Unused
	##@return the state's contour
	def getContour(self):
		return self.contour

	##Is this state a final state?
	##@return a boolean to show if the state is final or not
	def getFinal(self):
		return self.isfinal

	##Is the state's size is set mannually?
	##@return a boolean to show if the state is set mannually or not
	def getManualySized(self):
		return self.manualysized

	def getId(self):
		return self.id

	##We want to have a menu to check on when we decide the state
	##@param event happen when you check on a box.
	def contextMenuEvent(self, event):
		cmenu = QMenu("state context menu")
		cmenu.addAction(self.finalAct)
		cmenu.addAction(self.initialAct)
		#action = cmenu.exec_(self.mapToGlobal(event.pos()))
		cmenu.exec_(event.screenPos())

	##What is a state good for if we don't have access to its transitions?
	##@return list of transition associated to the state
	def getTransitions(self):
		return self.transitions

	#TOOLS

	##Now I want to know all about this state
	def showInfos(self):
		print("id : " + str(self.id))
		print("label : " + str(self.label))
		print("radius : " + str(self.radius))
		print("position : " + str(self.pos()))
		print("color : " + str(self.color))
		print("background_color : " + str(self.background_color))
		print("contour : " + str(self.contour))
		print("transitions len : "+str(len(self.transitions)))
		for transition in self.transitions:
			transition.showInfos()

	##I want to change the position of initial state's arrow
	##@param event happen when you press a direction key
	def keyPressEvent(self, event):
		#print("KeyPressed")
		if(event.key() == Qt.Key_Up):
			#print("Up")
			self.angleinitial += math.pi/12
		if(event.key() == Qt.Key_Down):
			#print("Down")
			self.angleinitial += -math.pi/12
		if(event.key() == Qt.Key_Left):
			#print("Left")
			self.angleinitial += -math.pi/12
		if(event.key() == Qt.Key_Right):
			#print("Right")
			self.angleinitial += math.pi/12
		self.update()

	##Release the mouse click lead to magnetize the state if the magnetized flag is up.
	##@param event happen when you release the mouse click.
	def mouseReleaseEvent(self,event):
		if(self.magnet_flag):
			x=round(self.x()/self.magnet_width,0)*self.magnet_width
			y=round(self.y()/self.magnet_height,0)*self.magnet_height
			self.setPos(QPointF(x,y))
		super().mouseReleaseEvent(event)

        ## add a Transition to the state.transitions list
	def addTransition(self, trans):
		if trans not in self.transitions:
			self.transitions.append(trans)
