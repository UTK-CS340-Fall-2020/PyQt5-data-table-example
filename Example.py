import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtCore import *

table_after_close = []


class App(QWidget):

    def __init__(self, data):
        super().__init__()
        self.title = 'Data'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.settings = QSettings('My company', 'myApp')
        # Initial window size/pos last saved. Use default values for first time
        size = self.settings.value("size")
        pos = self.settings.value("pos")
        if size:
            self.width = size.width()
            self.height = size.height()
        if pos:
            self.left = int(pos[0])
            self.top = int(pos[1])
        self.init_ui(data)

    def init_ui(self, data):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_table(data)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def create_table(self, data):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setHorizontalHeaderLabels(['Tweet', 'Sentiment'])
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(cell))
        self.tableWidget.move(0, 0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def closeEvent(self, e):
        global table_after_close
        # save data
        for i in range(self.tableWidget.rowCount()):
            row = []
            for j in range(self.tableWidget.columnCount()):
                row.append(self.tableWidget.item(i, j).text())
            table_after_close.append(row)
        # Write window size and position to config file
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", [self.left, self.top])
        e.accept()
        print(table_after_close)
        # this altered data can be pushed back into your database or
        # wherever you pulled it from


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # the data can be pulled from wherever you like.
    # this app will display your data in an interactable table.
    # you can change the data by double clicking the cell and
    # typing in new data. table_after_close should have the new data.
    # double clicking also displays the data in the console's output
    # this is example data
    data = [('Tweet', 'Sentiment'),
            ("@GovPhilScott @VermontPBS This only helps Vermonters that can afford cable tv and/or internet.  What about those low income families that can not afford those services ? My husband now has no job, thanks to Covid-19. Unemployment checks are not arriving. just got a disconnect notice from Comcast....", "Negative"),
            ("@FredTJoseph @gofundme I’m single mom of two girls I’ve been laid off due to covid 19 I haven’t been able to pay rent or any utilities for April and we have no food in the house I have applied for food stamps and unemployment but a month later stand with nothing I need help $ChanelAriaMaliyah cashapp https://t.co/diRkoAt3yP", "Negative"),
            ("Stay #Home, Stay #Safe Ok then what about #Income because #rent,#light Bill, #Food, #medicine, #mobile Bill, #loan, Cable Bill, #internet Bill can't be paid without income right. #Lockdown4 #coronavirus #PMOfIndia #समय_रहते_पहचान_लो https://t.co/kfXrFYBsGk", "Positive")]
    ex = App(data=data)
    sys.exit(app.exec_())

