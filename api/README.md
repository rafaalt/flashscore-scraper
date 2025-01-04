# Documentação da API

- [Documentação da API](#documentação-da-api)
  - [Visão Geral](#visão-geral)
  - [Tipos](#tipos)
    - [Jogo](#jogo)
    - [Time](#time)
    - [Estádio](#estádio)
  - [Base URL](#base-url)
  - [Resposta Padrão](#resposta-padrão)
  - [Endpoints](#endpoints)
    - [Get Last Games](#get-last-games)
    - [Get My Games](#get-my-games)
    - [Save Game](#save-game)
    - [Delete Game](#delete-game)


## Visão Geral

A API fornece dados de partidas, incluindo o resultado, campeonato, estádio, público presente e o árbitro da partida. Este guia de referência cobre os principais endpoints, parâmetros e formatos de resposta.

## Tipos

Para essa api algumas respostas estão formatadas nos seguintes tipos:

### Jogo

| Atributo         | Obrigatoriedade | Tipo     | Descrição                                |
|------------------|-----------------|----------|------------------------------------------|
| id               | Obrigatório     | String   | Identificador único da partida           |
| homeTeam         | Obrigatório     | String   | Nome do time da casa                     |
| awayTeam         | Obrigatório     | String   | Nome do time visitante                   |
| scoreHome        | Obrigatório     | Int      | Gols do time da casa                     |
| scoreAway        | Obrigatório     | Int      | Gols do time visitante                   |
| pointsHome       | Obrigatório     | Int      | Pontos do time da casa                   |
| pointsAway       | Obrigatório     | Int      | Pontos do time visitante                 |
| referee          | Opcional        | String   | Nome do árbitro                          |
| stadium          | Opcional        | String   | Nome do estádio                          |
| capacity         | Opcional        | Int      | Capacidade do estádio                    |
| publicPresent    | Opcional        | Int      | Público presente na partida              |
| homeTeamImage    | Obrigatório     | String   | URL da imagem do time da casa            |
| awayTeamImage    | Obrigatório     | String   | URL da imagem do time visitante          |
| date             | Obrigatório     | String   | Data do jogo                             |
| time             | Obrigatório     | String   | Horário do jogo                          |
| country          | Obrigatório     | String   | País onde ocorre o campeonato            |
| round            | Obrigatório     | String   | Rodada do campeonato                     |

### Time

| Atributo         | Obrigatoriedade | Tipo     | Descrição                                |
|------------------|-----------------|----------|------------------------------------------|
| team             | Obrigatório     | String   | Nome do Time                             |
| country          | Obrigatório     | String   | País do Time                             |

### Estádio

| Atributo         | Obrigatoriedade | Tipo     | Descrição                                |
|------------------|-----------------|----------|------------------------------------------|
| stadium          | Obrigatório     | String   | Nome do Estádio                          |
| city             | Obrigatório     | String   | Cidade do Estádio                        |
| capacity         | Opcional        | Int      | Capacidade do Estádio                    |

## Base URL
```http
http://localhost:3000/
```

## Resposta Padrão

A Api segue um formato de resposta paginada padrão. Seguindo o seguinte modelo de resposta:

| Campo        | Tipo               | Descrição                           | Valor Padrão |
|--------------|--------------------|-------------------------------------|:------------:|
| currentPage  | Int                | Página atual da busca               | |
| totalPages   | Int                | Total de páginas para a busca atual | |
| totalItems   | Int                | Total de itens retornados na busca  | |
| itemsPerPage | Int                | Número de Itens por página          | 20 |
| result       | Array do tipo Data | Resultado da busca da página atual  | |

**Exemplo:**

```json
{
  "currentPage": 1,
  "totalPages": 51,
  "totalItems": 1014,
  "itemsPerPage": 20,
  "results": [

  ]
}
```

## Endpoints

### Get Last Games

Obtém os últimos jogos do ano de todas as competições salvas no banco de dados, ordedando pelo jogo mais recente.

**Endpoint**

**GET /lastGames**

**Request**

Tabela de Parâmetros:

| Parâmetro | Tipo | Obrigatoriedade | Valor Padrão | Descrição                  |
|-----------|------|-----------------|--------------|----------------------------|
| page      | Int  | Opcional        | 1            | Número da página atual     |
| limit     | Int  | Opcional        | 20           | Número de itens por página |

Exemplo de Request:

```http
http://localhost:3000/lastGames?page=2
```
**Response**

| Campo        | Tipo               | Descrição                           |
|--------------|--------------------|-------------------------------------|
| currentPage  | Int                | Página atual da busca               |
| totalPages   | Int                | Total de páginas para a busca atual |
| totalItems   | Int                | Total de itens retornados na busca  |
| itemsPerPage | Int                | Número de Itens por página          |
| result       | Array do tipo [Jogo](#jogo) | Resultado da busca da página atual  |

### Get My Games

Obtém os jogos salvos pelo usuário

**Endpoint**

**GET /myGames**

**Request**

Tabela de Parâmetros:

| Parâmetro | Tipo | Obrigatoriedade | Valor Padrão | Descrição                  |
|-----------|------|-----------------|--------------|----------------------------|
| page      | Int  | Opcional        | 1            | Número da página atual     |
| limit     | Int  | Opcional        | 20           | Número de itens por página |

Exemplo de Request:

```http
http://localhost:3000/myGames?limit=10
```
**Response**

| Campo        | Tipo               | Descrição                           |
|--------------|--------------------|-------------------------------------|
| currentPage  | Int                | Página atual da busca               |
| totalPages   | Int                | Total de páginas para a busca atual |
| totalItems   | Int                | Total de itens retornados na busca  |
| itemsPerPage | Int                | Número de Itens por página          |
| result       | Array do tipo [Jogo](#jogo) | Resultado da busca da página atual  |

### Save Game

Salva determinado jogo na lista de jogos salvos do usuário.

**Endpoint**

**POST /save**

**Request**

Body:

Data do tipo [Jogo](#jogo) que será o elemento salvo na planilha do usuário.

Exemplo
```json
{
    "id": "61ofp0zQ",
    "homeTeam": "Cruzeiro",
    "homeTeamImage": "https://static.flashscore.com/res/image/data/lCWrxmg5-SjJmyx86.png",
    "awayTeam": "CSA",
    "awayTeamImage": "https://static.flashscore.com/res/image/data/UPX8Hag5-tQk41rnG.png",
    "scoreHome": 3,
    "scoreAway": 2,
    "pointsHome": 3,
    "pointsAway": 0,
    "referee": "Goncalves Lima J. (Bra)",
    "stadium": "Mineirão (Belo Horizonte)",
    "capacity": "61927",
    "public": "61291",
    "date": "06/11/2022",
    "time": "18:30",
    "country": "BRASIL",
    "round": "SÉRIE B - RODADA 38"
}
```

Exemplo de Request:

```http
http://localhost:3000/save
```

**Response**

| Campo        | Tipo               |
|--------------|--------------------|
| Message      | String             |

### Delete Game

Deleta determinado jogo da lista de jogos salvos do usuário.

**Endpoint**

**DELETE /delete/:id**

**Request**

O id no campo será o id do que vai ser removido

Exemplo
```http
http://localhost:3000/delete/61ofp0zQ
```

**Response**

| Campo        | Tipo               |
|--------------|--------------------|
| Message      | String             |