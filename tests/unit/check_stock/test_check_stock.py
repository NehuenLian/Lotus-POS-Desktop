from ...data_access.fake_dao import FakeCheckStockDAO
from unittest.mock import MagicMock, patch

from src.business_logic.check_stock import CheckStock

def test_search_product():

    check_stock_class = CheckStock()
    session_mock = MagicMock()
    with patch("src.business_logic.check_stock.session_scope", session_mock):
        with patch("src.business_logic.check_stock.CheckStockDAO", FakeCheckStockDAO):

            product_id, product_barcode, product_name, available_quantity = check_stock_class.search_product("1234567890123")

    assert product_id == 1
    assert product_barcode == "1234567890123"
    assert product_name == "COCA COLA"
    assert available_quantity == 2