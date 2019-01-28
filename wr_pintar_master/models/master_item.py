from datetime import date, datetime, timedelta
from odoo import fields, api, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class MasterItem(models.Model):
    _name = 'master.item'
    _description = 'Master Item'

    name = fields.Char('Nama Item')
    tanggal_mulai = fields.Datetime('Tanggal Mulai Pengerjaan')
    line_ids = fields.One2many('master.item.line', 'item_id', 'Master Item Line ')
    tanggal_selesai = fields.Datetime('Real Tanggal Selesai')
    ekspektasi_selesai = fields.Datetime('Ekspektasi Tanggal Selesai', compute='_compute_tgl_selesai')

    @api.onchange('line_ids.percentage')
    def check_percentage(self):
        if self.line_ids:
            all_bobot = self.line_ids.mapped('percentage')
            all_bobot = sum(all_bobot)
            if all_bobot > 100.0:
                raise UserError('Total Bobot Persentase tidak boleh lebih dari 100%')

    def _compute_tgl_selesai(self):
        for rec in self:
            all_komponen = rec.line_ids.mapped('komponen') if rec.line_ids else []
            delta = timedelta(days=0)

            for komponen in all_komponen:
                delta += komponen.get_time_delta()

            if rec.tanggal_mulai:
                date_ekspektasi = datetime.strptime(rec.tanggal_mulai, DEFAULT_SERVER_DATETIME_FORMAT)
                rec.ekspektasi_selesai = (date_ekspektasi + delta).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            else:
                rec.ekspektasi_selesai = False


class MasterItemLine(models.Model):
    _name = 'master.item.line'
    _description = 'Master Item Line'

    komponen = fields.Many2one('master.komponen', 'Komponen')
    percentage = fields.Float('Bobot Percentage')
    item_id = fields.Many2one('master.item', 'Items')









