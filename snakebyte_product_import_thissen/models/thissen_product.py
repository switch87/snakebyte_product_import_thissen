from odoo import models, fields, api

class ThissenProduct(models.Model):
    _name = 'thissen.product'
    _description = 'Thissen Product'

    name = fields.Char(string='Name', required=True)
    price = fields.Char(string='Price')
    url = fields.Char(string='URL', required=True, unique=True)
    description = fields.Text(string='Description')
    sku = fields.Char(string='SKU')
    image_url = fields.Char(string='Image URL')
    te_verbeteren_met_ai = fields.Boolean(string='Te Verbeteren met AI', default=True)
    status = fields.Selection([
        ('pending_review', 'Pending Review'),
        ('pending_detail_crawl', 'Pending Detail Crawl'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='pending')
    variants = fields.One2many('thissen.product.variant', 'product_id', string='Variants')

    @api.model
    def detailed_crawl_selected(self):
        for product in self:
            product.status = 'pending_review'  # Hier kun je de crawl-logica integreren
            # Voeg je detailed crawl logic hier toe
            self.env['thissen.crawler'].crawl_detailed_pages(product)  # Roep de crawler aan



class ThissenProductVariant(models.Model):
    _name = 'thissen.product.variant'
    _description = 'Thissen Product Variant'

    product_id = fields.Many2one('thissen.product', string='Product', required=True, ondelete='cascade')
    variant_name = fields.Char(string='Variant Name')
    stock = fields.Char(string='Stock')
