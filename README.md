# desafio-meta-backend
Os detalhes da solução estão disponíveis no [neste](descricao_solucao.pdf) arquivo.
## Instruções
1. Faça o clone do repositório do desafio:
    ```bash
    git clone https://github.com/DenysMenfredy/desafio-meta-backend
    ```
2. Entre no diretório do desafio:
    ```bash
    cd desafio-meta-backend
    ```
3. Utilize o docker para executar o desafio:
    
    3.1. Faça o build primeiro:
    ```bash
    docker build -t desafio-meta-backend .
    ```
    3.2. Execute o desafio:
    ```bash
    docker run -p 8000:8000 desafio-meta-backend
    ```
4. Executar sem o docker (opcional):

    4.1. Instale o Poetry
    ```bash
    pip install poetry
    ```
    4.2. Instale as dependências do projeto:
    ```bash
    poetry install
    ```
    4.3. Execute o desafio:
    ```bash
    python3 src.main:app --reload
    ```
5. Acesse o desafio no endereço:
    ```bash
    http://localhost:8000
    ```

- Para interagir com as rotas, acesse:
    ```bash
    http://localhost:8000/docs
    ```

## Usando a CLI para importar cards
1. Entre no diretório do desafio:
    ```bash
    cd desafio-meta-backend
    ```
2. Execute o comando:
    ```bash
    python src/import_cards.py -f <arquivo_cards.csv>
    ```
    - Deve se passar o caminho para o arquivo csv.