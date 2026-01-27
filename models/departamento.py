from odoo import models, fields

class Departamento(models.Model):
    _inherit = "hr.department"
    _description = 'Departamento - reto1_incidencias'

    descripcion = fields.Text(string="Descripción")


    incidencia_ids = fields.One2many(
        'reto1_incidencias.incidencia',
        'id_departamento',
        string='Incidencias del Departamento'
    )