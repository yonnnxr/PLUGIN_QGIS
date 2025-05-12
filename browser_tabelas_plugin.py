# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction
from .browser_dialog import BrowserTabelasDialog 

class BrowserTabelasPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
    def initGui(self):
        self.action = QAction("SCI Browser", self.iface.mainWindow())
        self.action.setWhatsThis("Abre o navegador de tabelas SCI com geometria.")
        self.action.setStatusTip("Navegador de Tabelas SCI")
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&SCI (Original)", self.action)
        self.iface.addToolBarIcon(self.action)
    def unload(self):
        self.iface.removePluginMenu("&SCI (Original)", self.action)
        self.iface.removeToolBarIcon(self.action)
        del self.action
    def run(self):
        dialog = BrowserTabelasDialog()
        dialog.exec_() 
