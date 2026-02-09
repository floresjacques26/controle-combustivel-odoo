⛽ Controle de Combustível – Odoo 19

Módulo Odoo desenvolvido para controle de abastecimentos, estoque de tanques e entrada de compras de combustível, com regras automáticas de movimentação e relatório PDF.

Projeto focado em boas práticas de ORM, regras de negócio no backend e estrutura modular escalável.

✨ Funcionalidades
⛽ Abastecimentos

Registro de abastecimentos por equipamento (Fleet)

Campos principais:

Data/Hora

Horímetro/Odômetro

Motorista

Litros

Valor por litro

Total calculado automaticamente (litros × valor por litro)

Baixa automática do estoque do tanque ao salvar

Ajuste automático do estoque ao editar ou excluir abastecimentos

🛢️ Tanques

Cadastro de tanques com:

Nome

Capacidade (litros)

Estoque atual (litros)

Visualização rápida do estoque disponível

🧾 Compras de Combustível (Entrada no Estoque)

Registro de compras com:

Data

Tanque

Fornecedor

Litros comprados

Valor total

Fluxo simples por status:

Rascunho → Confirmado

Ao confirmar a compra:

Soma automaticamente os litros ao estoque do tanque

🖨️ Relatório PDF

Botão Imprimir no abastecimento

Geração de PDF via QWeb com:

Data/Hora

Equipamento

Tanque

Motorista

Horímetro/Odômetro

Litros

Valor por litro

Total

🧠 Regras de Negócio
Regra 1 — Abastecimento baixa estoque

Ao criar um abastecimento:

estoque_atual(tanque) = estoque_atual(tanque) - litros

Regra 2 — Compra aumenta estoque

Ao confirmar uma compra:

estoque_atual(tanque) = estoque_atual(tanque) + litros_comprados

Regra 3 — Segurança de estoque

Não permite abastecimento que deixe o tanque com estoque negativo

Validação feita no backend (ORM)

🧪 Como Testar (Passo a Passo)
1️⃣ Criar um Tanque

Nome: Tanque Principal

Estoque Atual: 6000

2️⃣ Criar um Abastecimento

Tanque: Tanque Principal

Litros: 50

Valor por Litro: 6,00 (exemplo)

Salvar

✅ Estoque do tanque deve ficar 5950

3️⃣ Criar uma Compra

Tanque: Tanque Principal

Litros Comprados: 200

Status: Confirmar

✅ Estoque do tanque deve somar 200 litros

🧩 Dependências

base

fleet

🚀 Instalação

Copie o módulo para o diretório de addons do Odoo

Reinicie o Odoo

No Odoo:

Apps → Atualizar lista de Apps

Procure por: Controle de Combustível

Instale o módulo

📂 Estrutura do Módulo
controle_combustivel/
├── models/
│   ├── tanque.py
│   ├── abastecimento.py
│   └── compra.py
│
├── views/
│   ├── menus
│   ├── formulários
│   └── listas
│
├── security/
│   ├── grupos
│   └── permissões
│
├── reports/
│   ├── template QWeb
│   └── action de relatório PDF
│
└── README.md

🔮 Integrações Futuras (Proposta)

Integração com o módulo Purchase:

Geração de pedido de compra (PO) com produto Combustível

Atualização automática do tanque no recebimento (Receipt)

Integração com Stock Picking

Integração fiscal:

NF-e / NFS-e

Multi-tanque

Multi-empresa

Dashboard gerencial de consumo

👤 Autor

Alexandre Jacques
Projeto desenvolvido para fins técnicos, aprendizado e avaliação profissional em Odoo.
