import os
from math import sqrt, fabs, acos, pi, sin, cos, radians
from PyQt5.QtWidgets import QLabel, QGraphicsItem, QAction, QMenu
from PyQt5.QtCore import QPointF, QRectF, Qt, QLineF, QSizeF
from PyQt5.QtGui import QBrush, QPen, QColor, QPolygonF, QPainterPath, QPainterPathStroker, QImage
from sympy import preview

## Transition class
class Transition(QGraphicsItem):
	## initialize the transition
	## @param id
	## @param label the name of the Transition
	## @param color the color of the Transition
	## @param src the source State for the Transition
	## @param dest the destination State for the Transition
	## @param height the height of the Transition
	## @param preview the preview_flag of the Transition
	def __init__(self, id, label = "", color = (0, 0, 0), src = None, dest = None, height = 0, preview=False,dx=0,dy=0):
		super().__init__()
		"""ID must be specified"""
		self.id = id
		self.label = label
		self.color = color
		self.src = src
		self.dest = dest
		self.height = height

		#creates the image preview if not existing
		f = open('.tmp/.otmt/'+str(os.getpid())+'/t'+str(self.id)+'.png',"a+")
		f.close()
		self.preview_flag = preview

		self.shapePen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
		self.shapePen.setWidth(2)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setFlag(QGraphicsItem.ItemIsFocusable)
		self.setCursor(Qt.OpenHandCursor)
		self.arrowSize = 10.0

		self.inflection_dx = dx
		self.inflection_dy = dy
		self.inflection_point = QPointF(dx,dy)

		self.label_dx = 0
		self.label_dy = 0
		self.label_point = QPointF(dx,dy)

		self.positions = []
		self.have_positions()


	#CUSTOM QGRAPHICITEM
	## Returns the boundingRect of the Transition's Shape
	## Override QGraphicsItem.boundingRect(self)
	def boundingRect(self):
		self.have_positions()
		return self.shape().boundingRect()

	## Self-painting method
	## Override QGraphicsItem.paint(self, painter, option, widget)
	def paint(self, painter, option, widget):
		if self.isSelected():
			color=QColor(255,0,0)
			self.setColor((255,0,0))
		else:
			color=QColor(0,0,0)
			self.setColor((0,0,0))
		painter.setPen(self.shapePen)
		painter.setPen(QColor(self.color[0],self.color[1],self.color[2]))
		self.have_positions()
		line=QLineF(self.inflection_point, self.positions[1])
		if line.length()==0:
			angle=0
		else:
			angle = acos(line.dx() / line.length())
		if line.dy() >= 0:
			angle = pi * 2 - angle
		mid_x = self.positions[2].x()+self.inflection_dx/2
		mid_y = self.positions[2].y()+self.inflection_dy/2
		diff=sqrt(-1+1/(cos(angle)**2))
		if (diff>1):
			diff = 1
		if (cos(angle)*sin(angle) > 0):
			mid = QPointF(mid_x-10*diff-len(self.label)*5,mid_y-10)
		else:
			mid = QPointF(mid_x+10*diff,mid_y-10)

		if(self.preview_flag and len(self.label)>0):
			painter.drawImage(mid, self.prev_image)
		else :
			painter.drawText(mid,self.label)
		painter.pen().setWidth(2)
		brush = QBrush(color)
		painter.setBrush(brush)
		painter.drawPath(self.paths[0])

		brush = QBrush(Qt.transparent)
		painter.pen().setColor(Qt.white)
		painter.setBrush(brush)

		#Drawing the arrow
		#line=QLineF(self.inflection_point, self.positions[1]) --> Duplicata
		#angle = acos(line.dx() / line.length())

		#if line.dy() >= 0:
		#	angle = pi * 2 - angle
		destArrowP1 = self.positions[1] + QPointF(sin(angle - pi / 3) * self.arrowSize,
													cos(angle - pi / 3) * self.arrowSize)
		destArrowP2 = self.positions[1] + QPointF(sin(angle - pi + pi / 3) * self.arrowSize,
													cos(angle - pi + pi / 3) * self.arrowSize)
		painter.setBrush(Qt.black)
		painter.drawPolygon(QPolygonF([line.p2(), destArrowP1, destArrowP2]))
		self.update()


	#COORDONATES OF POINTS
	## Returns the positions of the points needed to paint the Transition
	def have_positions(self):
		if (self.src==None or self.dest == None):
			return

		abx = self.dest.pos().x() - self.src.pos().x()
		aby = self.dest.pos().y() - self.src.pos().y()
		self.height = sqrt(abx*abx + aby*aby)

		alpha = radians(QLineF(self.src.pos(), self.inflection_point).angle())
		beta = radians(QLineF(self.dest.pos(), self.inflection_point).angle())

		#if selfTransition
		if (self.src == self.dest):
			if(self.inflection_dx==0):
				self.inflection_dx += 100
			if(self.inflection_dy==0):
				self.inflection_dy -= 100
			alpha+=pi/8
			beta-=pi/8

		src_x = self.src.x() + self.src.radius * cos(alpha)
		src_y = self.src.y() - self.src.radius * sin(alpha)
		src = QPointF(src_x, src_y)

		dest_x = self.dest.x() + self.dest.radius * cos(beta)
		dest_y = self.dest.y() - self.dest.radius * sin(beta)
		dest = QPointF(dest_x,dest_y)

		len_x = dest_x - src_x
		len_y = dest_y -src_y
		self.dist =  sqrt(len_x*len_x + len_y*len_y)

		mid_x = (self.src.x()+self.dest.x())/2
		mid_y = (self.src.y()+self.dest.y())/2
		mid = QPointF(mid_x, mid_y)

		self.positions = [src, dest, mid]


		self.inflection_point.setX(mid.x() + self.inflection_dx)
		self.inflection_point.setY(mid.y() + self.inflection_dy)
		self.label_point.setX(mid.x() + self.label_dx)
		self.label_point.setY(mid.y() + self.label_dy)

	## Returns a QPainterPath to draw the Transition
	def shape(self):
		self.have_positions()
		path = QPainterPath()
		path.moveTo(self.positions[0])
		path.quadTo(self.inflection_point, self.positions[1])
		pathStroker = QPainterPathStroker()
		pathStroker.setWidth(self.shapePen.width())
		self.length=path.length()
		path1 = pathStroker.createStroke(path)
		pathStroker.setWidth(self.shapePen.width()+20)
		path2 = pathStroker.createStroke(path)
		self.paths = (path1,path2)
		return path2

	#SETTERS
	## Sets the label
	## @param label
	def setLabel(self, label=""):
		self.label = label
		if(self.preview_flag and len(self.label)>0):
			preview('$'+self.label+'$',viewer='file',filename=".tmp/.otmt/"+str(os.getpid())+"/t"+str(self.id)+'.png')
			self.prev_image=QImage(".tmp/.otmt/"+str(os.getpid())+"/t"+str(self.id)+'.png')

	## Sets the color
	## @param color
	def setColor(self, color=(0, 0, 0)):
		self.color = color

	## Sets the height
	## @param height
	def setHeight(self, height=0):
		self.height = height

	## Sets the src State
	## @param src
	def setSrc(self, state=None, inscription=True):
		self.src = state
		if state != None and inscription:
			self.src.addTransition(self)
		self.update()

	## Sets the dest State
	## @param dest
	def setDest(self, state=None, inscription=True):
		self.dest = state
		if state != None and inscription:
			self.dest.addTransition(self)
		self.update()

	## Sets the InflectionPoint of the Transition
	## @param x
	## @param y
	def setInflectionPoint(self, x, y):
		self.inflection_dx=x
		self.inflection_dy=y

    ## Sets the inflection_dx of the Transition
	## @param dx
	def setInflection_dx(self, dx):
		self.inflection_dx = dx

	## Sets the inflection_dy of the Transition
	## @param dy
	def setInflection_dy(self, dy):
		self.inflection_dy = dy

	## Sets the Transition to be a perfect line
	def setStraight(self):
		self.setInflection_dx(0)
		self.setInflection_dy(0)

	#GETTERS

	## Returns the InflectionPoint of the Transition
	def getInflectionPoint(self):
		"""Returns (x,y)"""
		return(self.inflection_dx,self.inflection_dy)

	## Returns the id of the Transition
	def getId(self):
		return self.id

	## Returns the label (name) of the Transition
	def getLabel(self):
		return self.label

	## Returns the color of the Transition
	def getColor(self):
		return self.color

	## Returns the height of the Transition
	def getHeight(self):
		return self.height

	## Returns the src of the Transition
	def getSrc(self):
		return self.src

	## Returns the dest of the Transition
	def getDest(self):
		return self.dest

	## Returns the inflection_dx of the Transition
	def getInflection_dx(self):
		return self.inflection_dx

	## Returns the inflection_dy of the Transition
	def getInflection_dy(self):
		return self.inflection_dy

	## Returns the length (length of the line) of the Transition
	def getLength(self):
		return self.length

	## Prints all informations of the Transition
	def showInfos(self):
		print("id : "+str(self.id))
		print("label : "+str(self.label))
		print("color : "+str(self.color))
		print("source : id = "+str(self.src.id))
		#self.src.showInfos()
		print("dest : id = "+str(self.dest.id))
		#self.dest.showInfos()
		print("height : "+str(self.height))

	## Binds mouseMoveEvent to curving the Transition
	def mouseMoveEvent(self,event):
		self.inflection_dx += event.screenPos().x() - event.lastScreenPos().x()
		self.inflection_dy += event.screenPos().y() - event.lastScreenPos().y()
		self.update()

	## Displays a contextMenu to set straight the Transition
	def contextMenuEvent(self, event):
		self.straightAct = QAction("straight")
		self.straightAct.setCheckable(True)
		self.straightAct.triggered.connect(self.setStraight)

		cmenu = QMenu("transition context menu")
		cmenu.addAction(self.straightAct)
		#action = cmenu.exec_(self.mapToGlobal(event.pos()))
		cmenu.exec_(event.screenPos())
