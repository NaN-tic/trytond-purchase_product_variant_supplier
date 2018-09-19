==========================================
Purchase Product Variant Supplier Scenario
==========================================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import Model, Wizard, Report
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Install purchase::

    >>> config = activate_modules('purchase_product_variant_supplier')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> cash = accounts['cash']

    >>> Journal = Model.get('account.journal')
    >>> cash_journal, = Journal.find([('type', '=', 'cash')])
    >>> cash_journal.credit_account = cash
    >>> cash_journal.debit_account = cash
    >>> cash_journal.save()

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create parties::

    >>> Party = Model.get('party.party')
    >>> supplier = Party(name='Supplier')
    >>> supplier.save()
    >>> supplier2 = Party(name='Supplier2')
    >>> supplier2.save()
    >>> customer = Party(name='Customer')
    >>> customer.save()

Create account categories::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name="Account Category")
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.save()

    >>> account_category_tax, = account_category.duplicate()
    >>> account_category_tax.supplier_taxes.append(tax)
    >>> account_category_tax.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.purchasable = True
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.cost_price = Decimal('5')
    >>> template.cost_price_method = 'fixed'
    >>> template.account_category = account_category_tax
    >>> template.save()
    >>> product, = template.products
    >>> product.code = 'P01'
    >>> product.save()
    >>> product2 = Product()
    >>> product2.template = template
    >>> product2.code = 'P02'
    >>> product2.save()

Add supplier in variants::

    >>> ProductSupplier = Model.get('purchase.product_supplier')
    >>> ProductSupplierPrice = Model.get('purchase.product_supplier.price')
    >>> ps = ProductSupplier()
    >>> ps.product = template
    >>> ps.party = supplier
    >>> ps.name = 'Supplier P01'
    >>> ps.code = 'SO1'
    >>> ps_price = ProductSupplierPrice()
    >>> ps.prices.append(ps_price)
    >>> ps_price.quantity = 5
    >>> ps_price.unit_price = Decimal(10)
    >>> ps_price.sequence = 2
    >>> ps_price = ProductSupplierPrice()
    >>> ps.prices.append(ps_price)
    >>> ps_price.quantity = 1
    >>> ps_price.unit_price = Decimal(15)
    >>> ps_price.sequence = 1
    >>> ps.save()

    >>> ps2 = ProductSupplier()
    >>> ps2.product = template
    >>> ps2.party = supplier2
    >>> ps2.name = 'Supplier P02'
    >>> ps2.code = 'SO2'
    >>> ps_price = ProductSupplierPrice()
    >>> ps2.prices.append(ps_price)
    >>> ps_price.quantity = 10
    >>> ps_price.unit_price = Decimal(18)
    >>> ps_price.sequence = 2
    >>> ps_price = ProductSupplierPrice()
    >>> ps2.prices.append(ps_price)
    >>> ps_price.quantity = 1
    >>> ps_price.unit_price = Decimal(20)
    >>> ps_price.sequence = 1
    >>> ps2.save()

    >>> product.variant_suppliers.append(ps)
    >>> product.save()
    >>> product2.variant_suppliers.append(ps2)
    >>> product2.save()

Purchase 5 products::

    >>> Purchase = Model.get('purchase.purchase')
    >>> PurchaseLine = Model.get('purchase.line')
    >>> purchase = Purchase()
    >>> purchase.party = supplier
    >>> purchase.payment_term = payment_term
    >>> purchase.invoice_method = 'order'
    >>> purchase_line = PurchaseLine()
    >>> purchase.lines.append(purchase_line)
    >>> purchase_line.product = product
    >>> purchase_line.quantity = 6.0
    >>> purchase_line.unit_price == Decimal('10.00')
    True
    >>> purchase_line = PurchaseLine()
    >>> purchase.lines.append(purchase_line)
    >>> purchase_line.product = product2
    >>> purchase_line.quantity = 20.0
    >>> purchase_line.unit_price == Decimal('10.00')
    True
    >>> purchase.save()
