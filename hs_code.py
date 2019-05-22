import sys
import os
import pickle
from PyQt5 import QtWidgets, QtCore
from main import Ui_MainWindow
from utils import (
    repaintText,
    getUNCodeList,
    getUNComtradeLen,
    getData,
    getParams,
    dataToExcel,
    checkInput,
    checkSelect,
    checkIndex,
)


class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)

        self.initGUI()
        self.bindFunc()

    def initGUI(self):
        self.text_message.setText('')
        repaintText(self.text_message, 'Start initial GUI ...')
        self.label_value_code_all.setText('')
        self.label_value_code_6.setText('')
        self.tab02_input_period.setText('')
        self.tab10_input_start_index.setText('0')
        self.tab11_input_end_index.setText('0')
        self.tab01_input_token.setText('')

        code_all, code_6, message = getUNComtradeLen()
        self.label_value_code_all.setText(str(code_all))
        self.label_value_code_6.setText(str(code_6))
        if len(message) != 0:
            repaintText(self.text_message, message)

        self.tab01_input_token.setEnabled(True)
        self.tab02_input_period.setEnabled(True)
        self.tab10_input_start_index.setEnabled(True)
        self.tab11_input_end_index.setEnabled(True)
        self.tab03_select_reporter.setEnabled(True)
        self.tab04_select_partner.setEnabled(True)
        self.tab05_select_trade_flow.setEnabled(True)
        self.btn_update_code_list.setEnabled(True)
        self.btn_get_data.setEnabled(True)
        self.tab01_input_token.setFocus(True)

        repaintText(self.text_message, 'Complete initial GUI ...\n')

    def bindFunc(self):
        self.btn_update_code_list.clicked.connect(self.btnUpdateCodeList)
        self.btn_get_data.clicked.connect(self.btnGetData)
        self.tab08_radio_code_all.clicked.connect(self.radioSelectAll)
        self.tab09_radio_code_6.clicked.connect(self.radioSelect6)

    def btnUpdateCodeList(self):
        repaintText(self.text_message, 'Start update HS Code, please wait a minute ...')
        message = getUNCodeList()
        repaintText(self.text_message, message)
        code_all, code_6, message = getUNComtradeLen()
        self.label_value_code_all.setText(str(code_all))
        self.label_value_code_6.setText(str(code_6))
        repaintText(self.text_message, '{}\n'.format(message))

    def btnGetData(self):
        radio = self.getRadio()
        year = self.tab02_input_period.text()
        reporter = self.tab03_select_reporter.currentText()
        partner = self.tab04_select_partner.currentText()
        trade_flow = self.tab05_select_trade_flow.currentText()
        start_index = self.tab10_input_start_index.text()
        end_index = self.tab11_input_end_index.text()
        token = self.tab01_input_token.text()
        check_input, message_input = checkInput(PeriodYear=year, StartIndex=start_index, EndIndex=end_index, Token=token)
        check_select, message_select = checkSelect(Reporter=reporter, Partner=partner, TradeFlow=trade_flow)
        check_index, message_index = checkIndex(start_index, end_index)

        if check_input and check_select and check_index:
            repaintText(self.text_message, 'Start get data ...')
            params = getParams(year, token, reporter, partner, trade_flow)
            data = getData(radio, params, start_index, end_index, self.text_message)
            message = dataToExcel(data)
            repaintText(self.text_message, message)
        else:
            repaintText(self.text_message, '{}{}{}'.format(message_input, message_select, message_index))

    def radioSelectAll(self):
        self.tab09_radio_code_6.setChecked(False)
        self.tab08_radio_code_all.setChecked(True)

    def radioSelect6(self):
        self.tab08_radio_code_all.setChecked(False)
        self.tab09_radio_code_6.setChecked(True)

    def getRadio(self):
        if self.tab08_radio_code_all.isChecked():
            return 'code_all.pkl'
        if self.tab09_radio_code_6.isChecked():
            return 'code_6.pkl'
        return None


class InitialMainWindow:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        InitialMainWindow.MainWindow = Main()
        InitialMainWindow.MainWindow.show()
        sys.exit(app.exec_())


def main():
    program = InitialMainWindow()


def initFile():
    if not os.path.isfile('code_all.pkl'):
        code_all = dict()
        f = open('code_all.pkl', 'wb')
        pickle.dump(code_all, f)
    if not os.path.isfile('code_6.pkl'):
        code_6 = dict()
        f = open('code_6.pkl', 'wb')
        pickle.dump(code_6, f)


if __name__ == '__main__':
    initFile()
    main()
