from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Encuesta(models.Model):
    _name = 'reto1_incidencias.encuesta'
    _description = 'Encuesta de Satisfacción'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'id_incidencia'

    puntuacion = fields.Selection([
        ('1', '1 - Muy Malo'),
        ('2', '2 - Malo'),
        ('3', '3 - Regular'),
        ('4', '4 - Bueno'),
        ('5', '5 - Excelente')
    ], string='Puntuación', required=True, tracking=True)

    comentario = fields.Text(string='Comentario')

    canal = fields.Selection([
        ('1', 'Web'),
        ('2', 'Email'),
        ('3', 'Teléfono')
    ], string='Canal', required=True)

    fecha_respuesta = fields.Datetime(
        string='Fecha Respuesta',
        default=fields.Datetime.now,
        readonly=True
    )

    id_incidencia = fields.Many2one('reto1_incidencias.incidencia', string='Incidencia', required=True,
                                    ondelete='cascade')
    id_empleado = fields.Many2one('hr.employee', string='Empleado', required=True)


    tag_ids = fields.Many2many(
        'reto1_incidencias.encuesta.etiqueta',
        relation='reto1_encuesta_tags_rel',
        string='Etiquetas',
        help="Clasificación (ej. Urgente, Felicitación)"
    )

    _sql_constraints = [
        ('unique_incidencia', 'unique(id_incidencia)', 'Error: Ya existe una encuesta para esta incidencia')
    ]

    @api.model
    def create(self, vals):
        if vals.get('puntuacion') == '1':
            vals['canal'] = '3'
        return super(Encuesta, self).create(vals)

    resultado_texto = fields.Char(string='Resultado', compute='_compute_resultado', store = True)

    @api.depends('puntuacion')
    def _compute_resultado(self):
        for record in self:
            if record.puntuacion in ['4', '5']:
                record.resultado_texto = 'POSITIVO'
            elif record.puntuacion == '3':
                record.resultado_texto = 'NEUTRAL'
            else:
                record.resultado_texto = 'NEGATIVO'

    @api.constrains('puntuacion', 'comentario')
    def _check_comentario_obligatorio(self):
        for record in self:
            if record.puntuacion in ['1', '2'] and not record.comentario:
                raise ValidationError("El comentario es obligatorio para puntuaciones bajas (1 o 2).")



class EncuestaEtiqueta(models.Model):
    _name = 'reto1_incidencias.encuesta.etiqueta'
    _description = 'Etiqueta de Encuesta'

    name = fields.Char(string='Etiqueta', required=True)
    color = fields.Integer(string='Color')



