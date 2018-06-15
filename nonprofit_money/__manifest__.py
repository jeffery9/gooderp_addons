# -*- coding: utf-8 -*-
{
    'name': "GOODERP 非营利组织模块",
    'author': "",
    'website': "http://www.osbzr.com",
    'category': 'gooderp',
    'summary': 'GoodERP非营利组织解决方案包',
    "description":
    '''
                            该模块实现了非营利组织的功能。
    ''',
    'version': '11.11',
    'depends': ['web_error_dialog','keep_good','auto_exchange','tree_zero_display_blank','money','core'],
    'data': [
        'views/inout_activities_view.xml',
        'views/nonprofit_money_order_view.xml',
        'security/groups_ccb.xml',
        'data/inout_activities_template.xml',
        'data/inout_export_template_data.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'application': True,
}

