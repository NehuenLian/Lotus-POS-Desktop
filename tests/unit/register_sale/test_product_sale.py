from decimal import Decimal

from src.business_logic.register_sale import Product, ProductSale


def test_product_sale():

    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))
    product_count = product_sale.count_products_in_cart()
    assert product_count == {1: 1}


def test_product_sale_subquantity():

    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))
    product_sale.count_and_assign_quantity_by_product({1: 1})
    assert product_sale.subquantity == 1


def test_product_sale_subtotal_excl_vat():

    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))
    product_sale.calculate_and_assign_subtotal_excl_vat_to_each_product({1: 1})
    assert product_sale.subtotal_excl_vat == Decimal("15.00")


def test_product_sale_subtotal_incl_vat():

    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))
    product_sale.calculate_and_assign_subtotal_incl_vat_to_each_product({1: 1})
    assert product_sale.subtotal_incl_vat == Decimal("18.15")


def test_product_sale_assign_subtotal():

    product_sale = ProductSale(Product(
        product_id=1,
        barcode="1234567890123",
        product_name="COCA COLA",
        available_quantity=50,
        price_excl_vat=Decimal("15.00"),
        price_incl_vat=Decimal("18.15"),
        customer_price=Decimal("20.00")
    ))
    product_sale.calculate_and_assign_subtotal_to_each_product({1: 1})
    assert product_sale.subtotal == Decimal("20.00")
