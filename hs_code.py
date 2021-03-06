import sys
import os
import pickle
from PyQt5 import QtWidgets, QtCore
from main import Ui_MainWindow
from utils import (
    repaintText,
    checkMonthCount,
    getUNCodeList,
    # getUNComtradeLen,
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
        # self.label_value_code_all.setText('')
        # self.label_value_code_6.setText('')
        self.tab01_input_period.setText('')
        self.tab09_input_start_index.setText('0')
        self.tab10_input_end_index.setText('0')
        self.tab11_input_start_hs.setText('0')
        self.tab12_input_end_hs.setText('0')
        self.label_name_end_hs.hide()
        self.tab12_input_end_hs.hide()
        # self.tab01_input_token.setText('')

        # code_all, code_6, message = getUNComtradeLen()
        # self.label_value_code_all.setText(str(code_all))
        # self.label_value_code_6.setText(str(code_6))
        # if len(message) != 0:
        #     repaintText(self.text_message, message)

        # self.tab01_input_token.setEnabled(True)
        self.tab01_input_period.setEnabled(True)
        self.tab09_input_start_index.setEnabled(True)
        self.tab10_input_end_index.setEnabled(True)
        self.tab02_select_reporter.setEnabled(True)
        self.tab03_select_partner.setEnabled(True)
        self.tab04_select_trade_flow.setEnabled(True)
        # self.btn_update_code_list.setEnabled(True)
        self.btn_get_data.setEnabled(True)
        self.tab01_input_period.setFocus(True)

        repaintText(self.text_message, 'Complete initial GUI ...\n')

    def bindFunc(self):
        # self.btn_update_code_list.clicked.connect(self.btnUpdateCodeList)
        self.btn_get_data.clicked.connect(self.btnGetData)
        self.tab05_radio_freq_year.clicked.connect(self.radioFreqYear)
        self.tab06_radio_freq_month.clicked.connect(self.radioFreqMonth)
        self.tab07_radio_index.clicked.connect(self.radioIndex)
        self.tab08_radio_hs.clicked.connect(self.radioHS)
        self.check_all.clicked.connect(self.checkAll)

    # def btnUpdateCodeList(self):
    #     repaintText(self.text_message, 'Start update HS Code, please wait a minute ...')
    #     message = getUNCodeList()
    #     repaintText(self.text_message, message)
    #     code_all, code_6, message = getUNComtradeLen()
    #     self.label_value_code_all.setText(str(code_all))
    #     self.label_value_code_6.setText(str(code_6))
    #     repaintText(self.text_message, '{}\n'.format(message))

    def btnGetData(self):
        # type = self.getRadioCodeType()
        freq = self.getRadioFreqType()
        year = self.getYearMonth()
        index_hs = self.getIndexHS()
        reporter = self.tab02_select_reporter.currentText()
        partner = self.tab03_select_partner.currentText()
        trade_flow = self.tab04_select_trade_flow.currentText()
        start_index = self.tab09_input_start_index.text()
        end_index = self.tab10_input_end_index.text()
        start_hs = self.tab11_input_start_hs.text()
        end_hs = self.tab12_input_end_hs.text()
        # token = self.tab01_input_token.text()
        check_input, message_input = checkInput(PeriodYear=year, StartIndex=start_index, EndIndex=end_index, StartHS=start_hs, EndHS=end_hs)
        check_select, message_select = checkSelect(Reporter=reporter, Partner=partner, TradeFlow=trade_flow)
        check_index, message_index = checkIndex(start_index, end_index)
        if self.tab06_radio_freq_month.isChecked() and not self.check_all.isChecked():
            check_month, message_month = self.checkMonth()
        else:
            check_month = True
            message_month = ''

        if check_input and check_select and check_index and check_month:
            repaintText(self.text_message, 'Start get data ...')
            params = getParams(year, freq, reporter, partner, trade_flow)
            data = getData(params, start_index, end_index, start_hs, index_hs, self.text_message)
            message = dataToExcel(data)
            repaintText(self.text_message, message)
        else:
            repaintText(self.text_message, '{}{}{}{}'.format(message_input, message_select, message_index, message_month))

    def radioIndex(self):
        self.tab09_input_start_index.setEnabled(True)
        self.tab10_input_end_index.setEnabled(True)
        self.tab11_input_start_hs.setText('0')
        self.tab11_input_start_hs.setEnabled(False)
        self.tab12_input_end_hs.setText('0')
        self.tab12_input_end_hs.setEnabled(False)
        self.centralwidget.repaint()

    def radioHS(self):
        self.tab09_input_start_index.setText('0')
        self.tab09_input_start_index.setEnabled(False)
        self.tab10_input_end_index.setText('0')
        self.tab10_input_end_index.setEnabled(False)
        self.tab11_input_start_hs.setEnabled(True)
        self.tab12_input_end_hs.setEnabled(True)
        self.centralwidget.repaint()

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

    def getYearMonth(self):
        year = self.tab01_input_period.text()
        if self.tab05_radio_freq_year.isChecked():
            return year
        if self.tab06_radio_freq_month.isChecked():
            if self.check_all.isChecked():
                return year
            else:
                month_list = str()
                if self.check_1.isChecked():
                    month_list += '{}01, '.format(year)
                if self.check_2.isChecked():
                    month_list += '{}02, '.format(year)
                if self.check_3.isChecked():
                    month_list += '{}03, '.format(year)
                if self.check_4.isChecked():
                    month_list += '{}04, '.format(year)
                if self.check_5.isChecked():
                    month_list += '{}05, '.format(year)
                if self.check_6.isChecked():
                    month_list += '{}06, '.format(year)
                if self.check_7.isChecked():
                    month_list += '{}07, '.format(year)
                if self.check_8.isChecked():
                    month_list += '{}08, '.format(year)
                if self.check_9.isChecked():
                    month_list += '{}09, '.format(year)
                if self.check_10.isChecked():
                    month_list += '{}10, '.format(year)
                if self.check_11.isChecked():
                    month_list += '{}11, '.format(year)
                if self.check_12.isChecked():
                    month_list += '{}12, '.format(year)
                if len(month_list) > 0:
                    return month_list[:-2]
        return year

    def getIndexHS(self):
        if self.tab07_radio_index.isChecked():
            return 'index'
        else:
            return 'hs'

    def getRadioFreqType(self):
        if self.tab05_radio_freq_year.isChecked():
            return 'A'
        if self.tab06_radio_freq_month.isChecked():
            return 'M'
        return 'A'

    # def getRadioCodeType(self):
    #     if self.tab06_radio_code_all.isChecked():
    #         return 'code_all.pkl'
    #     if self.tab07_radio_code_6.isChecked():
    #         return 'code_6.pkl'
    #     return 'code_6.pkl'


class InitialMainWindow:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        InitialMainWindow.MainWindow = Main()
        InitialMainWindow.MainWindow.show()
        sys.exit(app.exec_())


def main():
    program = InitialMainWindow()


def initFile():
    if not os.path.isfile('code_ccc.pkl'):
        code_ccc = dict()
        f = open('code_ccc.pkl', 'wb')
        pickle.dump(code_ccc, f)


if __name__ == '__main__':
    initFile()
    main()
