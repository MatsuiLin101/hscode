import sys
import os
import pickle
from PyQt5 import QtWidgets, QtCore
from main import Ui_MainWindow
from utils import (
    repaintText,
    checkMonthCount,
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
        self.tab12_input_start_index.setText('0')
        self.tab13_input_end_index.setText('0')
        self.tab14_input_start_hs.setText('0')
        self.tab15_input_end_hs.setText('0')
        # self.tab01_input_token.setText('')

        code_all, code_6, message = getUNComtradeLen()
        self.label_value_code_all.setText(str(code_all))
        self.label_value_code_6.setText(str(code_6))
        if len(message) != 0:
            repaintText(self.text_message, message)

        # self.tab01_input_token.setEnabled(True)
        self.tab02_input_period.setEnabled(True)
        self.tab12_input_start_index.setEnabled(True)
        self.tab13_input_end_index.setEnabled(True)
        self.tab14_input_start_hs.setEnabled(True)
        self.tab15_input_end_hs.setEnabled(True)
        self.tab03_select_reporter.setEnabled(True)
        self.tab04_select_partner.setEnabled(True)
        self.tab05_select_trade_flow.setEnabled(True)
        self.btn_update_code_list.setEnabled(True)
        self.btn_get_data.setEnabled(True)
        self.tab02_input_period.setFocus(True)

        repaintText(self.text_message, 'Complete initial GUI ...\n')

    def bindFunc(self):
        self.btn_update_code_list.clicked.connect(self.btnUpdateCodeList)
        self.btn_get_data.clicked.connect(self.btnGetData)
        self.tab08_radio_freq_year.clicked.connect(self.radioFreqYear)
        self.tab09_radio_freq_month.clicked.connect(self.radioFreqMonth)
        self.check_all.clicked.connect(self.checkAll)

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
        start_index = self.tab12_input_start_index.text()
        end_index = self.tab13_input_end_index.text()
        # token = self.tab01_input_token.text()
        check_input, message_input = checkInput(PeriodYear=year, StartIndex=start_index, EndIndex=end_index, Token='token')
        check_select, message_select = checkSelect(Reporter=reporter, Partner=partner, TradeFlow=trade_flow)
        check_index, message_index = checkIndex(start_index, end_index)
        if self.tab09_radio_freq_month.isChecked() and not self.check_all.isChecked():
            check_month, message_month = self.checkMonth()
        else:
            check_month = True
            message_month = ''

        if check_input and check_select and check_index and check_month:
            repaintText(self.text_message, 'Start get data ...')
            params = getParams(year, 'token', reporter, partner, trade_flow)
            data = getData(radio, params, start_index, end_index, self.text_message)
            message = dataToExcel(data)
            repaintText(self.text_message, message)
        else:
            repaintText(self.text_message, '{}{}{}{}'.format(message_input, message_select, message_index, message_month))

    def checkEnableAll(self):
        self.check_all.setEnabled(True)
        self.check_1.setEnabled(True)
        self.check_2.setEnabled(True)
        self.check_3.setEnabled(True)
        self.check_4.setEnabled(True)
        self.check_5.setEnabled(True)
        self.check_6.setEnabled(True)
        self.check_7.setEnabled(True)
        self.check_8.setEnabled(True)
        self.check_9.setEnabled(True)
        self.check_10.setEnabled(True)
        self.check_11.setEnabled(True)
        self.check_12.setEnabled(True)
        self.centralwidget.repaint()

    def checkDisableAll(self, all=True):
        if all:
            self.check_all.setChecked(False)
            self.check_all.setEnabled(False)
        self.check_1.setChecked(False)
        self.check_2.setChecked(False)
        self.check_3.setChecked(False)
        self.check_4.setChecked(False)
        self.check_5.setChecked(False)
        self.check_6.setChecked(False)
        self.check_7.setChecked(False)
        self.check_8.setChecked(False)
        self.check_9.setChecked(False)
        self.check_10.setChecked(False)
        self.check_11.setChecked(False)
        self.check_12.setChecked(False)
        self.check_1.setEnabled(False)
        self.check_2.setEnabled(False)
        self.check_3.setEnabled(False)
        self.check_4.setEnabled(False)
        self.check_5.setEnabled(False)
        self.check_6.setEnabled(False)
        self.check_7.setEnabled(False)
        self.check_8.setEnabled(False)
        self.check_9.setEnabled(False)
        self.check_10.setEnabled(False)
        self.check_11.setEnabled(False)
        self.check_12.setEnabled(False)
        self.centralwidget.repaint()

    def radioFreqYear(self):
        self.checkDisableAll()

    def radioFreqMonth(self):
        self.checkEnableAll()

    def checkAll(self):
        if self.check_all.isChecked():
            self.checkDisableAll(all=False)
        else:
            self.checkEnableAll()

    def checkMonth(self):
        count = 0
        if self.check_1.isChecked():
            count += 1
        if self.check_2.isChecked():
            count += 1
        if self.check_3.isChecked():
            count += 1
        if self.check_4.isChecked():
            count += 1
        if self.check_5.isChecked():
            count += 1
        if self.check_6.isChecked():
            count += 1
        if self.check_7.isChecked():
            count += 1
        if self.check_8.isChecked():
            count += 1
        if self.check_9.isChecked():
            count += 1
        if self.check_10.isChecked():
            count += 1
        if self.check_11.isChecked():
            count += 1
        if self.check_12.isChecked():
            count += 1
        return checkMonthCount(count)

    def getRadio(self):
        if self.tab06_radio_code_all.isChecked():
            return 'code_all.pkl'
        if self.tab07_radio_code_6.isChecked():
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
