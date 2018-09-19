# This file is part of the purchase_product_variant_supplier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['ProductSupplier', 'Product', 'ProductPurchaseProductSupplier']


class ProductSupplier(metaclass=PoolMeta):
    __name__ = 'purchase.product_supplier'
    variant_suppliers = fields.Many2Many('product.product-purchase.product_supplier',
        'supplier', 'product', 'Variant Supplier',
        domain=[('template', '=', Eval('product'))],
        depends=['product'])


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'
    purchasable_variant = fields.Function(fields.Boolean('Purchasable Variant'),
        'on_change_with_purchasable_variant', searcher='search_purchasable_variant')
    variant_suppliers = fields.Many2Many('product.product-purchase.product_supplier',
        'product', 'supplier', 'Variant Supplier',
        domain=[('product', '=', Eval('template'))],
        states={
            'invisible': (~Eval('purchasable_variant', False) |
                ~Eval('context', {}).get('company'))
            },
        depends=['template', 'purchasable_variant'])
    # ovewrite product_suppliers field defined at product template
    # because get_purchase_price calculate from product_suppliers field
    product_suppliers = fields.Function(fields.One2Many('purchase.product_supplier',
        'product', 'Suppliers', states={
            'invisible': (~Eval('purchasable_variant', False) |
                ~Eval('context', {}).get('company'))
            },
        depends=['purchasable_variant']), 'get_product_suppliers')

    @fields.depends('template')
    def on_change_with_purchasable_variant(self, name=None):
        if self.template:
            return self.template.purchasable

    @classmethod
    def search_purchasable_variant(cls, name, clause):
        return [
            ('template.purchasable',) + tuple(clause[1:]),
            ]

    def get_product_suppliers(self, name):
        if self.variant_suppliers:
            return [x.id for x in self.variant_suppliers]
        return [x.id for x in self.template.product_suppliers]


class ProductPurchaseProductSupplier(ModelSQL):
    'Product - Purchase Product Supplier'
    __name__ = 'product.product-purchase.product_supplier'
    _table = 'product_purchase_supplier_rel'
    product = fields.Many2One('product.product', 'Product', ondelete='CASCADE',
            required=True, select=True)
    supplier = fields.Many2One('purchase.product_supplier', 'Supplier',
        ondelete='CASCADE', required=True, select=True)
