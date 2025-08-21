# Ecommerce Management

Projeto de gerenciamento de estoque, pedidos e clientes com base em uma arquitetura orientada a objetos, com persistência em banco de dados SQLite, testes automatizados e futura exposição via API REST (Flask) com possibilidade de integração com uma interface local em Tkinter.

---

## Objetivo do Projeto

Desenvolver um sistema modular, orientado a objetos, para controle de estoque e pedidos de um e-commerce, respeitando princípios como SRP (Princípio da Responsabilidade Única), visando boa manutenibilidade, testabilidade e extensibilidade.

---

## Arquitetura do Projeto

O projeto é dividido em três camadas principais:

### Entity (Entidades)
Representam os objetos centrais do domínio do sistema, contendo atributos e validações básicas (ex: `Product`, `Order`, `Customer`, `ProductBatch`, etc).

### DAO (Data Access Object)
Camada responsável por toda a comunicação com o banco de dados. Cada entidade possui sua DAO específica para persistência, exclusão, atualização e consulta (ex: `ProductDAO`, `CustomerDAO`, etc).

### Service
Camada intermediária entre o DAO e a futura API. Contém regras de negócio, verificações adicionais e orquestração de chamadas entre entidades e o banco (ex: `ProductService`, `OrderService`, etc).

---

## 🧠 Mapa da Empatia — Cliente (Mercado Local)
**Quem é o cliente?**  
Um mercado de bairro que deseja digitalizar suas vendas por meio de um e-commerce próprio.  

- **O que pensa e sente?**  
  Quer expandir as vendas, facilitar a vida dos clientes e acompanhar concorrentes que já vendem online.  

- **O que vê?**  
  Clientes com rotinas corridas, muitas vezes sem tempo de ir até o mercado. Concorrência com apps de entrega já consolidados.  

- **O que fala e faz?**  
  Reclama da dificuldade de gerenciar estoque manualmente e do alcance limitado das vendas físicas. Demonstra interesse em usar tecnologia como diferencial competitivo.  

- **O que ouve?**  
  Feedback dos clientes pedindo maior praticidade. Conversas com outros comerciantes sobre digitalização e delivery.  

- **Dores (problemas):**  
  - Perda de clientes para aplicativos de entrega concorrentes.  
  - Estoque desorganizado e falta de integração entre vendas físicas e digitais.  
  - Custos com sistemas complexos e pouco acessíveis.  

- **Ganhos (o que deseja conquistar):**  
  - Plataforma simples para gerenciar estoque e pedidos.  
  - Fidelização de clientes com praticidade e atendimento diferenciado.  
  - Aumento no faturamento com vendas online.  

---

## Funcionalidades já implementadas

### Entidades implementadas:
- `Address`
- `Category`
- `Customer`
- `Date`
- `Order`
- `OrderItem`
- `OrderItemBatch`
- `Payment`
- `Product`
- `ProductBatch`

### DAOs implementadas:
- Superclasse `BaseDAO`
- `CategoryDAO`
- `CustomerDAO`
- `OrderDAO`
- `OrderItemBatchDAO`
- `OrderItemDAO`
- `PaymentDAO`
- `ProductBatchDAO`
- `ProductDAO`

### Testes implementados:
- Testes automatizados para as entidades acima
- Testes para os DAOs `ProductDAO`, `CategoryDAO`, `ProductBatchDAO`
- Menu interativo para executar os testes (`test.py`)

---

## Funcionalidades pendentes

### DAOs a implementar:
- `CustomerDAO`
- `OrderDAO`
- `OrderItemDAO`
- `OrderItemBatchDAO`
- `PaymentDAO`

### Services a implementar:
- (possível) Superclasse `BaseService`
- `CategoryService`
- `CustomerService`
- `IventoryService`
- `OrderItemBatchService`
- `OrderItemService`
- `OrderService`
- `PaymentService`
- `ProductBatchService`
- `ProductService`
- (possível) `ReportService`

---

## Próximos passos do projeto

Após a finalização de todas as classes `Service`, o projeto seguirá para a camada de interface externa com API REST e posteriormente com GUI. A seguir, o roadmap:

### 1. Criar rotas Flask
Criação de rotas RESTful em `api/*.py` com endpoints para CRUD e listagem com filtros.

### 2. Criar o `app.py` principal
Arquivo principal da aplicação Flask, que registra todas as rotas.

### 3. Integrar os Services nas rotas
Cada rota chamará o respectivo método da camada `Service`.

### 4. Testar a API com Postman
Testar endpoints `GET`, `POST`, `DELETE`, etc., simulando o uso real.

### 5. Tratar erros e validar dados
Captura de exceções nos endpoints e retorno de mensagens HTTP apropriadas.

### 6. Adicionar documentação da API
Documentar os endpoints usando `README`, Swagger ou outro recurso.

### 7. Desenvolver uma interface via aplicação web
Criação de uma interface acessível por navegador, permitindo o uso remoto e intuitivo do sistema.

---

## Estrutura do Projeto

```
ecommerce_management/
├── app.py                  # Entrada principal da API (a ser feito)
├── api/                    # Rotas Flask (a ser feito)
│   └── product_routes.py
├── dao/                    # DAOs com acesso ao SQLite
├── entities/               # Classes de domínio
├── services/               # Lógica de negócio
├── tests/                  # Testes
├── utils/                  # Validações e funções auxiliares
├── banco.py                # Criação e conexão com o banco
└── test.py                 # Menu interativo para testes
```

---

## Como rodar os testes atuais

1. Execute o script principal de testes:
```bash
python test.py
```

2. Escolha a opção desejada no menu (testar entidades, DAOs, ou todas as classes).

---

## Requisitos e dependências

- Python 3.10+
- SQLite (já embutido no Python)
- Flask (apenas necessário para a API futura):
```bash
pip install flask
```

---

## Membros

Júlia Coelho Rodrigues  (Líder e Desenvolvedora BackEnd)

Ricardo Souza Moraes    (Analista de Dados e Tester)

Maria Eduarda Jardim    (Desenvolvedora FrontEnd e Documentadora)

Letícia Mascarenhas     (Desenvolvedora FrontEnd)

Victor Ritcheli         (Desenvolvedor BackEnd)
