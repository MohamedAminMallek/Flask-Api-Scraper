from my_flask_api.views.abstract_views import PublicAbstractView
from webargs.flaskparser import use_kwargs
from marshmallow import Schema
from webargs import fields
from my_flask_api.scraper.amazon import scrape_product
PRODUCTS = []


class ScraperSchema(Schema):
    class Meta:
        strict = True

    product_name = fields.Str(required=True, location="view_args")

class ProductScraperView(PublicAbstractView):

    @use_kwargs(ScraperSchema)
    def post(self, product_name):
        product = scrape_product(product_name)
        if product:
            PRODUCTS.append(product)
        return product    
    

class ProductsView(PublicAbstractView):
    def get(self):
        return PRODUCTS
    