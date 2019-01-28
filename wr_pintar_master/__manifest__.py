# -*- coding: utf-8 -*-
{
    'name': 'Warung Pintar Recruitment',
    'version': '11.0.1.0.0',
    'author': 'Syarifudin Akbar',
    'website': 'https://github.com/sharibar/wr_pintar_recruitment',
    'summary': "Custom Module Recruitment Warung Pintar",
    'contributors': [
        'Syarifudin Akbar',
    ],
    'description': """
        Module Recruitment Warung Pintar
    """,
    'category': 'Recruitment',
    'sequence': 1,
    'qweb': ['static/src/xml/master_template.xml'],
    'depends': ['base_import'],
    'data': [
        'security/ir.model.access.csv',
        'views/master_komponen_view.xml',
        'views/master_item_view.xml',
        'views/master_menu.xml',
        'wizard/master_custom_import.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
