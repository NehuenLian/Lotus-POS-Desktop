from decimal import Decimal

import pytest

from src.business_logic.register_sale import Product, ProductSale, SaleManagement, SalePersister
from datetime import date, time


@pytest.fixture(autouse=True)
def clear_instances():

    Product.clear_product_instance_list()
    ProductSale.clear_productsale_instances()

    yield

    Product.clear_product_instance_list()
    ProductSale.clear_productsale_instances()


def prepare_for_sale_persister():
    ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))

    sale_mgmt = SaleManagement()

    sale_mgmt.total_quantity = 3.15
    sale_mgmt.amount = 20
    sale_mgmt.amount_excl_vat = 15
    sale_mgmt.amount_only_vat = 18.15
    sale_mgmt.pay_method = "Cash"
    sale_mgmt.sale_date = date.today()
    sale_mgmt.sale_hour = time(14, 30, 0)

    sale_persister = SalePersister(sale_mgmt)
    details_list = sale_persister.get_products_dict()

    sale_mgmt.clear_sale_list()

    return details_list, sale_persister
