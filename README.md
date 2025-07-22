# API de Veículos com suporte a MCP

<p align="center">
  <a href="#dart-sobre">Sobre</a> &#xa0; | &#xa0;
  <a href="#rocket-principais-tecnologias">Tecnologias</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requisitos">Requisitos</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-instalacao">Instalação</a> &#xa0; | &#xa0;
  <a href="#spiral_notepad-exemplos">Exemplos</a>
</p>

## :dart: Sobre ##

API para buscar veículos em um Banco de Dados integrado com um servidor MCP para suporte a buscas em linguagem natural.


## :rocket: Principais Tecnologias ##

<a href="https://www.python.org/">
  <img width="50" title="Python" alt="Logo Python" src="https://icon.icepanel.io/Technology/svg/Python.svg">
</a> &#xa0; &#xa0;

<a href="https://fastapi.tiangolo.com/">
  <img width="50" title="FastAPI" alt="Logo FastAPI" src="https://icon.icepanel.io/Technology/svg/FastAPI.svg">
</a> &#xa0; &#xa0;

<a href="https://modelcontextprotocol.io/">
  <img width="50" title="Model Context Protocol (MCP)" alt="Logo MCP" src="https://avatars.githubusercontent.com/u/182288589?s=200&v=4">
</a> &#xa0; &#xa0;

<a href="https://claude.ai">
  <img width="50" title="Claude" alt="Logo Claude" src="https://images.seeklogo.com/logo-png/55/1/claude-logo-png_seeklogo-554534.png">
</a>

###

<details>
  <summary>Veja mais</summary>

  ###

  * [FastAPI-MCP](https://github.com/tadata-org/fastapi_mcp)
  * [SQLAlchemy](https://www.sqlalchemy.org/)
  * [SQLite](https://www.sqlite.org/)
  * [Faker](https://pypi.org/project/Faker/)
  * [pytest](https://docs.pytest.org/)
  * [OpenAI](https://openai.com)

</details>

## :white_check_mark: Requisitos ##

Ter [Git](https://git-scm.com) e [Python](https://nodejs.org/en/) acima da versão 3.13 instalado no seu sistema. ([pyenv](https://github.com/pyenv/pyenv) recomendado).

## :checkered_flag: Instalação ##

```bash
# Clone este projeto
$ git clone https://github.com/nelzonr/api-veiculos-mcp.git

# Acesse a pasta do projeto
$ cd api-veiculos-mcp

# Crie um ambiente virtual
$ python -m venv .venv

# Habilite o ambiente virtual
## MacOS e Linux
$ source .venv/bin/activate
## Windows
$ .venv\Scripts\activate

# Instale as bibliotecas do projetos
$ pip install -r requirements.txt

# Renomeie o arquivo .env.example para .env
## MacOS e Linux
$ mv .env.example .env
## Windows
$ ren .env.example .env

# Crie e popule o banco de dados
$ python -m src.utils.populate_veiculos

# Inicie o servidor <http://localhost:8000>
$ python src/api/server.py
```

## :robot: MCP Stdio ##

Use as configurações abaixo no seu MCP client para integrar a API com seu LLM favorito

```
{
  "servers": {
    "veiculos-mcp-stdio": {
      "type": "stdio",
      "command": "CAMINHO_ABSOLUTO_DA_PASTA_DO_PROJETO/api-veiculos-mcp/.venv/bin/python",
      "args": ["CAMINHO_ABSOLUTO_DA_PASTA_DO_PROJETO/api-veiculos-mcp/src/api/server.py"]
    }
  }
}
```

## :globe_with_meridians: MCP SSE - API Web ##

Use as configurações abaixo no seu MCP client para integrar a API com seu LLM favorito

```
{
  "servers": {
    "veiculos-mcp-sse": {
      "url": "http://localhost:8000/mcp",
      "type": "http"
    }
  }
}
```

## :spiral_notepad: Exemplos ##

* "Me mostre todos os veiculos da Ford em uma tabela com as colunas Marca, Modelo, Ano e Valor."

- "Liste todos os veiculos da Fiat."
- "Desses veiculos quero modelos apenas com ano acima de 2020."
- "Acima de 2015."

* "Liste veiculos de qualquer marca que custem menos de 50 mil."

- "Qual o veiculo mais barato e o mais caro da lista?"
