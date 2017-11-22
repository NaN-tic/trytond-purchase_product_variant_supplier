# This file is part purchase_product_variant_supplier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import product

def register():
    Pool.register(
        product.ProductSupplier,
        product.Product,
        product.ProductPurchaseProductSupplier,
        module='purchase_product_variant_supplier', type_='model')
