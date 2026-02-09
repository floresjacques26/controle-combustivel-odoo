from odoo import api, fields, models
from odoo.exceptions import UserError


class ControleCombustivelAbastecimento(models.Model):
    _name = "controle.combustivel.abastecimento"
    _description = "Abastecimento"
    _order = "data_hora desc, id desc"

    equipamento_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Equipamento/Placa",
        required=True,
    )
    data_hora = fields.Datetime(string="Data e Hora", default=fields.Datetime.now, required=True)

    horimetro_odometro = fields.Float(string="Horímetro/Odômetro", digits=(16, 2))

    tanque_id = fields.Many2one(
        comodel_name="controle.combustivel.tanque",
        string="Tanque",
        required=True,
    )

    litros = fields.Float(string="Litros", digits=(16, 2), required=True, default=0.0)
    valor_por_litro = fields.Float(string="Valor por Litro", digits=(16, 2), required=True, default=0.0)

    total = fields.Monetary(
        string="Total",
        currency_field="currency_id",
        compute="_compute_total",
        store=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Moeda",
        default=lambda self: self.env.company.currency_id.id,
        readonly=True,
    )

    motorista_id = fields.Many2one("res.partner", string="Motorista")
    usuario_responsavel_id = fields.Many2one(
        "res.users",
        string="Usuário Responsável",
        default=lambda self: self.env.user,
        readonly=True,
    )

    @api.depends("litros", "valor_por_litro")
    def _compute_total(self):
        for rec in self:
            rec.total = (rec.litros or 0.0) * (rec.valor_por_litro or 0.0)

    # -------------------------
    # REGRAS DE ESTOQUE (TANQUE)
    # -------------------------
    def _check_and_apply_stock(self, tanque, delta_litros):
        """
        delta_litros > 0  => vai consumir do tanque (baixar estoque)
        delta_litros < 0  => vai devolver ao tanque (aumentar estoque)
        """
        if not tanque:
            return

        novo_estoque = (tanque.estoque_atual or 0.0) - float(delta_litros)
        # Ex.: delta 50 -> estoque -50
        # Ex.: delta -10 -> estoque +10

        if novo_estoque < 0:
            raise UserError(
                f"Estoque insuficiente no tanque '{tanque.name}'. "
                f"Estoque atual: {tanque.estoque_atual:.2f} L."
            )

        tanque.sudo().write({"estoque_atual": novo_estoque})

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        # Ao criar, desconta litros do tanque
        for rec in records:
            if rec.tanque_id and rec.litros:
                rec._check_and_apply_stock(rec.tanque_id, rec.litros)

        return records

    def write(self, vals):
        # Guardar estado anterior para calcular diferença
        before = {
            rec.id: {
                "tanque_id": rec.tanque_id.id,
                "litros": rec.litros,
            }
            for rec in self
        }

        res = super().write(vals)

        # Depois de escrever, ajustar estoque pelo DELTA
        for rec in self:
            old = before.get(rec.id, {})
            old_tanque_id = old.get("tanque_id")
            old_litros = float(old.get("litros") or 0.0)

            new_tanque = rec.tanque_id
            new_litros = float(rec.litros or 0.0)

            # Caso 1: mudou tanque
            if old_tanque_id and old_tanque_id != new_tanque.id:
                old_tanque = self.env["controle.combustivel.tanque"].browse(old_tanque_id)
                # devolve litros ao tanque antigo
                if old_litros:
                    self._check_and_apply_stock(old_tanque, -old_litros)
                # consome do tanque novo
                if new_litros:
                    self._check_and_apply_stock(new_tanque, new_litros)

            # Caso 2: mesmo tanque, mudou litros
            else:
                delta = new_litros - old_litros
                # delta > 0 consome mais | delta < 0 devolve
                if delta and new_tanque:
                    self._check_and_apply_stock(new_tanque, delta)

        return res

    def unlink(self):
        # Ao apagar, devolve litros ao tanque
        for rec in self:
            if rec.tanque_id and rec.litros:
                rec._check_and_apply_stock(rec.tanque_id, -rec.litros)
        return super().unlink()
