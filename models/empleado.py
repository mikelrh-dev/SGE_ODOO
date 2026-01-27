from odoo import models, fields


class Empleado(models.Model):
    _inherit = 'hr.employee'

    # Creamos la relación inversa: Un empleado -> Muchas encuestas
    encuesta_ids = fields.One2many(
        'reto1_incidencias.encuesta',
        'id_empleado',
        string='Encuestas Asignadas'
    )
    _description = 'Empleado -  reto1_incidencias'

    personal_email = fields.Char('Email Personal')
    rol = fields.Selection([
        ('usuario', 'Usuario'),
        ('administrador', 'Administrador'),
        ('tecnico', 'Tecnico')
    ], string='Rol en Incidencias', default='usuario')

    incidencias_creadas_ids = fields.One2many('reto1_incidencias.incidencia','id_empleado_origen',string='Incidencias Creadas')
    comentarios_ids = fields.One2many('reto1_incidencias.comentario','id_empleado',string='Comentarios')

    departamento_ids = fields.Many2many('hr.department', string='Departamentos')
