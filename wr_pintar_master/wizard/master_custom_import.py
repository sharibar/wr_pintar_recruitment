# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, sql_db
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError
import tempfile
import base64
from datetime import datetime
import xlrd
from xlrd import open_workbook
import threading


class MasterCustomImport(models.TransientModel):
    _name = 'master.custom.import'

    xls_file = fields.Binary("Import")
    datas_file = fields.Char('Filename')

    def import_xls(self):
        datafile = self.xls_file
        file_name = str(self.datas_file)
        if not datafile:
            raise UserError('File Masih Kosong!')
        try:
            book = xlrd.open_workbook(file_contents=base64.decodebytes(self.xls_file))
        except xlrd.XLRDError as e:
            raise UserError('Tolong hanya upload file xlsx saja, Terima Kasih')
        header = {}
        sheet = book.sheet_by_index(0)

        #get header
        for col in range(sheet.ncols):
            if sheet.cell_value(0, col) == 'Nama Item':
                header['name'] = col
            elif sheet.cell_value(0, col) == 'Tanggal Mulai Pengerjaan':
                header['tanggal_mulai'] = col
            elif sheet.cell_value(0, col) == 'Nama Komponen':
                header['komponen.name'] = col
            elif sheet.cell_value(0, col) == 'Waktu Pengerjaan Komponen':
                header['komponen.waktu_pengerjaan'] = col
            elif sheet.cell_value(0, col) == 'Tipe Waktu':
                header['komponen.tipe_waktu'] = col
            elif sheet.cell_value(0, col) == 'Bobot Presentase Komponen':
                header['line_ids.percentage'] = col

        all_vals = []
        last_item = -1
        for row in range(sheet.nrows):
            if row == 0:
                continue
            vals = {}
            if sheet.cell_value(row, header['name']):
                vals['name'] = sheet.cell_value(row, header['name'])
                if sheet.cell_value(row, header['tanggal_mulai']):
                    exceltime = sheet.cell_value(row, header['tanggal_mulai'])
                    time_tuple = xlrd.xldate_as_tuple(exceltime, 0)
                    date_py = datetime(*time_tuple)
                    date_str = date_py.strftime(DEFAULT_SERVER_DATE_FORMAT)
                    vals['tanggal_mulai'] = date_str

            komponen = self.env['master.komponen'].search(
                [('name', '=', sheet.cell_value(row, header['komponen.name']))])
            komponen = komponen[0] if komponen else False

            if not komponen:
                komponen = self.env['master.komponen'].create({
                    'name': sheet.cell_value(row, header['komponen.name']) if header['komponen.name'] else False,
                    'tipe_waktu': sheet.cell_value(row, header['komponen.tipe_waktu']) if header['komponen.tipe_waktu'] else 'hari',
                    'waktu_pengerjaan': sheet.cell_value(row, header['komponen.waktu_pengerjaan']) if header['komponen.waktu_pengerjaan'] else False
                })
            else:
                komponen.write({
                    'tipe_waktu': sheet.cell_value(row, header['komponen.tipe_waktu']) if header['komponen.tipe_waktu'] else komponen.tipe_waktu,
                    'waktu_pengerjaan': int(sheet.cell_value(row, header['komponen.waktu_pengerjaan'])) if header['komponen.waktu_pengerjaan'] else komponen.waktu_pengerjaan,
                })

            if vals:
                line_ids = [(0, 0, {
                    'komponen': komponen.id,
                    'percentage': int(sheet.cell_value(row, header['line_ids.percentage'])) * 100 if header['line_ids.percentage'] else 0
                })]
                vals['line_ids'] = line_ids
                last_item += 1
                all_vals.append(vals)
            else:
                vals = all_vals[last_item]
                line_ids = vals.get('line_ids', [])
                line_ids.append((0, 0, {
                    'komponen': komponen.id,
                    'percentage': int(sheet.cell_value(row, header['line_ids.percentage']) * 100 if header['line_ids.percentage'] else 0)
                }))
                vals['line_ids'] = line_ids
                all_vals[last_item] = vals

        for rec in all_vals:
            res = self.env['master.item'].create(rec)

        action = self.env.ref('wr_pintar_master.action_master_item').read()[0]
        return action







