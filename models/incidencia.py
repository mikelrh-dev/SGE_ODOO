from odoo import fields, models, api


class Incidencia(models.Model):
    _name = 'reto1_incidencias.incidencia'
    _description = 'Información de la Incidencia'
    _rec_name = 'titulo'

    titulo = fields.Char(string="Título", required=True)
    descripcion = fields.Text(string="Descripción")
    fecha_creacion = fields.Datetime(string="Fecha de Creación", default=fields.Datetime.now)
    fecha_cierre = fields.Datetime(string="Fecha de Cierre", readonly=True)

    estado_actual = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('abierta', 'Abierta'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada')
    ], string="Estado", default='borrador')

    id_departamento = fields.Many2one('hr.department', string="Departamento", ondelete='cascade')
    id_empleado_origen = fields.Many2one('hr.employee', string="Empleado Origen", ondelete='set null')

    comentario_ids = fields.One2many('reto1_incidencias.comentario', 'id_incidencia', string="Comentarios")

    # CORRECCIÓN: Borramos 'id_adjunto' y dejamos solo la lista
    adjunto_ids = fields.One2many('reto1_incidencias.adjunto', 'id_incidencia', string="Archivos Adjuntos")

    @api.onchange('estado_actual')
    def _onchange_estado(self):
        # Ahora detecta ambos estados finales
        if self.estado_actual in ['resuelta', 'cerrada']:
            self.fecha_cierre = fields.Datetime.now()
        else:
            self.fecha_cierre = False