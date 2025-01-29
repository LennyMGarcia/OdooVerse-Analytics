# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Custom',
    'version' : '0.1',
    'sequence': 185,
    'category': 'Human Resources/Custom',
    'module_type': 'official',
    'summary': 'Custom API for querying sales orders',
    'depends': [
        'base',
	'sale',  
    ],
    'installable': True,
    'application': True,  
    'license': 'LGPL-3',
}