from odoo import fields, models
from odoo.exceptions import UserError


class ControleCombustivelCompra(models.Model):
    _name = "controle.combustivel.compra"
    _description = "Compra de Combustível"
    _order = "data desc, id desc"

    data = fields.Date(
        string="Data",
        default=fields.Date.context_today,
        required=True,
    )

    tanque_id = fields.Many2one(
        "controle.combustivel.tanque",
        string="Tanque",
        required=True,
    )

    fornecedor_id = fields.Many2one(
        "res.partner",
        string="Fornecedor",
    )

    litros = fields.Float(
        string="Litros Comprados",
        required=True,
    )

    valor_total = fields.Monetary(
        string="Valor Total",
        currency_field="currency_id",
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Moeda",
        default=lambda self: self.env.company.currency_id.id,
        readonly=True,
    )

    usuario_responsavel_id = fields.Many2one(
        "res.users",
        string="Usuário Responsável",
        default=lambda self: self.env.user,
        readonly=True,
    )

    state = fields.Selection(
        [
            ("draft", "Rascunho"),
            ("confirmado", "Confirmado"),
        ],
        string="Status",
        default="draft",
        required=True,
    )

    def action_confirmar(self):
        for rec in self:
            if rec.state == "confirmado":
                raise UserError("Esta compra já está confirmada.")

            if rec.litros <= 0:
                raise UserError("A quantidade de litros deve ser maior que zero.")

            tanque = rec.tanque_id
            novo_estoque = (tanque.estoque_atual or 0.0) + rec.litros
            tanque.sudo().write({"estoque_atual": novo_estoque})

            rec.state = "confirmado"
