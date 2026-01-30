# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Estadisticas(models.Model):
    _name = 'reto1_incidencias.estadisticas'
    _description = 'Estadísticas de Incidencias'
    _rec_name = 'fecha'

    # ------
    # CAMPOS
    # ------
    id_estadistica = fields.Integer(string='ID Estadística', required=True)

    fecha = fields.Date(
        string='Fecha de Análisis',
        default=fields.Date.context_today,
        required=True
    )

    id_departamento = fields.Many2one(
        'hr.department',
        string='Departamento'
    )

    # -----------------
    # CAMPOS CALCULADOS 
    # -----------------
    total_incidencias = fields.Integer(
        string='Total Incidencias',
        compute='_calculo_estadisticas',
        store=True
    )

    incidencias_finalizadas = fields.Integer(
        string='Resueltas',
        compute='_calculo_estadisticas',
        store=True
    )

    tiempo_promedio_resolucion = fields.Float(
        string='Tiempo Medio Resolución (días)',
        compute='_calculo_estadisticas',
        store=True,
        group_operator="avg" 
    )

    porcentaje_resueltas = fields.Float(
        string='% Éxito',
        compute='_calculo_estadisticas',
        store=True,
        group_operator="avg"
    )

    _sql_constraints = [
        ('unique_fecha_dept', 'unique(fecha, id_departamento)',
         '¡Error! Ya existen estadísticas para este departamento en esta fecha.')
    ]

    # ------------
    # VALIDACIONES 
    # ------------
    @api.constrains('id_estadistica')
    def _check_id_positivo(self):
        """Valida que el ID sea lógico, evitando inconsistencias"""
        for record in self:
            if record.id_estadistica < 0:
                raise ValidationError("El ID de estadística no puede ser negativo.")

    @api.depends('fecha', 'id_departamento')
    def _calculo_estadisticas(self):
        # Instanciamos el modelo de incidencias para hacer búsquedas
        Incidencia = self.env['reto1_incidencias.incidencia']

        for record in self:
            domain = []
            if record.id_departamento:
                domain.append(('id_departamento', '=', record.id_departamento.id))
            if record.fecha:
                domain.append(('fecha_creacion', '<=', record.fecha))

            total = Incidencia.search_count(domain)
            finalizadas_recs = Incidencia.search(
                domain + [('estado_actual', '=', 'resuelta')]
            )

            # Asignación de valores
            record.total_incidencias = total
            record.incidencias_finalizadas = len(finalizadas_recs)

            # Cálculos
            tiempos = []
            for inc in finalizadas_recs:
                if inc.fecha_creacion and inc.fecha_cierre:
                    delta = inc.fecha_cierre - inc.fecha_creacion
                    tiempos.append(delta.days)  # Usamos días completos

            if tiempos:
                record.tiempo_promedio_resolucion = sum(tiempos) / len(tiempos)
            else:
                record.tiempo_promedio_resolucion = 0.0

            if total > 0:
                record.porcentaje_resueltas = (len(finalizadas_recs) / total) * 100
            else:
                record.porcentaje_resueltas = 0.0

    # ----------
    # SOBRECARGA
    # ----------
    @api.model
    def create(self, vals):
        """
        Sobrescribimos create para inyectar lógica antes de guardar.
        Ejemplo: Asegurar que si no viene fecha, se asigne hoy explícitamente.
        """
        if 'fecha' not in vals:
            vals['fecha'] = fields.Date.context_today(self)

        return super(Estadisticas, self).create(vals)
