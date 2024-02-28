# Movie Review API

Este é um projeto de API para consulta de informações sobre filmes, seguindo os requisitos fornecidos pelo desafio "Pessoa Desenvolvedora .NET" porem adaptado para o ecossistema python. A API permite operações de cadastro, edição, exclusão lógica de usuários e filmes, além de consultas filtradas e ordenadas.

## Requisitos

- Docker
- Git

## Executando o Projeto

1. Clone este repositório:

    ```bash
    git clone https://github.com/VictorSnt/Code-Review_Rating_Movies.git Rating_Movies
    cd Rating_Movies
    ```

2. Copie o arquivo de exemplo `.env.example` e renomeie para `.env`, ajustando os valores das variáveis conforme necessário:

    ```bash
    cp .env.example .env
    ```

3. Construa e execute o contêiner Docker:

    ```bash
    docker-compose up --build
    ```

4. Após o contêiner estar em execução, abra outro terminal e execute os testes:

    ```bash
    docker exec -it <nome_do_servico_docker|default:movie_review_api> python manage.py test
    ```

5. Após os testes passarem com sucesso, crie um super usuário:

    ```bash
    docker exec -it <nome_do_servico_docker|default:movie_review_api> python manage.py createsuperuser
    ```

6. Agora você pode acessar a documentação da API em:

    ```
    http://127.0.0.1:8000/api/docs
    ```

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

- `api/`: Contém os arquivos do Django Ninja que implementam a lógica da API.
- `data/`: Configurações do Django, como configuração de banco de dados, arquivos de ambiente, etc.
- `api/core`: Configurações de projeto padrão Django, settings.py, urls.py etc.
- `api/movie_review/`: App principal com todos arquivos que compõe a api.
- `api/movie_review/tests/`: Testes unitários para garantir a integridade da aplicação.
- `Dockerfile`: Arquivo para construir a imagem Docker da aplicação.
- `docker-compose.yml`: Arquivo para orquestrar a execução do contêiner Docker.



