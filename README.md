# Tabelas SCI para QGIS

## Descrição

Este é um plugin para o QGIS que permite aos usuários navegar por esquemas e tabelas em um banco de dados SQL Server específico (configurado como SCI) e adicionar tabelas que contêm colunas de geometria espacial (tipos `geometry` ou `geography`) diretamente como camadas vetoriais no QGIS.

O plugin apresenta uma árvore de navegação que começa com localidades pré-definidas, expande para os esquemas associados a essas localidades (baseado em um prefixo numérico) e, finalmente, lista as tabelas com geometria dentro de cada esquema selecionado.

## Versão

0.1

## Autor

* **Nome:** Carlos Borges
* **Email:** carlosborges2007edu@gmail.com

## Requisitos

* **QGIS:** Versão 3.0 ou superior.
* **Banco de Dados:** Acesso a uma instância do Microsoft SQL Server.
* **Driver ODBC:** Driver ODBC adequado para SQL Server instalado e configurado no sistema operacional.
* **Permissões:** Permissões de leitura no banco de dados SQL Server para listar esquemas (`sys.schemas`), tabelas (`INFORMATION_SCHEMA.TABLES`) e colunas (`INFORMATION_SCHEMA.COLUMNS`), além de permissões para ler os dados das tabelas espaciais a serem adicionadas. Conexão Confiável (Trusted Connection) deve estar habilitada ou as credenciais devem ser fornecidas (requer modificação do código).

## Instalação

1.  Baixe ou clone este repositório.
2.  Localize o diretório de plugins do seu QGIS. Você pode encontrá-lo no QGIS em `Configurações -> Perfis de Usuário -> Abrir Pasta do Perfil Ativo` e, em seguida, navegue até a pasta `python/plugins`.
3.  Copie a pasta inteira do plugin (a pasta que contém `__init__.py`, `metadata.txt`, etc.) para o diretório de plugins do QGIS.
4.  Inicie ou reinicie o QGIS.
5.  Vá em `Plugins -> Gerenciar e Instalar Plugins...`.
6.  Procure por "SCI" na aba "Instalados" e certifique-se de que a caixa de seleção está marcada para ativá-lo.

## Configuração Obrigatória

**Antes de usar o plugin, você PRECISA editar o arquivo `browser_dialog.py`:**

1.  Abra o arquivo `browser_dialog.py` em um editor de texto.
2.  Localize as seguintes linhas dentro do método `__init__`:
    ```python
    # --- ATENÇÃO: Substitua os placeholders abaixo pelas suas informações ---
    self.db_server_instance = "SEU_SERVIDOR\\SUA_INSTANCIA_SQL" # Ex: "10.100.100.48\sci"
    self.db_name = "SEU_BANCO_DE_DADOS" # Ex: "SCI"
    self.db_port = "1433" # Porta padrão do SQL Server, ajuste se necessário
    # --- Fim das informações sensíveis ---
    ```
3.  **Substitua** `"SEU_SERVIDOR\\SUA_INSTANCIA_SQL"` pelo nome ou IP do seu servidor SQL Server, incluindo a instância se necessário (ex: `"MEUSQLSERVER\\SQLEXPRESS"` ou `"192.168.0.10"`).
4.  **Substitua** `"SEU_BANCO_DE_DADOS"` pelo nome exato do banco de dados que você deseja acessar.
5.  Ajuste `self.db_port` se o seu SQL Server não estiver rodando na porta padrão `1433`.
6.  Verifique a string de conexão ODBC no método `conectar_sqlserver`. O padrão usa `Trusted_Connection=yes;`. Se você precisar usar um login SQL específico, altere essa parte da string para `UID=seu_usuario_sql;PWD=sua_senha_sql;`. **Atenção:** Armazenar senhas diretamente no código não é seguro. Considere métodos mais seguros se a conexão confiável não for uma opção.
7.  Salve o arquivo `browser_dialog.py`.

## Como Usar

1.  Após a instalação e configuração, você encontrará uma nova entrada de menu chamada "&SCI (Original)" (provavelmente dentro do menu "Plugins" ou "Banco de Dados") e/ou um ícone na barra de ferramentas do QGIS.
2.  Clique na ação do menu ou no ícone da barra de ferramentas para abrir a janela "Selecionar Tabela com Geometria".
3.  A janela exibirá as localidades pré-configuradas. Clique em uma localidade para carregar os esquemas associados.
4.  Clique em um esquema para carregar as tabelas que contêm colunas de geometria dentro desse esquema.
5.  Selecione a tabela desejada na árvore.
6.  Clique no botão "Adicionar Camada".
7.  Se a conexão for bem-sucedida e a tabela for válida, ela será adicionada como uma nova camada vetorial ao seu projeto QGIS.
