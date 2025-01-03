
from configparser import ConfigParser
from PyQt5.QtWidgets import (QApplication, QErrorMessage)
from src.QT_classes.GEC_Tool import GECRegularWindow
from src.QT_classes.GEC_Tool_Stream import GECStreamWindow
from src.Game import GameFactory
app = QApplication([])


if not __name__ == "__main__":
    exit()

config = ConfigParser()
config.read("Config.ini")
gen = config.get("GENERAL","Gen")
windowtype = config.get("GENERAL","Window_type")

window = None
factory=GameFactory()
gameClass = factory.getGame(gen)
if not gameClass:
    error = QErrorMessage()
    error.showMessage("Error: unrecognized game type")
    app.exec()
    exit()
    
if windowtype.lower() == "stream":
    window = GECStreamWindow(gameClass)
elif windowtype.lower() == "scroll":
    window = GECRegularWindow(gameClass)

if not  window:
    error = QErrorMessage()
    error.showMessage("Error: window type not recognized. accepted values are 'Scroll' or 'Stream'")
    app.exec()
    exit()
window.setup(config)
window.show()
window.extraWindow.show()
app.exec()