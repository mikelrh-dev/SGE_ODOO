from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Adjunto(models.Model):
    _name = 'reto1_incidencias.adjunto'
    _description = 'Adjunto'
    _rec_name = 'nombre_archivo'

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

    id_incidencia = fields.Many2one(
        'reto1_incidencias.incidencia',
        string='Incidencia',
        ondelete='cascade'
    )

    @api.constrains('nombre_archivo')
    def _check_extension_archivo(self):
        for record in self:
            if record.nombre_archivo and '.' not in record.nombre_archivo:
                raise ValidationError("El nombre del archivo debe incluir una extensión (ej: documento.pdf).")

    @api.model
    def create(self, vals):
        # Ejemplo: Si el usuario sube un archivo con espacios, los cambiamos por guiones bajos
        if vals.get('nombre_archivo'):
            vals['nombre_archivo'] = vals['nombre_archivo'].replace(' ', '_')
        return super(Adjunto, self).create(vals)

    def write(self, vals):
        # Lógica al EDITAR (modificar)
        if vals.get('nombre_archivo'):
            vals['nombre_archivo'] = vals['nombre_archivo'].replace(' ', '_')
        return super(Adjunto, self).write(vals)

    def unlink(self):
        # Restricción de seguridad: No borrar adjuntos de incidencias cerradas
        for record in self:
            if record.id_incidencia and record.id_incidencia.estado_actual == 'cerrada':
                raise ValidationError("No puedes borrar adjuntos de una incidencia cerrada.")
        return super(Adjunto, self).unlink()