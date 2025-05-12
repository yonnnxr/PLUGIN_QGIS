# -*- coding: utf-8 -*-

# Este é o ponto de entrada principal para o plugin.
# Ele é chamado pelo QGIS quando o plugin é carregado.

def classFactory(iface):
    """Carrega a classe BrowserTabelasPlugin do arquivo browser_tabelas_plugin.
    
    :param iface: Uma instância de QgisInterface.
    :type iface: QgisInterface
    :returns: Instância da classe principal do plugin.
    :rtype: BrowserTabelasPlugin
    """
    # Importa a classe principal do plugin do arquivo browser_tabelas_plugin.py
    from .browser_tabelas_plugin import BrowserTabelasPlugin
    return BrowserTabelasPlugin(iface)

