from decimal import Decimal
from unittest.mock import MagicMock, patch

from src.business_logic.register_sale import (Product, ProductSale,
                                              SaleManagement)

from ...data_access.fake_dao import FakeRegisterSaleDAO


def test_sale_management_get_full_product():

    session_mock = MagicMock()
    with patch("src.business_logic.register_sale.session_scope", session_mock):
        with patch("src.business_logic.register_sale.RegisterSaleDAO", FakeRegisterSaleDAO):

            sale_operation = SaleManagement()
            product = sale_operation.get_full_product("1234567890123")
            assert product.product_id == 1


def test_cancel_product():

    product = Product(1, 
                "1234567890123", 
                "COCA COLA", 
                50, 
                Decimal("15.00"),
                Decimal("18.15"), 
                Decimal("20.00")
            )

    sale_operation = SaleManagement()
    sale_operation.cancel_product(1)
    assert len(product.product_instance_list) == 0


def test_set_pay_method():

    sale_operation = SaleManagement()
    sale_operation.set_pay_method("Cash")

    assert sale_operation.pay_method == "Cash"


def test_build_product_sale():

    product = Product(
                1, 
                "1234567890123", 
                "COCA COLA", 
                50, 
                Decimal("15.00"),
                Decimal("18.15"), 
                Decimal("20.00")
            )
    sale_operation = SaleManagement()
    sale_operation.build_product_sale()

    assert sale_operation.sale_list[0].productsale_instances[0].subquantity == 1
    assert sale_operation.sale_list[0].productsale_instances[0].subtotal == Decimal("20.00")
    assert sale_operation.sale_list[0].productsale_instances[0].subtotal_excl_vat == Decimal("15.00")
    assert sale_operation.sale_list[0].productsale_instances[0].subtotal_incl_vat == Decimal("18.15")


def test_compute_total_quantity():

    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))

    sale_operation = SaleManagement()
    sale_operation.compute_total_quantity()
    assert sale_operation.total_quantity == 1


def test_compute_total_amount():

    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))

    sale_operation = SaleManagement()
    sale_operation.compute_total_amount()
    assert sale_operation.amount == Decimal("20.00")


def test_compute_total_amount_excl_vat():
    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))

    sale_operation = SaleManagement()
    sale_operation.compute_total_amount_excl_vat()

    assert sale_operation.amount_excl_vat == Decimal("15.00")


def test_compute_total_iva():
    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))

    sale_operation = SaleManagement()
    total_iva = sale_operation.compute_total_iva()

    assert total_iva == Decimal("3.15")


def test_remove_duplicates():
    product = Product(
            product_id=1,
            barcode="1234567890123",
            product_name="COCA COLA",
            available_quantity=50,
            price_excl_vat=Decimal("15.00"),
            price_incl_vat=Decimal("18.15"),
            customer_price=Decimal("20.00")
        )
    for i in range(2):
        product_sale = ProductSale(product)

    sale_operation = SaleManagement()
    sale_operation.remove_duplicates()

    assert len(sale_operation.sale_list) == 1