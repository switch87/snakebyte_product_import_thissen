# -*- coding: utf-8 -*-

import re

from odoo import fields, models, api
from odoo.tools.translate import html_translate


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _out_of_stock_message = fields.Html(string="Out-of-Stock Message", default="", translate=html_translate)

    @api.depends('website_id')
    def get_out_of_stock_message(self):
        self.out_of_stock_message = self._out_of_stock_message if re.sub(re.compile('<.*?>'), '', self._out_of_stock_message).strip() else self.website_id.out_of_stock_msg

    out_of_stock_message = fields.Html("Out-of-stock Message", compute=get_out_of_stock_message, store=False)

    def _default_website_meta(self):
        res = super(ProductTemplate, self)._default_website_meta()
        res['default_opengraph']['g:title'] = self.name
        res['default_opengraph']['g:id'] = self.id
        res['default_opengraph']['g:description'] = self.description_sale
        res['default_opengraph']['g:image'] = self.env['website'].image_url(self, 'image_1024')
        res['default_opengraph']['g:price'] = self.list_price
        res['default_opengraph']['g:availability'] = 'in_stock'
        res['default_opengraph']['g:condition'] = 'new'
        return res
