from odoo import fields, models


class ControleCombustivelTanque(models.Model):
    _name = "controle.combustivel.tanque"
    _description = "Tanque de Combustível"
    _order = "name"

    name = fields.Char(string="Tanque", required=True)
    capacidade = fields.Float(string="Capacidade (Litros)", default=6000.0, readonly=True)
    estoque_atual = fields.Float(string="Estoque Atual (Litros)", default=0.0)
