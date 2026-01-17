from unittest.mock import patch

from src.business_logic.check_stock import CheckStock
from src.controllers.check_stock import StockManagementController

from ..conftest import mock_session_scope
from ..views.fake_views import FakeCheckStockViewManager


def test_check_stock_success(insert_data_in_memory_db):
    fake_view = FakeCheckStockViewManager()
    check_stock_business = CheckStock()

    stock_mgmt = StockManagementController(check_stock_business)
    stock_mgmt.view = fake_view

    with patch("src.business_logic.check_stock.session_scope", mock_session_scope):
        stock_mgmt.get_product("7790895000997")


def test_check_stock_product_not_found(insert_data_in_memory_db):
    fake_view = FakeCheckStockViewManager()
    check_stock_business = CheckStock()

    stock_mgmt = StockManagementController(check_stock_business)
    stock_mgmt.view = fake_view

    with patch("src.business_logic.check_stock.session_scope", mock_session_scope):
        stock_mgmt.get_product("1111111111")

    assert fake_view.notifications_list[0] == "Producto no encontrado."