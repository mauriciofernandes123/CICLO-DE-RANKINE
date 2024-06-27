# Nome do arquivo: Ferramenta didática Ciclo de Rankine
# Autor: Maurício Fernandes de Oliveira Assis
# Data de criação: 30/12/2023
# Data da última modificação: 25/02/2024 
# Versão do Python: 3.12.1

import sys
from PySide6 import QtCore
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QMessageBox)
from ui_main import Ui_MainWindow
#from PyQt6 import QtCore
from Ciclos import Ciclos
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtGui import QImage, QPixmap, QIcon
from otimizacao import otimizarReaquecimento
from propriedades_1 import encontrarPropriedade
from propriedades_2 import allPropriedades


class MainWindow (QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("MF - Ferramenta didática Ciclo de Rankine")
        self.showMaximized()
        appIcon = QIcon(u":/icons/icons/logo.png")
        self.setWindowIcon(appIcon)
        #
        ###################################
        #Chamando o Menu lateral (TOGGLE BUTTON)
        self.btn_toggle.clicked.connect(self.LeftMenu)
        ###########################

#__________________________Páginas do Sistema______________________________________
        self.btn_home.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_home))
        self.btn_simples.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_Simples))
        self.btn_reaquecimento.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_Reaquecimento))
        self.btn_regenerativo.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_regenerativo))
        self.btn_contatos.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_contatos))
        self.btn_sobre.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_sobre))
        ##################################################################

#______________PARAMETROS DE CALCULAR E LIMPAR DADOS______________
        
        self.calcular.clicked.connect(self.processarDadosSimples)
        self.limpar.clicked.connect(self.limparCampos)
        self.botaoprop.clicked.connect(self.calcularPropriedades)
        self.limpar_prop.clicked.connect(self.limparCampos)
        self.calcular_rea.clicked.connect(self.processarDadosReaquecimento)
        self.limpar_rea.clicked.connect(self.limparCampos)
        self.otimizar_rea.clicked.connect(self.otimizar)
        self.calcular_reg.clicked.connect(self.processarDadosRegenerativo)
        self.limpar_reg.clicked.connect(self.limparCampos)
        self.calcular_reg_2.clicked.connect(self.processarDadosRegenerativoReaquecimento)
        self.limpar_reg_2.clicked.connect(self.limparCampos)
####################################################################################

#__________________MARCAR E DESMARCAR CHECKBOX____________________________       
        self.op1bomba.clicked.connect(lambda: self.desmarcarBomba(self.op1bomba ))
        self.op2bomba.clicked.connect(lambda: self.desmarcarBomba(self.op2bomba))
        self.op1caldeira.clicked.connect(lambda: self.desmarcarCaldeira(self.op1caldeira))
        self.op2caldeira.clicked.connect(lambda: self.desmarcarCaldeira(self.op2caldeira))
        self.op1bombarea.clicked.connect(lambda: self.desmarcarBombarea(self.op1bombarea ))
        self.op2bombarea.clicked.connect(lambda: self.desmarcarBombarea(self.op2bombarea))
        self.op1caldeirarea.clicked.connect(lambda: self.desmarcarCaldeirarea(self.op1caldeirarea))
        self.op2caldeirarea.clicked.connect(lambda: self.desmarcarCaldeirarea(self.op2caldeirarea))
        self.op1bombareg.clicked.connect(lambda: self.desmarcarBombareg(self.op1bombareg ))
        self.op2bombareg.clicked.connect(lambda: self.desmarcarBombareg(self.op2bombareg))
        self.op1bomba2reg.clicked.connect(lambda: self.desmarcarBomba2reg(self.op1bomba2reg ))
        self.op2bomba2reg.clicked.connect(lambda: self.desmarcarBomba2reg(self.op2bomba2reg))
        self.op1turbinarea.clicked.connect(lambda: self.desmarcarTurbinarea(self.op1turbinarea ))
        self.op2turbinarea.clicked.connect(lambda: self.desmarcarTurbinarea(self.op2turbinarea))
        self.op1turbinareg.clicked.connect(lambda: self.desmarcarTurbinareg(self.op1turbinareg ))
        self.op2turbinareg.clicked.connect(lambda: self.desmarcarTurbinareg(self.op2turbinareg))

        #_________________REGENERATIVO COM REAQUECIMENTO_____________________________________________
        self.op1bombareg_2.clicked.connect(lambda: self.desmarcarBombareg_2(self.op1bombareg_2 ))
        self.op2bombareg_2.clicked.connect(lambda: self.desmarcarBombareg_2(self.op2bombareg_2))
        self.op1bomba2reg_2.clicked.connect(lambda: self.desmarcarBomba2reg_2(self.op1bomba2reg_2 ))
        self.op2bomba2reg_2.clicked.connect(lambda: self.desmarcarBomba2reg_2(self.op2bomba2reg_2))
        self.op1turbinareg_2.clicked.connect(lambda: self.desmarcarTurbinareg_2(self.op1turbinareg_2 ))
        self.op2turbinareg_2.clicked.connect(lambda: self.desmarcarTurbinareg_2(self.op2turbinareg_2))
        self.op1turbina2reg_2.clicked.connect(lambda: self.desmarcarTurbina2reg_2(self.op1turbina2reg_2 ))
        self.op2turbina2reg_2.clicked.connect(lambda: self.desmarcarTurbina2reg_2(self.op2turbina2reg_2))
################################################################################################

#__________________________________PROPRIEDADES TERMODINAMICAS_________________________________________________________________
    def calcularPropriedades(self):
        
        #_________Capturar as opções________________________
        substancia = self.comboBoxFluido.currentText()
        propriedade = self.comboBoxprop.currentText()
        op1 = self.comboBoxprop1.currentText()
        op2 = self.comboBoxprop2.currentText()

        #_____________________Verificar se os valores da propriedade foram inseridos__________________
        if not self.propriedade1.text():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("PREENCHA O VALOR DA PROPRIEDADE 1")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not self.propriedade2.text():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("PREENCHA O VALOR DA PROPRIEDADE 2")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        ##############################################################################################
            
        propriedade1 = float(self.propriedade1.text())
        propriedade2 = float(self.propriedade2.text())
###########################################################################################


#____________________________TRANSFORMAR AS OPÇÕES SELECIONADAS PARA O BACK_____________________________________________
        opcoes= {'Pressão': 'P', 'Temperatura': 'T', 'Volume específico': 'V', 'Energia interna':  'U', 'Entalpia': 'H', 'Entropia': 'S' , 'Título': 'Q'}
        # Verifica se op1 está presente em opcoes1, se estiver substitui, senão mantém op1
        propriedade = opcoes[propriedade] if propriedade in opcoes else propriedade
        op1 = opcoes[op1] if op1 in opcoes else op1
        op2 = opcoes[op2] if op2 in opcoes else op2

#___________________CALCULAR AS PROPRIEDADES______________________________________________
        
        #_______________Calcular todas as propriedades_____________________________________
        if propriedade == 'Todas':

            resultado = allPropriedades(substancia, propriedade1, propriedade2, op1, op2)

            if op1 == op2:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PROPRIEDADE 1 IGUAL A PROPRIEDADE 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            
            elif resultado == 'Erro':
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PROPRIEDADE NÃO ENCONTRADA, VERIFIQUE E TENTE NOVAMENTE")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            else:
                if resultado[3] =='twophase':

                    resultados = 'RESULTADOS'
                    self.resultados.setText(resultados)

                    saturacao = 'VALORES DE SATURAÇÃO'
                    self.saturacao.setText(saturacao)

                    pressao = "Valor da Pressão: {:.5f}  kPa ".format(resultado[0][0])
                    self.valor_pressao.setText(pressao)

                    temperatura = "Valor da Temperatura: {:.5f} °C".format(resultado[0][1])
                    self.valor_temperatura.setText(temperatura)

                    volume = "Valor do Volume específico: {:.5f} m³/kg".format(resultado[0][2])
                    self.valor_volume.setText(volume)

                    energia = "Valor da Energia: {:.5f} kJ/kg".format(resultado[0][3])
                    self.valor_energia.setText(energia)

                    entalpia = "Valor da Entalpia: {:.5f} kJ/kg".format(resultado[0][4])
                    self.valor_entalpia.setText(entalpia)

                    entropia = "Valor da Entropia: {:.5f} kJ/kgK".format(resultado[0][5])
                    self.valor_entropia.setText(entropia)
                    
                    #_______________________  LIQUIDOS ______________________________________
                    volume_liquido = 'O volume do liquido saturado é: {:.5f} m³/kg'.format(resultado[1][2])
                    self.liquido.setText(volume_liquido)

                    energia_liquida = 'A energia do liquido saturado é: {:.5f} kJ/kg'.format(resultado[1][3])
                    self.liquido2.setText(energia_liquida)

                    entalpia_liquida = 'A entalpia do liquido saturado é: {:.5f} kJ/kg'.format(resultado[1][4])
                    self.liquido3.setText(entalpia_liquida)

                    entropia_liquida = 'A entropia do liquido saturado é: {:.5f} kJ/kgK'.format(resultado[1][5])
                    self.liquido4.setText(entropia_liquida)
                    #################################################################################

                    #_________________________VAPORES________________________________________
                    volume_vapor = 'O volume do vapor saturado é: {:.5f} m³/kg'.format(resultado[2][2])
                    self.vapor.setText(volume_vapor)

                    energia_vapor = 'A energia do vapor saturado é: {:.5f} kJ/kg'.format(resultado[2][3])
                    self.vapor2.setText(energia_vapor)

                    entalpia_vapor = 'A entalpia do vapor saturado é: {:.5f} kJ/kg'.format(resultado[2][4])
                    self.vapor3.setText(entalpia_vapor)

                    entropia_vapor = 'A entropia do vapor saturado é: {:.5f} kJ/kgK'.format(resultado[2][5])
                    self.vapor4.setText(entropia_vapor)

                else:
                    resultados = 'RESULTADOS'
                    self.resultados.setText(resultados)

                    pressao = "Valor da Pressão: {:.5f} Kpa".format(resultado[0][0])
                    self.valor_pressao.setText(pressao)

                    temperatura = "Valor da Tempepratura: {:.5f} °C".format(resultado[0][1])
                    self.valor_temperatura.setText(temperatura)

                    volume = "Valor do Volume específico: {:.5f} m³/kg".format(resultado[0][2])
                    self.valor_volume.setText(volume)

                    energia = "Valor da Energia: {:.5f} kJ/kg".format(resultado[0][3])
                    self.valor_energia.setText(energia)

                    entalpia = "Valor da Entalpia: {:.5f} kJ/kg".format(resultado[0][4])
                    self.valor_entalpia.setText(entalpia)

                    entropia = "Valor da Entropia: {:.5f} kJ/kgK".format(resultado[0][5])
                    self.valor_entropia.setText(entropia)

        ############################################################################################
                

        #________________________Calcular propriedade específica_______________________________________________
        else:
            
            resultado = encontrarPropriedade(propriedade, substancia, propriedade1, propriedade2, op1, op2)
            
        
            if resultado == 'Erro':
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PROPRIEDADE NÃO ENCONTRADA, VERIFIQUE E TENTE NOVAMENTE")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif resultado =='op1':
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PROPRIEDADE 1 IGUAL A DESEJADA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif resultado =='op2':
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PROPRIEDADE 2 IGUAL A DESEJADA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif resultado =='op':
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PROPRIEDADE 1 IGUAL A PROPRIEDADE 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            else:
                if resultado['fase'] == 'twophase':
                    if propriedade == 'T' or propriedade == 'P':
                        resultado = "O resultado é: {:.5f} ".format(resultado['propriedade'])
                        self.propriedadeEncontrada.setText(resultado)

                    elif propriedade == 'Q':
                        resultado = "O resultado é: {:.5f} ".format(resultado['propriedade'])
                        self.propriedadeEncontrada.setText(resultado)

                    else:

                        liquido = "O resultado é : {:.5f} para liquido saturado ".format(resultado['liquido'])
                        self.liquido.setText(liquido)

                        vapor = "O resultado é : {:.5f} para vapor saturado".format(resultado['vapor'])
                        self.vapor.setText(vapor)
                
                resultado = "O resultado é: {:.5f} ".format(resultado['propriedade'])
                self.propriedadeEncontrada.setText(resultado)
                
            
            ##########################################################################

#################################################################################################


#____________PROCESSADOR DOS DADOS SIMPLES____________________________   
    def processarDadosSimples(self):

       #___________VERIFICANDO DEPÊNDENCIA____________________
        if not (self.op1bomba.isChecked() or self.op2bomba.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA BOMBA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1caldeira.isChecked() or self.op2caldeira.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA CALDEIRA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        #############################################

#__________________Check se as variáveis foram preenchidas para o calculo_____________________________
        if self.op1bomba.isChecked():

            if not self.p1.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 = 1
                p1 = float(self.p1.text()) * 1000
                t1 = None
        
        elif self.op2bomba.isChecked():
            
            if not self.p1.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =2
                p1 = float(self.p1.text()) * 1000
            
                
                if not self.t1.text():
                    op1 =2
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 1")
                    msg_box.setWindowTitle("Aviso")
                    msg_box.exec()
                else:
                    t1 = float(self.t1.text()) + 273.15

        if self.op1caldeira.isChecked():

            if not self.p2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op2 = 1
                p2 = float(self.p2.text()) * 1000

            if not self.x3.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA TÍTULO DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                x3 = float(self.x3.text()) / 100
                t3 = None

        elif self.op2caldeira.isChecked():

            if not self.p2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA PRESSÃO DO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op2 = 2
                p2 = float(self.p2.text()) * 1000
                #op2 = float(entry_op2.get())
                x3 = None

            if not self.t3.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA TEMPERATURA DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t3 = float(self.t3.text()) + 273.15
#____________________________________________________________________________________________________________________________________
                
        #Chamando a função para resolver o ciclo de rankine simples
        resultado = Ciclos.rankineSimples(op1, p1, t1, p2, op2, x3, t3)
#___________________________________________________________________________________________
        
#_______________________Verificar as propriedades termodinamicas da tabela________________
        verificar1 = resultado
        if verificar1 == 2:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("VERIFIQUE AS PROPRIEDADES INSERIDAS EM CADA ESTADO")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        else:
        #______________Verifica os volumes de controle_____________________
            erro = resultado['erro']
            
            if erro == 0: #Parametro de verificação (sem erro)

                eta = "Eficiência: {:.3f} ou {:.3f}%".format(resultado['eta'], resultado['eta'] * 100)
                self.eta_result.setText(eta)

                wt = "Trabalho da turbina: {:.3f} kJ/kg".format(resultado['wt'])
                self.wt_result.setText(wt)

                wb = "Trabalho da bomba: {:.3f} kJ/kg".format(resultado['wb'])
                self.wb_result.setText(wb)

                qh = "Calor da caldeira: {:.3f} kJ/kg".format(resultado['qh'])
                self.qh_result.setText(qh)
            
            #______________Se houver erros_________________________
            elif erro == 1:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA CALDEIRA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 2:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA TURBINA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 3:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA BOMBA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 4:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
           
            elif erro == 5:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 6:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 7:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 4")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            
            #______________________________________________________________
############################################################################
        


#___________________PROCESSADOR DE DADOS REAQUECIMENTO____________________
    def processarDadosReaquecimento(self):

         #___________VERIFICANDO DEPÊNDENCIA____________________
        if not (self.op1bombarea.isChecked() or self.op2bombarea.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA BOMBA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1caldeirarea.isChecked() or self.op2caldeirarea.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA CALDEIRA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1turbinarea.isChecked() or self.op2turbinarea.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA TURBINA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        #############################################

        if self.op1bombarea.isChecked():

            if not self.p1rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =1
                p1 = float(self.p1rea.text()) * 1000
                
                t1 = None

        elif self.op2bombarea.isChecked():

            if not self.p1rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =2
                p1 = float(self.p1rea.text()) * 1000
                    #    x1 = None
            if not self.t1rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t1 = float(self.t1rea.text()) + 273.15

        if self.op1caldeirarea.isChecked():

            if not self.p2rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op2 =1
                p2 = float(self.p2rea.text()) * 1000
                #op2 = float(entry_op2.get())

            if not self.x3rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TÍTULO DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                x3 = float(self.x3rea.text()) / 100
                t3 = None

            if not self.p4rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 4")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                p4 = float(self.p4rea.text()) * 1000

        elif self.op2caldeirarea.isChecked():
            
            if not self.p2rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op2 =2
                p2 = float(self.p2rea.text()) * 1000
                #op2 = float(entry_op2.get())
                x3 = None

            if not self.t3rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t3 = float(self.t3rea.text()) + 273.15
            
            if not self.p4rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 4")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                p4 = float(self.p4rea.text()) * 1000

        if self.op2turbinarea.isChecked():

            op3=1

            if not self.t5rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t5 = float(self.t5rea.text()) + 273.15
                x5 = None

        elif self.op1turbinarea.isChecked():
                
            op3 = 2
    
            if not self.x5rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA O TÍTULO DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                x5 = float(self.x5rea.text()) / 100
                t5 = None

        #O parametro grafico é adicionado para plotar o grafico se for grafico = 1. (no otimizar nao tem grafico de calculo)
        resultado = Ciclos.reaquecimento(op1, p1, t1, p2, op2, x3, t3, p4, op3, t5 ,x5, grafico=1) #Resolve o ciclo


        #___________verificar as  propriedades______________________
        verificar1 = resultado
        if verificar1 == 2:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("VERIFIQUE AS PROPRIEDADES INSERIDAS EM CADA ESTADO")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
       
        else:
        #______________Verifica os volumes de controle_____________________
            erro = resultado['erro']
            
            if erro == 0: #Parametro de verificação (sem erro)

                eta = "Eficiência: {:.3f} ou {:.3f}%".format(resultado['n'], resultado['n'] * 100)
                self.eta_result_rea.setText(eta)

                wt = "Trabalho da turbina: {:.3f} kJ/kg".format(resultado['wt'])
                self.wt_result_rea.setText(wt)

                wb = "Trabalho da bomba: {:.3f} kJ/kg".format(resultado['wb'])
                self.wb_result_rea.setText(wb)

                qh = "Calor da caldeira: {:.3f} kJ/kg".format(resultado['qh'])
                self.qh_result_rea.setText(qh)
            
            #______________Se houver erros_________________________
            elif erro == 1:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA CALDEIRA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 2:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA TURBINA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 3:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA BOMBA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 4:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NA PRESSÃO INTERMEDIÁRIA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            
            elif erro == 5:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
           
            elif erro == 6:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 7:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 8:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 9:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 6")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
          ##########################################################

    def otimizar(self):
        
        grafico = 2
          #___________VERIFICANDO DEPÊNDENCIA____________________
        if not (self.op1bombarea.isChecked() or self.op2bombarea.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA BOMBA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1caldeirarea.isChecked() or self.op2caldeirarea.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA CALDEIRA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1turbinarea.isChecked() or self.op2turbinarea.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA TURBINA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        #############################################

        if self.op1bombarea.isChecked():

            if not self.p1rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =1
                p1 = float(self.p1rea.text()) * 1000
                
                t1 = None

        elif self.op2bombarea.isChecked():

            if not self.p1rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =2
                p1 = float(self.p1rea.text()) * 1000
                    #    x1 = None
            if not self.t1rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t1 = float(self.t1rea.text()) + 273.15

        if self.op1caldeirarea.isChecked():

            if not self.p2rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op2 =1
                p2 = float(self.p2rea.text()) * 1000
                #op2 = float(entry_op2.get())

            if not self.x3rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TÍTULO DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                x3 = float(self.x3rea.text())
                t3 = None

            if not self.p4rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 4")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                p4 = float(self.p4rea.text()) * 1000

        elif self.op2caldeirarea.isChecked():
            
            if not self.p2rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op2 =2
                p2 = float(self.p2rea.text()) * 1000
                #op2 = float(entry_op2.get())
                x3 = None

            if not self.t3rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t3 = float(self.t3rea.text()) + 273.15
            
            if not self.p4rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 4")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                p4 = float(self.p4rea.text()) * 1000

        if self.op2turbinarea.isChecked():

            op3=1

            if not self.t5rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t5 = float(self.t5rea.text()) + 273.15
                x5 = None

        elif self.op1turbinarea.isChecked():
                
            op3 = 2
    
            if not self.x5rea.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA O TÍTULO DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                x5 = float(self.x5rea.text())
                t5 = None

        resultado = otimizarReaquecimento(op1, p1, t1, p2, op2, x3, t3, p4, op3, t5 ,x5,grafico)

        verificar1 = resultado
        if verificar1 == 2:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("VERIFIQUE AS PROPRIEDADES INSERIDAS EM CADA ESTADO")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
       
        else:
        #______________Verifica os volumes de controle_____________________
            erro = resultado['erro']
            
            if erro == 0: #Parametro de verificação (sem erro)

                eta = "Eficiência máxima: {:.3f} ou {:.3f}%".format(resultado['etamax'], resultado['etamax'] * 100)
                self.eta_result_rea.setText(eta)

                wt = "Trabalho da líquido máximo: {:.3f} kJ/kg".format(resultado['wliqmax'])
                self.wt_result_rea.setText(wt)

                petamax = "Pressão para eficiência máxima: {:.3f} (kPa)".format(resultado['petamax'])
                self.wb_result_rea.setText(petamax)

                pwmax = "Pressão para trabalho líquido máxima: {:.3f} (KPa)".format(resultado['pwmax'])
                self.qh_result_rea.setText(pwmax)

                
            
            #______________Se houver erros_________________________
            elif erro == 1:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA CALDEIRA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 2:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA TURBINA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 3:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA BOMBA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 4:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NA PRESSÃO INTERMEDIÁRIA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            
            elif erro == 5:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
           
            elif erro == 6:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 7:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 8:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 9:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 6")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
          


###################################################################################

#______________PROCESSADOR DE DADOS REGENERATIVO___________________________________
    def processarDadosRegenerativo(self):
         #___________VERIFICANDO DEPÊNDENCIA____________________
        if not (self.op1bombareg.isChecked() or self.op2bombareg.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA BOMBA 1 NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1bomba2reg.isChecked() or self.op2bomba2reg.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA BOMBA 2 NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1turbinareg.isChecked() or self.op2turbinareg.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA TURBINA NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        #############################################
            
        if self.op1bombareg.isChecked():
             
            if not self.p1reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =1
                p1 = float(self.p1reg.text()) * 1000
                # x1 = float(entry_op1.get())
                t1 = None

        if self.op2bombareg.isChecked():
            if not self.p1reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =2
                p1 = float(self.p1reg.text()) * 1000
                    #    x1 = None
            if not self.t1reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t1 = float(self.t1reg.text()) + 273.15

        if self.op1bomba2reg.isChecked():

            if not self.p2reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op3 =2
                p2 = float(self.p2reg.text()) * 1000
                y=0
                t3 = None

        elif self.op2bomba2reg.isChecked():
            if not self.p2reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op3 =1
                p2 = float(self.p2reg.text()) * 1000

            if not self.yreg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A FRAÇÃO")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                y = float(self.yreg.text())
                
                x3 = None
        
        if self.op1turbinareg.isChecked():
            if not self.p5reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op2 =2
                p5 = float(self.p5reg.text()) * 1000
            
            if not self.x5reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA O TÍTULO DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                x5 = float(self.x5reg.text()) / 100
                t5 = None

        elif self.op2turbinareg.isChecked():

            if not self.p5reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op2 = 1
                p5 = float(self.p5reg.text()) * 1000
                x5 = None
            
            if not self.t5reg.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t5 = float(self.t5reg.text()) + 273.15

        
        resultado = Ciclos.regenerativo(op1, p1, t1, p2, op2, p5, t5, x5, op3, y)

        #___________verificar as  propriedades______________________
        verificar1 = resultado
        if verificar1 == 2:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("VERIFIQUE AS PROPRIEDADES INSERIDAS EM CADA ESTADO")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
       
        else:
        #______________Verifica os volumes de controle_____________________
            erro = resultado['erro']
            
            if erro == 0: #Parametro de verificação (sem erro)
                
                eta = "Eficiência: {:.3f} ou {:.3f}%".format(resultado['eta'], resultado['eta'] * 100)
                self.eta_result_reg.setText(eta)

                wt = "Trabalho da turbina: {:.3f} kJ/kg".format(resultado['wt'])
                self.wt_result_reg.setText(wt)

                wb = "Trabalho da bomba: {:.3f} kJ/kg".format(resultado['wb'])
                self.wb_result_reg.setText(wb)

                qh = "Calor da caldeira: {:.3f} kJ/kg".format(resultado['qh'])
                self.qh_result_reg.setText(qh)

                y = "Fração y: {:.3f} ".format(resultado['y'])
                self.yreg_2.setText(y)
            
            #______________Se houver erros_________________________
            elif erro == 1:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA CALDEIRA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 2:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA TURBINA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 3:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA BOMBA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 4:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
           
            elif erro == 5:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 6:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 7:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 4")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 8:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 9:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 6")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()


            elif erro == 10:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 7")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()


            elif erro == 11:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NA FRAÇÃO Y")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            

          ##########################################################
       
        

#______________PROCESSADOR DE DADOS REGENERATIVO COM REAQUECIMENTO___________________________________
    def processarDadosRegenerativoReaquecimento(self):
         #___________VERIFICANDO DEPÊNDENCIA____________________
        if not (self.op1bombareg_2.isChecked() or self.op2bombareg_2.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA BOMBA 1 NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1bomba2reg_2.isChecked() or self.op2bomba2reg_2.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA BOMBA 2 NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        
        if not (self.op1turbinareg_2.isChecked() or self.op2turbinareg_2.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA TURBINA DE ALTA PRESSÃO NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()

        if not (self.op1turbina2reg_2.isChecked() or self.op2turbina2reg_2.isChecked()):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("A DEPENDÊCIA DA TURBINA DE BAIXA PRESSÃO NÃO FOI MARCADA")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        #############################################
        
        if not self.m_reg_2.text():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("PREENCHA A VAZÃO MASSICA DO CICLO")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        else:
            m = float(self.m_reg_2.text())

        if self.op1bombareg_2.isChecked():
             
            if not self.p1reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =1
                p1 = float(self.p1reg_2.text()) * 1000
                # x1 = float(entry_op1.get())
                t1 = None



        if self.op2bombareg_2.isChecked():
            if not self.p1reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op1 =2
                p1 = float(self.p1reg_2.text()) * 1000
                    #    x1 = None
            if not self.t1reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t1 = float(self.t1reg_2.text()) + 273.15

        if not self.p2reg_2.text():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 2")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        else:

            p2 = float(self.p2reg_2.text()) * 1000


        if not self.n_reg_2.text():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("PREENCHA A EFICIÊNCIA ISENTRÓPICA DAS BOMBAS")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        else:
            n = float(self.n_reg_2.text()) / 100

            if n <0.2 or n>1:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NA EFICIÊNCIA ISENTRÓPICA DA BOMBA: RECOMENDADO ENTRE 20-100%")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

        if self.op1bomba2reg_2.isChecked():

            if not self.p3reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op3 =1
                p3 = float(self.p3reg_2.text()) * 1000
                t3 = None

        elif self.op2bomba2reg_2.isChecked():
            if not self.p3reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                op3 =2
                p3 = float(self.p3reg_2.text()) * 1000

            if not self.t3reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t3 = float(self.t3reg_2.text())
                
                x3 = None
        
        if self.op1turbinareg_2.isChecked():
            op5 =2
             
            if not self.x5reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA O TÍTULO DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                
                t5 = None
                x5 = float(self.x5reg_2.text())
            
            if not self.p6reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 6")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                p6 = float(self.p6reg_2.text()) * 1000

        elif self.op2turbinareg_2.isChecked():
            op5 = 1

            x5 = None
            
            if not self.t5reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t5 = float(self.t5reg_2.text()) + 273.15

            if not self.p6reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A PRESSÃO DO ESTADO 6")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                p6 = float(self.p6reg_2.text()) * 1000

        if not self.nt_reg_2.text():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("PREENCHA A EFICIÊNCIA ISENTRÓPICA DAS TURBINAS")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
        else:
            nt = float(self.nt_reg_2.text()) / 100

            if nt<0.2 or nt>1:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NA EFICIÊNCIA ISENTRÓPICA DA TURBINA: RECOMENDADO ENTRE 20-100%")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            

        if self.op1turbina2reg_2.isChecked():
            op7 =2
        
            if not self.x7reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA O TÍTULO DO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t7 = None
                x7 = float(self.x7reg_2.text())
                

        elif self.op2turbina2reg_2.isChecked():
            op7 = 1

            x7 = None
            
            if not self.t7reg_2.text():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("PREENCHA A TEMPERATURA DO ESTADO 7")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
            else:
                t7 = float(self.t7reg_2.text()) + 273.15
        
        
        resultado = Ciclos.regenerativoReaquecimento(m, op1, p1, t1, p2, n, op3, p3, t3, op5, t5, x5, p6, nt, op7, t7, x7 )
        
        #___________verificar as  propriedades______________________
        verificar1 = resultado
        if verificar1 == 2:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("VERIFIQUE AS PROPRIEDADES INSERIDAS EM CADA ESTADO")
            msg_box.setWindowTitle("Aviso")
            msg_box.exec()
       
        else:
        #______________Verifica os volumes de controle_____________________
            erro = resultado['erro']
            
            if erro == 0: #Parametro de verificação (sem erro)
                
                eta = "Eficiência: {:.3f} ou {:.3f}%".format(resultado['eta'], resultado['eta'] * 100)
                self.eta_result_reg_2.setText(eta)

                wt = "Trabalho da turbina: {:.3f} kW".format(resultado['wt'])
                self.wt_result_reg_2.setText(wt)

                wb = "Trabalho da bomba: {:.3f} kW".format(resultado['wb'])
                self.wb_result_reg_2.setText(wb)

                qh = "Calor da caldeira: {:.3f} kW".format(resultado['qh'])
                self.qh_result_reg_2.setText(qh)

                y = "Fração y: {:.3f} ".format(resultado['y'])
                self.y_result_reg_2.setText(y)

                t8 = "A temperatura do estado 8 é: : {:.3f} °C ".format(resultado['t8'])
                self.t8_result_reg_2.setText(t8)

                m8 = "O fluxo de massa do vapor extraído : {:.3f} kg/s ".format(resultado['m8'])
                self.m8_result_reg_2.setText(m8)

                wliq = "O trabalho líquido do ciclo: {:.3f} kW".format(resultado['wliq'])
                self.wliq_result_reg_2.setText(wliq)
            
            #______________Se houver erros_________________________
            
            elif erro == 1:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA CALDEIRA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 2:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA TURBINA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 3:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO VOLUME DE CONTROLE DA BOMBA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 4:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 1")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
           
            elif erro == 5:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 2")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 6:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 3")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 7:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 4")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 8:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 5")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 9:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 6")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()


            elif erro == 10:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NO ESTADO 7")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()


            elif erro == 11:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NA FRAÇÃO Y")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 12:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NA EFICIÊNCIA ISENTRÓPICA DA BOMBA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()

            elif erro == 13:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("ERRO NA EFICIÊNCIA ISENTRÓPICA DA TURBINA")
                msg_box.setWindowTitle("Aviso")
                msg_box.exec()
          ##########################################################


#______________________FUNÇÃO DE MARCAR E DESMARCAR CHECKBOX___________________________
    
    #________________desmarcar checkbox da bomba______________________________
    def desmarcarBomba(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1bomba, self.op2bomba]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)

    #________________desmarcar checkbox da caldeira______________________________
    def desmarcarCaldeira(self, checkBox):
        for cb in [ self.op1caldeira, self.op2caldeira]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkBox:
                cb.setChecked(False)

    #________________desmarcar checkbox da bomba reaquecida______________________________
    def desmarcarBombarea(self, checkBox):
        for cb in [ self.op1bombarea, self.op2bombarea]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkBox:
                cb.setChecked(False)

    #________________desmarcar checkbox da caldeira reaquecida______________________________
    def desmarcarCaldeirarea(self, checkBox):
        
        for cb in [ self.op1caldeirarea, self.op2caldeirarea]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkBox:
                cb.setChecked(False)

    #________________desmarcar checkbox da bomba regenerativa______________________________  
    def desmarcarBombareg(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1bombareg, self.op2bombareg]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)
    
    #________________desmarcar checkbox da bomba 2 regenerativa______________________________
    def desmarcarBomba2reg(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1bomba2reg, self.op2bomba2reg]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)

    #________________desmarcar checkbox da turbina reaquecida______________________________
    def desmarcarTurbinarea(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1turbinarea, self.op2turbinarea]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)

    #________________desmarcar checkbox da turbina regenerativa______________________________
    def desmarcarTurbinareg(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1turbinareg, self.op2turbinareg]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)
    
    #________________desmarcar checkbox da bomba regenerativa com reaquecimento______________________________  
    def desmarcarBombareg_2(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1bombareg_2, self.op2bombareg_2]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)
    
    #________________desmarcar checkbox da bomba 2 regenerativa com reaquecimento______________________________
    def desmarcarBomba2reg_2(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1bomba2reg_2, self.op2bomba2reg_2]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)

    def desmarcarTurbinareg_2(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1turbinareg_2, self.op2turbinareg_2]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)

    def desmarcarTurbina2reg_2(self, checkbox):
        # Desmarca todas as outras caixas de seleção exceto a que foi clicada
        for cb in [ self.op1turbina2reg_2, self.op2turbina2reg_2]:  # Adicione mais caixas de seleção conforme necessário
            if cb is not checkbox:
                cb.setChecked(False)

    
######################################################################################
                
#____________LIMPANDO OS CAMPOS__________________________
    def limparCampos(self):
         # Limpar campos QLineEdit individualmente
        #______________SIMPLES____________________
        self.p1.clear()
        self.t1.clear()
        self.p2.clear()
        self.x3.clear()
        self.t3.clear()
        #__________REAQUECIMENTO____________
        self.p1rea.clear()
        self.t1rea.clear()
        self.p2rea.clear()
        self.x3rea.clear()
        self.t3rea.clear()
        self.p4rea.clear()
        self.t5rea.clear()
        self.x5rea.clear()
        #_________________REGENERATIVO____________
        self.p1reg.clear()
        self.t1reg.clear()
        self.p2reg.clear()
        self.yreg.clear()
        self.p5reg.clear()
        self.t5reg.clear()
        self.x5reg.clear()
        #__________REGENERATIVO COM REAQUECIMENTO____________
        self.p1reg_2.clear()
        self.t1reg_2.clear()
        self.p2reg_2.clear()
        self.p3reg_2.clear()
        self.t3reg_2.clear()
        self.t5reg_2.clear()
        self.x5reg_2.clear()
        self.p6reg_2.clear()
        self.t7reg_2.clear()
        self.x7reg_2.clear()
        self.m_reg_2.clear()
        self.n_reg_2.clear()
        self.nt_reg_2.clear()
        


        #Limapando os resultados gerados
        self.wb_result.clear()
        self.wt_result.clear()
        self.eta_result.clear()
        self.qh_result.clear()
        self.wb_result_rea.clear()
        self.wt_result_rea.clear()
        self.eta_result_rea.clear()
        self.qh_result_rea.clear()
        self.wb_result_reg.clear()
        self.wt_result_reg.clear()
        self.eta_result_reg.clear()
        self.qh_result_reg.clear()
        self.yreg_2.clear()
        
        self.wb_result_reg_2.clear()
        self.wt_result_reg_2.clear()
        self.eta_result_reg_2.clear()
        self.qh_result_reg_2.clear()
        self.t8_result_reg_2.clear()
        self.m8_result_reg_2.clear()
        self.wliq_result_reg_2.clear()
        self.y_result_reg_2.clear()


        self.propriedade1.clear()
        self.propriedade2.clear()
        self.valor_pressao.clear()
        self.valor_temperatura.clear()
        self.valor_volume.clear()
        self.valor_energia.clear()
        self.valor_entalpia.clear()
        self.valor_entropia.clear()
        self.propriedadeEncontrada.clear()
        self.saturacao.clear()
        self.vapor.clear()
        self.vapor2.clear()
        self.vapor3.clear()
        self.vapor4.clear()
        self.liquido.clear()
        self.liquido2.clear()
        self.liquido3.clear()
        self.liquido4.clear()
        self.resultados.clear()



        # Desmarcar caixas de seleção QCheckBox individualmente
        self.op1bomba.setChecked(False)
        self.op2bomba.setChecked(False)
        self.op1bombareg.setChecked(False)
        self.op2bombareg.setChecked(False)
        self.op1caldeira.setChecked(False)
        self.op2caldeira.setChecked(False)

        self.op1bombarea.setChecked(False)
        self.op2bombarea.setChecked(False)
        self.op1bombarea.setChecked(False)
        self.op2bombareg.setChecked(False)
        self.op1caldeirarea.setChecked(False)
        self.op2caldeirarea.setChecked(False)

        self.op1bomba2reg.setChecked(False)
        self.op2bomba2reg.setChecked(False)
        self.op1turbinarea.setChecked(False)
        self.op2turbinarea.setChecked(False)
        self.op1turbinareg.setChecked(False)
        self.op2turbinareg.setChecked(False)


        self.op1bombareg_2.setChecked(False)
        self.op2bombareg_2.setChecked(False)
        self.op1bomba2reg_2.setChecked(False)
        self.op2bomba2reg_2.setChecked(False)
        self.op1turbinareg_2.setChecked(False)
        self.op2turbinareg_2.setChecked(False)
        self.op1turbina2reg_2.setChecked(False)
        self.op2turbina2reg_2.setChecked(False)
#############################################################################  


#______________MENU A ESQUERDA ANIMAÇÃO____________        
    def LeftMenu(self):

        width = self.left.width()
    
        if width == 9:
            newWidth = 265

        else :
            newWidth =9

        self.animation = QtCore.QPropertyAnimation(self.left, b"maximumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
##############################################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()