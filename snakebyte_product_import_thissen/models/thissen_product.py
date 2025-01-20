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
    tmpl_id = fields.Many2one('product.template', 'Product template', required=False, default=False)
    tmpl_attribute_line_ids = fields.One2many('product.template.attribute.line', related="tmpl_id.attribute_line_ids", readonly=False)

    def _link_to_product_template(self):
        """Link Thissen Product to a product.template based on SKU."""
        if not self.sku:
            return

        product_supplierinfo = self.env['product.supplierinfo'].sudo().search([
            ('product_code', '=', self.sku[0:4])
        ], limit=1)
        if product_supplierinfo:
            self.tmpl_id = product_supplierinfo.product_tmpl_id


    @api.model
    def detailed_crawl_selected(self):
        for product in self:
            product.status = 'pending_review'  # Hier kun je de crawl-logica integreren
            # Voeg je detailed crawl logic hier toe
            self.env['thissen.crawler'].crawl_detailed_pages_for_product(product)  # Roep de crawler aan



class ThissenProductVariant(models.Model):
    _name = 'thissen.product.variant'
    _description = 'Thissen Product Variant'

    product_id = fields.Many2one('thissen.product', string='Product', required=True, ondelete='cascade')
    variant_name = fields.Char(string='Variant Name')
    stock = fields.Char(string='Stock')
