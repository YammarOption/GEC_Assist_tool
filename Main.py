from configparser import ConfigParser
from PyQt5.QtWidgets import (QApplication, QErrorMessage)
from GEC_Tool_Stream import GECStreamWindow
from GEC_Tool import GECRegularWindow
app = QApplication([])


if not __name__ == "__main__":
    exit()

config = ConfigParser()
config.read("Config.ini")
gen = config.get("GENERALE","Gen")
windowtype = config.get("GENERALE","Window_type")

window = None
if windowtype.lower() == "stream":
    window = GECStreamWindow()
elif windowtype.lower() == "scroll":
    window = GECRegularWindow()

if not  window:
    error = QErrorMessage()
    error.showMessage("Errore: tipo finestra non riconosciuta. i valori accettati sono 'Scroll' o 'Stream'")
    app.exec()
    exit()
window.setup(config)
window.show()
window.extraWindow.show()
app.exec()