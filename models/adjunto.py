from odoo import fields, models

class adjunto(models.Model):
    _name = 'reto1_incidencias.adjunto'
    _description = 'Adjunto'

    id_adjunto = fields.Integer(string='ID Adjunto')
    nombre_archivo = fields.Char(string='Nombre Archivo', required=True)
    ruta_archivo = fields.Char(string='Ruta Archivo')
    fecha_subida = fields.Datetime(
        string='Fecha Subida',
        default=fields.Datetime.now,
        readonly=True
    )
    id_comentario = fields.Many2one(
        'reto1_incidencias.comentario',
        string='Comentario',
        ondelete='cascade'
    )
    id_incidencia = fields.Many2one('reto1_incidencias.incidencia', string='Incidencia', ondelete='cascade')