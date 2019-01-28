from datetime import date, datetime, timedelta
from odoo import models, fields, api, _

class MasterComponent(models.Model):
    _name = 'master.komponen'
    _description = 'Master Komponen'

    name = fields.Char('Nama Komponen')
    tipe_waktu = fields.Selection([('jam', 'Jam'), ('hari', 'Hari'), ('minggu', 'Minggu')], default='hari')
    waktu_pengerjaan = fields.Integer('Waktu Pengerjaan')

    def get_time_delta(self):
        if self.tipe_waktu == 'jam':
            return timedelta(hours=self.waktu_pengerjaan)
        elif self.tipe_waktu == 'hari':
            return timedelta(days=self.waktu_pengerjaan)
        elif self.tipe_waktu == 'minggu':
            return timedelta(weeks=self.waktu_pengerjaan)
        else:
            return timedelta(days=0)
