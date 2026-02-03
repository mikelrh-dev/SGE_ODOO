{
    'name': 'Reto1_Incidencias',
    'description': "Gestión de Incidencias ",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/account_security.xml',
        'security/encuesta_security.xml',
        'security/ir.model.access.csv',

        'views/vistaIncidencia.xml',
        'views/vistaEstadisticas.xml',
        'views/encuestaview.xml',
        'views/vistaDepartamento.xml',
        'views/vistaEmpleado.xml',
        'views/vistaAdjunto.xml',
        'views/vistaComentario.xml',

        'views/menu.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}