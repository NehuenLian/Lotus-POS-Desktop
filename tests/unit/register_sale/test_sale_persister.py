from datetime import date, time
from decimal import Decimal
from unittest.mock import MagicMock, patch

from src.business_logic.register_sale import (Product, ProductSale,
                                              SaleManagement, SalePersister)

from ...conftest import prepare_for_sale_persister
from ...data_access.fake_dao import FakeRegisterSaleDAO


def test_get_products_dict():

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

    assert len(details_list) == 1
    sale_mgmt.clear_sale_list()


def test_insert_sale():
    """
    sale_id is the id returned after a session.flush()
    """

    # - SalePersister needs an SaleManagement instance on runtime
    sale_mgmt = SaleManagement()
    sale_mgmt.total_quantity = 3.15
    sale_mgmt.amount = 20
    sale_mgmt.amount_excl_vat = 15
    sale_mgmt.amount_only_vat = 18.15
    sale_mgmt.pay_method = "Cash"
    sale_mgmt.sale_date = date.today()
    sale_mgmt.sale_hour = time(14, 30, 0)
    # - SalePersister needs an SaleManagement instance on runtime

    session_mock = MagicMock()
    with patch("src.business_logic.register_sale.session_scope", session_mock):
        with patch("src.business_logic.register_sale.RegisterSaleDAO", FakeRegisterSaleDAO):

            sale_persister = SalePersister(session_mock)

            sale_id = sale_persister.insert_sale(session_mock)

    assert sale_id == 1
    sale_mgmt.clear_sale_list()


def test_insert_sale_details():
    session_mock = MagicMock()
    details_list, sale_persister = prepare_for_sale_persister()

    with patch("src.business_logic.register_sale.session_scope", session_mock):
        with patch("src.business_logic.register_sale.RegisterSaleDAO") as mock_dao_cls:

            mock_dao_instance = mock_dao_cls.return_value
            sale_persister.insert_sale_details(1, details_list, session_mock)

    mock_dao_instance.insert_sale_detail.assert_called()


def test_update_inventory():
    session_mock = MagicMock()
    details_list, sale_persister = prepare_for_sale_persister()

    with patch("src.business_logic.register_sale.session_scope", session_mock):
        with patch("src.business_logic.register_sale.RegisterSaleDAO") as mock_dao_cls:

            mock_dao_instance = mock_dao_cls.return_value
            sale_persister.update_inventory(details_list, session_mock)

    mock_dao_instance.update_stock_table.assert_called()


def test_update_fiscal_status():
    session_mock = MagicMock()
    sale_persister = SalePersister(MagicMock())

    with patch("src.business_logic.register_sale.session_scope", session_mock):
        with patch("src.business_logic.register_sale.RegisterSaleDAO") as mock_dao_cls:

            mock_dao_instance = mock_dao_cls.return_value
            sale_persister.update_fiscal_status(1, False)

    mock_dao_instance.update_sale_fiscal_status.assert_called()
