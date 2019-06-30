Welcome to project OTomateMozarella. Requirements can be found at the end of this document.

PyQt5 classes documentation : http://pyqt.sourceforge.net/Docs/PyQt4/classes.html


TODO :
- Genetic Algorithm:
	- Score calculation need improvements

ISSUES/BUGS:
- Delete is still broken, but works about 95% of the time. I don't know how to fix it.
- Genetic Algorithm:
	- Crash when you use it too many times. Maybe a problem with reset
- pasted elements are not magnetized (only destination states, but it works when you deselect)
- The initial state arrow position is not saved
- The Radius is not exported to LaTeX

REQUIREMENTS:

- Basics :
	- Python 3
	- PyQT5
	- sympy : on arch linux : pacman -S texlive-most
	- LaTex compiler
	- Not sure if it's bundled with python but numPy is used for random sampling purposes.

- Used by the AI :
	- matplotlib
	- keras ?
	- tensorflow (available for Windows, MacOs and Ubuntu with pip)
/!\ For arch linux -> install package python-tensorflow with pacman /!\
# AutomataCreator
# AutomataCreator
