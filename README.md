# Controle de Combustível (Odoo 19) Módulo Odoo para **controle de abastecimentos**, **estoque de tanques** e **entrada de compras de combustível**, com regras automáticas de movimentação e **relatório PDF**.

---
## ✨ Funcionalidades

### ⛽ Abastecimentos - Registro de abastecimentos por **equipamento (Fleet)**. - Campos: data/hora, horímetro/odômetro, motorista, litros, valor por litro. - **Total calculado automaticamente** (litros × valor por litro). - **Baixa automática** do estoque do tanque ao salvar um abastecimento. - Ajuste automático do estoque ao **editar** ou **excluir** abastecimentos.

### 🛢️ Tanques - Cadastro de tanques com: - Nome - Capacidade (litros) - Estoque atual (litros) - Visualização rápida do estoque. 

### 🧾 Compras de combustível (entrada no estoque) - Registro de compras com: - Data - Tanque - Fornecedor - Litros comprados - Valor total - Fluxo simples por status: - **Rascunho → Confirmado** - Ao confirmar a compra: **soma os litros ao estoque do tanque**. 

### 🖨️ Relatório PDF - Botão **Imprimir** no abastecimento. - Gera PDF com dados principais do abastecimento: - data/hora, equipamento, tanque, motorista, horímetro/odômetro, litros, valores e total. 

---
## 🧠 Regras de Negócio 
### Regra 1 — Abastecimento baixa estoque Ao criar um abastecimento: - estoque_atual(tanque) = estoque_atual(tanque) - litros 
### Regra 2 — Compra aumenta estoque Ao confirmar uma compra: - estoque_atual(tanque) = estoque_atual(tanque) + litros_comprados 
### Regra 3 — Segurança de estoque - Não permite abastecimento que deixe o tanque com estoque negativo.

---
## 🧪 Como testar (passo a passo) 1. Criar 1 tanque: - Nome: Tanque Principal - Estoque Atual: 6000 2. Criar 1 abastecimento: - Tanque: Tanque Principal - Litros: 50 - Valor por Litro: 6,00 (exemplo) - Salvar ✅ Volte no tanque: deve ficar 5950. 3. Criar 1 compra: - Tanque: Tanque Principal - Litros Comprados: 200 - Status: **Confirmar** ✅ Volte no tanque: deve somar 200 litros. 

---
## 🧩 Dependências - base - fleet 

--- 
## 🚀 Instalação 1. Copie o módulo para o caminho de addons. 2. Reinicie o Odoo. 3. No Odoo: **Apps → Atualizar lista de Apps** 4. Procure por: **Controle de Combustível** 5. Instale. 

---
## 📂 Estrutura do módulo - models/ - tanque.py - abastecimento.py - compra.py - views/ - menus + telas (list/form) - security/ - grupos e permissões - reports/ - template QWeb e action de relatório 

--- 
## 🔮 Integração futura com Compras Este projeto já possui o conceito de “Compra de combustível” para entrada no estoque. Próximos passos possíveis: - Integrar com o app nativo **Purchase**: - gerar compra (PO) com produto “Combustível” - ao receber (Receipt), atualizar o tanque automaticamente - Integração com **Stock Picking** (recebimento) e rastreabilidade - Multi-tanque e multi-empresa 

--- 
## 📸 Prints sugeridos para o GitHub - Menu do app com: Tanques, Abastecimentos e Compras - Tela de tanque mostrando estoque - Abastecimento mostrando baixa automática - Compra confirmada aumentando estoque - PDF gerado pelo botão “Imprimir” 

--- 
## 👤 Autor - Alexandre Jacques
