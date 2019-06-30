from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QGraphicsView

## Class myview : allow us to override functions from QGraphicsView, for zoom, background and grid.
class myview(QGraphicsView):
    def __init__(self, Drawer, gridactivate = False): #initialisation function
        super().__init__()
        self.drawer = Drawer
        self.width = 100
        self.height = 100
        self.grid = gridactivate
        self.view_menu = QMenu(self)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.zoom=1
	## Draws he grid
    def drawBackground(self, painter, rect):
        if (self.grid):
            gr = rect.toRect()
            start_x = gr.left() + self.width - (gr.left() % self.width)
            start_y = gr.top() + self.height - (gr.top() % self.height)
            painter.save()
            painter.setPen(QColor(60, 70, 80).lighter(90))
            painter.setOpacity(1.2)

            for x in range(start_x, gr.right(), self.width):
                painter.drawLine(x, gr.top(), x, gr.bottom())

            for y in range(start_y, gr.bottom(), self.height):
                painter.drawLine(gr.left(), y, gr.right(), y)
            painter.restore()
        self.update()

    #----------Zoom method-----------------
	## Manage the mouse wheel
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
        factor = self.transform().scale(zoomFactor, zoomFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.15:
            return
        self.scale( zoomFactor, zoomFactor )
        self.drawer.zoom *= zoomFactor
		
	## Toogle the grid
    def setGrid(self, gridactivate):
        self.grid = gridactivate
        self.update()
