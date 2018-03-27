import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class FilteringComboBox(QComboBox):
    def __init__(self, parent=None, **kwargs):
        QComboBox.__init__(self, parent, editable=True, focusPolicy=Qt.StrongFocus, **kwargs)

        self._proxy = QSortFilterProxyModel(self, filterCaseSensitivity=Qt.CaseInsensitive)
        self._proxy.setSourceModel(self.model())

        self._completer = QCompleter(self._proxy, self, activated=self.onCompleterActivated)

        self._completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self._completer)

        self.lineEdit().textEdited.connect(self._proxy.setFilterFixedString)

    @pyqtSlot(str)
    def onCompleterActivated(self, text):
        if not text: return
        self.setCurrentIndex(self.findText(text))
        self.activated[str].emit(self.currentText())