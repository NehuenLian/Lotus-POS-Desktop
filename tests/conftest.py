import csv
from contextlib import contextmanager
from datetime import date, time
from decimal import Decimal

import pytest

from src.business_logic.register_sale import (Product, ProductSale,
                                              SaleManagement, SalePersister)
from src.data_access.connection import DataBaseConnection
from src.data_access.database_tables import Stock


# Integration tests settings
def get_memory_session():
    DB_URL = "sqlite:///:memory:"
    connection = DataBaseConnection(DB_URL)
    session = connection.get_session()

    return session

@pytest.fixture
def insert_data_in_memory_db():
    DataBaseConnection.reset_singleton()
    session = get_memory_session()

    filas = [
        Stock(
            db_barcode="7790895000997",
            db_product_name="COCA COLA SABOR ORIGINAL 2.25L",
            db_available_quantity=100,
            db_final_price_to_consumer=3852.81,
            db_price_excl_vat=2892.56,
            db_price_incl_vat=3500.00
        ),
        Stock(
            db_barcode="7798339251141",
            db_product_name="CERVEZA ARTESANAL PAMPA",
            db_available_quantity=100,
            db_final_price_to_consumer=2200.00,
            db_price_excl_vat=1652.89,
            db_price_incl_vat=2000.00
        ),
        Stock(
            db_barcode="7790490998309",
            db_product_name="EDULCORANTE HILERET CLASICO",
            db_available_quantity=100,
            db_final_price_to_consumer=1320.00,
            db_price_excl_vat=991.74,
            db_price_incl_vat=1200.00
        )
    ]

    session.add_all(filas)
    session.commit()

@contextmanager
def mock_session_scope():

    session = get_memory_session()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# Unit tests settings
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
