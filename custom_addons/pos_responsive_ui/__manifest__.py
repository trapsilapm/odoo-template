# -*- coding: utf-8 -*-
{
    'name': 'POS Responsive UI & Large Product View',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Adaptive and responsive product grid sizing for multi-device Odoo 17 POS',
    'author': 'Antigravity AI',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_responsive_ui/static/src/css/pos_responsive.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
