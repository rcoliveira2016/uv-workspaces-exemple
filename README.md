# Monorepo com Python usando `uv` no VS Code

## Objetivo

Demonstrar como criar um **monorepo** em Python utilizando o [uv](https://github.com/astral-sh/uv), garantindo funcionamento adequado no **VS Code** e permitindo o compartilhamento de bibliotecas entre projetos do mesmo workspace.

---

## Passo a Passo

### 1. Inicializar o Workspace

```bash
uv init --bare
```

Cria um **workspace vazio** sem um projeto Python específico, apenas com a estrutura inicial e o arquivo `pyproject.toml` raiz.

```bash
uv sync
```

Cria e prepara o ambiente virtual (`.venv`) na raiz, instalando as dependências listadas no `pyproject.toml` (nesse momento, ainda não há nenhuma).

---

> **Observação:** No VS Code, se o nome da pasta do projeto for igual ao nome da biblioteca Python, podem ocorrer conflitos de importação.
> Por isso, é recomendado dar nomes diferentes para a pasta e para o pacote Python.

```bash
uv init monorepo_lib_core --name monorepo_core
uv init monorepo_cli
uv init monorepo_api
uv sync
```

---

### 2. Configurar o VS Code

1. Instale a extensão [**Python Envy**](https://marketplace.visualstudio.com/items?itemName=teticio.python-envy) para facilitar a seleção do ambiente virtual correto.

2. Crie o arquivo `.vscode/settings.json` na raiz do projeto:

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "pythonEnvy.venvName": ".venv"
}
```

* Essa configuração informa à extensão **Python Envy** para usar o ambiente virtual `.venv` criado pelo `uv` na raiz do monorepo.
* Sem essa configuração, o VS Code pode tentar criar ou usar ambientes diferentes para cada pasta.

---

### 3. Configurar o `pyproject.toml` da raiz

No arquivo `pyproject.toml` **da raiz**, adicione (ou confirme) a configuração do workspace:

```toml
[tool.uv.workspace]
members = [
    "monorepo_lib_core",
    "monorepo_cli",
    "monorepo_api"
]
```

Isso informa ao `uv` que esses três projetos fazem parte do mesmo workspace e podem compartilhar dependências e código.

---

Claro. Aqui está uma versão mais detalhada e clara da seção **4. Adicionar a biblioteca `monorepo_core` como dependência**, enfatizando sua importância e explicando o papel de cada configuração para facilitar o entendimento do usuário final:

---

### 4. Adicionar a biblioteca `monorepo_core` como dependência

Esta etapa é fundamental para que os projetos `monorepo_api` e `monorepo_cli` possam **usar o código da biblioteca compartilhada** `monorepo_core`, que está no pacote `monorepo_lib_core`.

Para isso, em cada projeto que precisa usar a biblioteca (exemplo: `monorepo_api` e `monorepo_cli`), você deve modificar o arquivo `pyproject.toml` incluindo:

```toml
dependencies = [
    "monorepo_core"
]

[tool.uv.sources]
monorepo-core = { workspace = true }
```

#### Explicação detalhada:

* **`dependencies = ["monorepo_core"]`**
  Informa ao `uv` e ao gerenciador de pacotes que este projeto depende do pacote `monorepo_core`. Isso faz com que, ao instalar dependências, ele procure e habilite o uso dessa biblioteca.

* **`[tool.uv.sources]` com `monorepo-core = { workspace = true }`**
  Essa configuração é essencial para que o `uv` entenda que a dependência `monorepo_core` **não deve ser buscada no PyPI ou em outro repositório externo**, mas sim **resolvida localmente dentro do próprio workspace**.
  Ou seja, o código fonte da biblioteca está presente localmente, no diretório `monorepo_lib_core`, e deve ser usado diretamente, facilitando desenvolvimento integrado e testes locais.

#### Por que isso é importante?

Sem essa configuração, ao rodar `uv sync` ou tentar executar os projetos, o `uv` não saberá onde encontrar o pacote `monorepo_core` e a importação falhará, pois ele procuraria por ele no PyPI (onde não existe) ou em outro repositório remoto.

Ao indicar que a origem da biblioteca está no **workspace local**, você garante:

* Desenvolvimento ágil, com mudanças na biblioteca refletidas imediatamente nos projetos que a usam.
* Ambiente consistente, com todas as dependências controladas dentro do monorepo.
* Facilidade para o VS Code e outras ferramentas resolverem as referências internas.

---

### 5. Sincronizar todos os pacotes

```bash
uv sync --all-packages
```

* Atualiza o ambiente virtual de todos os projetos do workspace.
* Necessário após adicionar novas dependências ou fontes no `pyproject.toml`.

---

### 6. Testar a execução

```bash
uv --project monorepo_cli run monorepo_cli/main.py
```

* `--project monorepo_cli` indica qual projeto rodar.
* `run monorepo_cli/main.py` executa o arquivo principal do CLI, garantindo que ele importe `monorepo_core` corretamente a partir do workspace.

---

### 7. Simplificar a execução com o Taskipy

Para simplificar a execução de comandos complexos, como o comando para rodar a API, podemos usar a ferramenta **Taskipy**.

#### Instalação do Taskipy

Para instalar a ferramenta no ambiente de desenvolvimento, utilize o seguinte comando:

```bash
uv add --dev taskipy
```

#### Configuração no `pyproject.toml`

Adicione a seção `[tool.taskipy.tasks]` no arquivo `pyproject.toml` da raiz. Cada chave dentro dessa seção representa o nome de um comando (ou "task") que você deseja criar.

```toml
[tool.taskipy.tasks]
run-api = "uv --project monorepo_api run uvicorn monorepo_api.main:app --reload"
```

  * **`run-api`**: É o nome do comando que você vai executar. Você pode escolher qualquer nome que faça sentido.
  * **`"uv --project monorepo_api run uvicorn monorepo_api.main:app --reload"`**: É o comando real que será executado quando você chamar `run-api`.

#### Como usar o Taskipy

Agora, em vez de digitar o comando longo toda vez, você pode simplesmente usar o `uv run` para executar a task que você definiu:

```bash
uv run task run-api
```

Isso torna a execução de comandos comuns mais rápida, menos propensa a erros de digitação e padroniza o fluxo de trabalho para todos os desenvolvedores no projeto.

-----

## Estrutura de Pastas

```plaintext
monorepo/
├── .vscode/
│   └── settings.json
├── monorepo_lib_core/        # Pasta do pacote principal (nome diferente do módulo Python)
│   ├── main.py               # Código fonte da biblioteca
│   └── pyproject.toml
├── monorepo_cli/             # Projeto CLI
│   ├── main.py               # Código fonte do CLI
│   └── pyproject.toml
├── monorepo_api/             # Projeto API
│   ├── main.py               # Código fonte da API
│   └── pyproject.toml
├── pyproject.toml            # Configuração principal do workspace
```
