from odoo import  fields, models, api

class Comentario(models.Model):
    _name = 'reto1_incidencias.comentario'
    _description = 'Comentario'
    _order = 'fecha desc'

    contenido = fields.Text(string='Contenido', required=True)
    fecha = fields.Datetime(string='Fecha',default=fields.Datetime.now,readonly=True)
    id_incidencia = fields.Many2one('reto1_incidencias.incidencia',string='Incidencia',required=True,ondelete='cascade')
    id_empleado = fields.Many2one('hr.employee',string='Autor', required=True)
    adjunto_ids = fields.One2many('reto1_incidencias.adjunto','id_comentario', string='Adjuntos')
    total_adjuntos = fields.Integer(string='Total Adjuntos', compute='_compute_total_adjuntos')

    @api.depends('adjunto_ids')
    def _compute_total_adjuntos(self):
        for record in self:
            record.total_adjuntos = len(record.adjunto_ids)