import os

from PyQt5.QtWidgets import QMainWindow,QApplication,QDialog,QFileDialog,QMessageBox
import sys
from Notepad import Ui_MainWindow
import subprocess


class NotePad_C(QMainWindow):

    def __init__(self):
       #function_call
        super().__init__()
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self)

        #to_save_recent_path_name
        self.path_name=None
        #to_listen_Scroolbar_open_or_close
        self.listen=1
       #to_find_untitles
        self.untitle=0

        self.ShortCut()

        #menu file_open
        self.ui.actionopen.setStatusTip("use to open the file")
        self.ui.actionopen.triggered.connect(self.file_open)
        #menu file_new
        self.ui.actionnew.setStatusTip("new file...")
        self.ui.actionnew.triggered.connect(self.File_new)
        #menu file_saveAs
        self.ui.actionSave_As.setStatusTip("save As")
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        # menu file_save
        self.ui.actionsave.setStatusTip("Save")
        self.ui.actionsave.triggered.connect(self.save)
        # menu Exit
        self.ui.actionExit.setStatusTip("quit")
        self.ui.actionExit.triggered.connect(self.Exit)

        #Edit
        #Edit_cut
        self.ui.actioncut.setStatusTip("cut")
        self.ui.actioncut.triggered.connect(self.ui.textEdit.cut)
        #Copy
        self.ui.actioncopy.setStatusTip("copy")
        self.ui.actioncopy.triggered.connect(self.ui.textEdit.copy)
        #past
        self.ui.actionPast.setStatusTip("paste")
        self.ui.actionPast.triggered.connect(self.ui.textEdit.paste)
        #select_All
        self.ui.actionSelete_All.setStatusTip("Select All")
        self.ui.actionSelete_All.triggered.connect(self.ui.textEdit.selectAll)
        #undo
        self.ui.actionundo.setStatusTip("undo")
        self.ui.actionundo.triggered.connect(self.ui.textEdit.undo)
        #redo
        self.ui.actionredo.setStatusTip("rndo")
        self.ui.actionredo.triggered.connect(self.ui.textEdit.redo)

        #run_menu
        self.ui.actionrun.triggered.connect(self.exe)

        #btns_Actions
        #exe_btn
        self.ui.run_btn.clicked.connect(self.exe)
        #Slide_btn
        self.ui.Slide_btn_3.clicked.connect(self.slider)
        #run_btn
        self.ui.close.clicked.connect(self.close_output_tab)



    def close_output_tab(self):
        self.ui.OutPut_tot.setMaximumSize(16777215, 0)




    def slider(self):
            self.listen+= 1
            if self.listen % 2 == 0:
                self.ui.slideMenu_container.setMaximumSize(200,16777215)
            else:
                self.ui.slideMenu_container.setMaximumSize(0,16777215)



    def exe(self):
        def Check_MessageBox_1(i):
            if (i.text() == "OK"):
                self.save()
            elif (i.text() == "Cancel"):
                pass

        # Creating_messageBox
        MessageBox = QMessageBox()
        MessageBox.setIcon(QMessageBox.Question)
        MessageBox.setText("Do you want save this file ?")
        MessageBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        MessageBox.setModal(True)
        MessageBox.buttonClicked.connect(Check_MessageBox_1)
        x = MessageBox.exec_()
        try:

            check_ex=self.check_ext(os.path.basename(self.path_name))
            print(check_ex)
            if(check_ex == "py"):
                Output = subprocess.run(["python",self.path_name],stdout=subprocess.PIPE,text=True,stderr=subprocess.PIPE)
                print(Output.stdout,Output.stderr)
            elif (check_ex == "txt"):
                Output = subprocess.run(["cat", self.path_name], stdout=subprocess.PIPE, text=True,stderr=subprocess.PIPE)
                print(Output.stdout, Output.stderr)
            elif (check_ex == "c"):
                Output = subprocess.run(["gcc", "a.out"], stdout=subprocess.PIPE, text=True,stderr=subprocess.PIPE)
                print(Output.stdout, Output.stderr)
            #Set_OutPut_Wid_Size
            self.ui.OutPut_tot.setMaximumSize(16777215, 150)
            self.ui.Output.setStatusTip("OutPut Area")
            #Print_OutPut
            self.ui.Output.setText(str(Output.stdout) + str(Output.stderr))
            #Output_title
            self.ui.label.setText("OutPut {"+os.path.basename(self.path_name)+"}")
            self.setStatusTip("file runing..")
        except:
            print("File Can't Run At the moment")


    def check_ext(self,F_Name):
        ex=F_Name.split('.')
        return ex[1]

    def file_open(self):
        # getting path and bool value
        try:
            self.path,_ = QFileDialog.getOpenFileName(self,"open file","","(*.*)")
            self.path_name = self.path
            print(self.path_name)
            with open(self.path, 'r+') as f:
                # read the file
                text = f.read()
                self.ui.textEdit.setText(text)
                self.update_title(self.path)
        except:
            pass



    def save(self):
        if self.path_name is None:

              self.saveAs()

        else:
            file = open(self.path_name, 'w')
            file.write(self.ui.textEdit.toPlainText())
            file.close()



    def update_title(self,path_name):
        self.setWindowTitle("NotePad Pro { "+os.path.basename(path_name)+" }")



    def File_new(self):
        def Check_MessageBox(i):
            if (i.text() == "OK"):
                self.save()
                self.ui.textEdit.clear()
                self.untitle=self.untitle+1
                self.setWindowTitle("NotePad Pro "+"{ Untitled-" + str(self.untitle)+" }")
                self.path_name = None
            elif (i.text() == "Cancel"):
                self.ui.textEdit.clear()
                self.untitle = self.untitle + 1
                self.setWindowTitle("NotePad Pro "+"{ Untitled-" + str(self.untitle)+" }")
                self.path_name = None
        #Creating_messageBox
        if(self.ui.textEdit.toPlainText()):
            MessageBox = QMessageBox()
            MessageBox.setIcon(QMessageBox.Question)
            MessageBox.setText("Do you want save this file ?")
            MessageBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            MessageBox.setModal(True)
            MessageBox.buttonClicked.connect(Check_MessageBox)
            x = MessageBox.exec_()
        else:
            self.ui.textEdit.clear()
            self.untitle = self.untitle + 1
            self.setWindowTitle("NotePad Pro "+"{ Untitled-" + str(self.untitle)+" }")
            self.path_name=None




    def saveAs(self):
        try:
            name,_ = QFileDialog.getSaveFileName(self, 'Save File',"","Text File (*.txt)")
            self.path_name = str(name)
            file = open(name,'w')
            text = self.ui.textEdit.toPlainText()
            file.write(text)
            file.close()
            self.update_title(self.path_name)
        except:
            self.path_name=None


    def Exit(self):
            self.close()

    def ShortCut(self):
        #Edit_menu_Shorts....
        self.ui.actionPast.setShortcut('Ctrl+p')
        self.ui.actioncut.setShortcut('Ctrl+x')
        self.ui.actionCopy.setShortcut('Ctrl+c')
        self.ui.actionredo.setShortcut('Ctrl+shift+z')
        self.ui.actionundo.setShortcut('Ctrl+z')
        self.ui.actionSelete_All.setShortcut('Ctrl+a')

        #Run_menu_short
        self.ui.actionrun.setShortcut('f5')

        #File_menu_shorts
        self.ui.actionopen.setShortcut('Ctrl+o')
        self.ui.actionsave.setShortcut('Ctrl+s')
        self.ui.actionSave_As.setShortcut('Ctrl+shift+s')
        self.ui.actionExit.setShortcut('Ctrl+esc')
        self.ui.actionnew.setShortcut('Ctrl+n')





if __name__ == '__main__':
    app = QApplication(sys.argv)
    NotePad_1=NotePad_C()
    NotePad_1.show()
    sys.exit(app.exec_())