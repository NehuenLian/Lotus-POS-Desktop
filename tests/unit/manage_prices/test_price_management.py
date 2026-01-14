from ...data_access.fake_dao import FakeManagePricesDAO
from unittest.mock import MagicMock, patch

from src.business_logic.manage_prices import PriceManagement
from src.exceptions import InvalidPriceError
import pytest

def test_search_product():

    price_management_class = PriceManagement()
    session_mock = MagicMock()
    with patch("src.business_logic.manage_prices.session_scope", session_mock):
        with patch("src.business_logic.manage_prices.ManagePricesDAO", FakeManagePricesDAO):

            id, barcode, product_name, price = price_management_class.search_product("1234567890123")

    assert id == 1
    assert barcode == "1234567890123"
    assert product_name == "COCA COLA"
    assert price == 20


def test_update_prices():

    price_management_class = PriceManagement()
    session_mock = MagicMock()
    with patch("src.business_logic.manage_prices.session_scope", session_mock):
        with patch("src.business_logic.manage_prices.ManagePricesDAO") as mock_class:
            mock_class_instance = mock_class.return_value

            price_management_class.update_prices(1, 15.00)
            
    mock_class_instance.update_price_in_db.assert_called()


def test_update_prices_error():

    price_management_class = PriceManagement()
    session_mock = MagicMock()
    with patch("src.business_logic.manage_prices.session_scope", session_mock):
        with patch("src.business_logic.manage_prices.ManagePricesDAO") as mock_class:
            mock_class_instance = mock_class.return_value

            with pytest.raises(InvalidPriceError):
                price_management_class.update_prices(1, -1)

    mock_class_instance.update_price_in_db.assert_not_called()


def test_is_price_valid_true():
    price_management_class = PriceManagement()
    is_valid = price_management_class._is_price_valid(15.00)

    assert is_valid == True


def test_is_price_valid_false():
    price_management_class = PriceManagement()
    is_valid = price_management_class._is_price_valid(-1)

    assert is_valid == False