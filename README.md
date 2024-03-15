# Projeto Design Pattern

Este é um projeto incrível chamado Template Pattern que usa Docker para facilitar a execução da aplicação e dos testes.
Basicamente ele segue uma estrutura de repository pattern para alocar seus módulos.

Resumidamente, a aplicação possui:

- clientes
- lojas
- produtos
- histórico de compra


### Clientes:
Os clientes eles possuem nome e valor na conta, isto é adicionado quando é criado o cliente

### Lojas:
As lojas possuem nome e estado de abertura (Se elas estão abertas ou não)

### Produtos:
Os produtos precisam estar vinculado a uma loja, e possuem nome, quantidade atual, valor unitário

### Histórico de compra:
O histórico de compra precisa de um cliente, de uma loja, e de um produto e a quantidade comprada do produto

A finalidade do projeto não é "Criar um projeto de manipulação de itens e etc", isto foi apenas um contexto, o projeto
é para demonstrar como seria a utilização de uma organização baseada em um design de repositórios, onde neste contexto
os produtos conversam com a loja, a compra do cliente conversa com a loja, com o produto e com o cliente, desta forma
demonstrando como seriam esses relacionamentos.

A cobertura de testes unitários deste projeto se encontram em 91%, fiquem a vontade para melhorar os testes e lançar 
correções.

## Pré-requisitos

Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina.

- [Docker](https://docs.docker.com/get-docker/)

## Iniciando o Projeto

1. Clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/DanielXavierJob/RepositoryPatternProject
cd RepositoryPatternProject
```

2. Construa os contêineres Docker usando o Docker Compose:

```bash
docker compose build
```

## Executando Testes

Para executar os testes, você pode usar o comando a seguir:

```bash
docker compose run --rm test
```

Isso iniciará o contêiner de teste, executará os testes e exibirá os resultados no terminal.

## Executando a aplicação

Para executar a aplicação, você pode usar o comando a seguir:

```bash
docker compose up app
```
Caso queira deixar em segundo plano só adicioanr a flag ```-d``` ao final do bash
Isso iniciará o contêiner da aplicação.


## Encerrando o Projeto

Para parar os contêineres Docker em execução, você pode usar o seguinte comando:

```bash
docker compose down
```

Isso encerrará os contêineres e limpará os recursos utilizados.

## Contribuindo

Se você quiser contribuir para este projeto, sinta-se à vontade para fazer um fork e enviar pull requests. Agradecemos antecipadamente por suas contribuições!

```