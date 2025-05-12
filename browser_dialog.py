# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTreeView, QPushButton, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QModelIndex
from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject

class BrowserTabelasDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selecionar Tabela com Geometria")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()
        self.tree = QTreeView()
        layout.addWidget(self.tree)

        self.botao = QPushButton("Adicionar Camada")
        self.botao.clicked.connect(self.adicionar_camada)
        layout.addWidget(self.botao)

        self.setLayout(layout)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Localidades / Schemas / Tabelas'])
        self.tree.setModel(self.model)
        self.tree.expandAll()
        self.tree.clicked.connect(self.on_item_click)

        self.db_server_instance = "SEU_SERVIDOR\\SUA_INSTANCIA_SQL"
        self.db_name = "SEU_BANCO_DE_DADOS"
        self.db_port = "1433"
        self.db = self.conectar_sqlserver()
        if self.db:
            self.carregar_localidades()

    def conectar_sqlserver(self):
        connection_name = "meu_plugin_sql_server_conn" 
        if QSqlDatabase.contains(connection_name):
            db = QSqlDatabase.database(connection_name)
        else:
            db = QSqlDatabase.addDatabase("QODBC", connection_name)
        
        connection_string = (
            f"Driver={{SQL Server}};"
            f"Server={self.db_server_instance};"
            f"Database={self.db_name};"
            f"Trusted_Connection=yes;
        )
        db.setDatabaseName(connection_string)

        if not db.open():
            QMessageBox.critical(self, "Erro", f"Erro ao conectar ao banco:\n{db.lastError().text()}")
            return None
        return db

    def carregar_localidades(self):
        self.localidades = {
            'Dourados': '20',
            'Três Lagoas': '25',
            'Coxim': '30',
            'Jardim': '35',
            'Naviraí': '40',
            'Ponta Porã': '45',
            'Nova Andradina': '50',
            'Paranaíba': '55',
            'Corumbá': '60',
            'Aquidauana': '65',
        }
        for nome, prefixo in self.localidades.items():
            item = QStandardItem(nome)
            item.setData({'tipo': 'localidade', 'prefixo': prefixo})
            item.setEditable(False)
            self.model.appendRow(item)

    def on_item_click(self, index: QModelIndex):
        item = self.model.itemFromIndex(index)
        dados = item.data()
        if dados and dados.get('tipo') == 'localidade' and item.rowCount() == 0:
            self.carregar_schemas(item, dados['prefixo'])
        elif dados and dados.get('tipo') == 'schema' and item.rowCount() == 0:
            self.carregar_tabelas(item, dados['nome'])

    def carregar_schemas(self, item_localidade, prefixo):
        schemas = []
        query = QSqlQuery(self.db)
        query.prepare(f"SELECT name FROM sys.schemas WHERE name LIKE '{prefixo}%'")
        if query.exec():
            while query.next():
                schemas.append(query.value(0))
        else:
            QMessageBox.warning(self, "Erro Query Schemas", f"Erro ao buscar schemas: {query.lastError().text()}")


        for schema in schemas:
            schema_item = QStandardItem(schema)
            schema_item.setData({'tipo': 'schema', 'nome': schema})
            schema_item.setEditable(False)
            item_localidade.appendRow(schema_item)

    def carregar_tabelas(self, item_schema, schema_name):
        query = QSqlQuery(self.db)
        query.prepare(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{schema_name}'")
        if not query.exec():
            QMessageBox.warning(self, "Erro Query Tabelas", f"Erro ao buscar tabelas: {query.lastError().text()}")
            return

        while query.next():
            tabela = query.value(0)
            subquery = QSqlQuery(self.db)
            subquery.prepare(f"""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = '{schema_name}' AND TABLE_NAME = '{tabela}'
                AND DATA_TYPE IN ('geometry', 'geography')
            """)
            if subquery.exec() and subquery.next():
                geom_col_name_found = subquery.value(0)
                tabela_item = QStandardItem(tabela)
                tabela_item.setData({'tipo': 'tabela', 'schema': schema_name, 'tabela': tabela, 'geom_col': geom_col_name_found})
                tabela_item.setEditable(False)
                item_schema.appendRow(tabela_item)
            elif not subquery.isActive() and subquery.lastError().isValid():
                 QMessageBox.warning(self, "Erro Subquery Colunas", f"Erro ao verificar colunas de geometria: {subquery.lastError().text()}")


    def adicionar_camada(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Aviso", "Nenhum item selecionado.")
            return
            
        item = self.model.itemFromIndex(index)
        dados = item.data()

        if dados and dados.get('tipo') == 'tabela':
            schema = dados['schema']
            tabela = dados['tabela']
            geom_column_name = dados.get('geom_col', 'geom')

            uri = QgsDataSourceUri()
            
            uri.setConnection(self.db_server_instance, self.db_port, self.db_name, "", "") 
            
            uri.setDataSource(schema, tabela, geom_column_name)

            camada_nome_qgis = f"{schema}_{tabela}"
            camada = QgsVectorLayer(uri.uri(False), camada_nome_qgis, "mssql")
            
            if camada.isValid():
                QgsProject.instance().addMapLayer(camada)
                QMessageBox.information(self, "Sucesso", f"Camada '{camada_nome_qgis}' adicionada.")
            else:
                QMessageBox.warning(self, "Erro", f"Erro ao carregar camada: {camada_nome_qgis}\nDetalhes: {camada.error().message()}")
        else:
            QMessageBox.information(self, "Aviso", "Por favor, selecione uma tabela com geometria para adicionar.")

    def closeEvent(self, event):
        if self.db and self.db.isOpen():
            connection_name = self.db.connectionName()
            self.db.close()
            QSqlDatabase.removeDatabase(connection_name)
        super().closeEvent(event)

