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
    checkInput,
    checkSelect,
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
        self.input_period.setText('')
        self.input_start_index.setText('0')
        self.input_token.setText('')

        code_all, code_6, message = getUNComtradeLen()
        self.label_value_code_all.setText(str(code_all))
        self.label_value_code_6.setText(str(code_6))
        if len(message) != 0:
            repaintText(self.text_message, message)

        self.input_period.setEnabled(True)
        self.input_start_index.setEnabled(True)
        self.input_token.setEnabled(True)
        self.select_reporter.setEnabled(True)
        self.select_partner.setEnabled(True)
        self.select_trade_flow.setEnabled(True)
        self.btn_update_code_list.setEnabled(True)
        self.btn_get_data.setEnabled(True)
        repaintText(self.text_message, 'Complete initial GUI ...\n')

    def bindFunc(self):
        self.btn_update_code_list.clicked.connect(self.btnUpdateCodeList)
        self.btn_get_data.clicked.connect(self.btnGetData)

    def btnUpdateCodeList(self):
        repaintText(self.text_message, 'Start update HS Code, please wait a minute ...')
        message = getUNCodeList()
        repaintText(self.text_message, message)
        code_all, code_6, message = getUNComtradeLen()
        self.label_value_code_all.setText(str(code_all))
        self.label_value_code_6.setText(str(code_6))
        repaintText(self.text_message, '{}\n'.format(message))

    def btnGetData(self):
        year = self.input_period.text()
        reporter = self.select_reporter.currentText()
        partner = self.select_partner.currentText()
        trade_flow = self.select_trade_flow.currentText()
        start_index = self.input_start_index.text()
        token = self.input_token.text()
        check_input, message_input = checkInput(PeriodYear=year, StartIndex=start_index, Token=token)
        check_select, message_select = checkSelect(Reporter=reporter, Partner=partner, TradeFlow=trade_flow)

        if check_input and check_select:
            repaintText(self.text_message, 'Start get data ...')
            params = getParams(year, start_index, token, reporter, partner, trade_flow)
            data = getData(params, start_index, self.text_message)
            print(data)
        else:
            repaintText(self.text_message, '{}{}'.format(message_input, message_select))


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
