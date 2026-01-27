from odoo import models, fields, api


class Estadisticas(models.Model):
    _name = 'reto1_incidencias.estadisticas'
    _description = 'Estadísticas de Incidencias'
    _rec_name = 'fecha'

    id_estadistica = fields.Integer(string='Id de estadística', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today, required=True)
    id_departamento = fields.Many2one('hr.department', string='Departamento')

    total_incidencias = fields.Integer(string='Total de Incidencias', compute='calculo_estadisticas', store=True)
    incidencias_finalizadas = fields.Integer(string='Incidencias Finalizadas', compute='calculo_estadisticas',
                                             store=True)
    tiempo_promedio_resolucion = fields.Float(string='Tiempo Promedio de Resolución (días)',
                                              compute='calculo_estadisticas', store=True)
    porcentaje_resueltas = fields.Float(string='Porcentaje Resueltas (%)', compute='calculo_estadisticas', store=True)

    @api.depends('fecha', 'id_departamento')
    def calculo_estadisticas(self):
        # CORRECCIÓN: El nombre del modelo debe ser singular, tal como se definió en incidencia.py
        Incidencia = self.env['reto1_incidencias.incidencia']

        for record in self:
            domain = []

            if record.id_departamento:
                domain.append(('id_departamento', '=', record.id_departamento.id))

            if record.fecha:
                domain.append(('fecha_creacion', '<=', record.fecha))

            total = Incidencia.search_count(domain)

            # Buscamos incidencias resueltas que tengan fecha de cierre establecida
            finalizadas = Incidencia.search(
                domain + [
                    ('estado_actual', 'in', ['resuelta', 'cerrada']),  # Aceptamos ambos
                    ('fecha_cierre', '!=', False)
                ]
            )

            record.total_incidencias = total
            record.incidencias_finalizadas = len(finalizadas)

            tiempos = []
            for inc in finalizadas:
                # Odoo devuelve objetos datetime, operamos directamente
                if inc.fecha_creacion and inc.fecha_cierre:
                    diferencia = inc.fecha_cierre - inc.fecha_creacion
                    dias = diferencia.total_seconds() / 86400
                    if dias > 0:
                        tiempos.append(dias)

            record.tiempo_promedio_resolucion = (sum(tiempos) / len(tiempos)) if tiempos else 0.0

            record.porcentaje_resueltas = (
                (record.incidencias_finalizadas / total) * 100
                if total else 0.0
            )