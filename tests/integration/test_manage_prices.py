from unittest.mock import patch

from src.business_logic.manage_prices import PriceManagement
from src.controllers.manage_prices import PricesManagementController

from ..conftest import mock_session_scope
from ..views.fake_views import FakePriceViewManager


def test_manage_prices_success(insert_data_in_memory_db):
    fake_view = FakePriceViewManager()
    manage_prices_business = PriceManagement()
    
    prices_mgmt = PricesManagementController(manage_prices_business)
    prices_mgmt.view = fake_view

    with patch("src.business_logic.manage_prices.session_scope", mock_session_scope):
        prices_mgmt.get_product("7790895000997")
        prices_mgmt.update_price(1, 4000.00)

def test_manage_prices_product_not_found():
    fake_view = FakePriceViewManager()
    manage_prices_business = PriceManagement()
    
    prices_mgmt = PricesManagementController(manage_prices_business)
    prices_mgmt.view = fake_view

    with patch("src.business_logic.manage_prices.session_scope", mock_session_scope):
        prices_mgmt.get_product("unknown barcode")

def test_manage_prices_invalid_price():
    fake_view = FakePriceViewManager()
    manage_prices_business = PriceManagement()
    
    prices_mgmt = PricesManagementController(manage_prices_business)
    prices_mgmt.view = fake_view

    with patch("src.business_logic.manage_prices.session_scope", mock_session_scope):
        prices_mgmt.get_product("7790895000997")
        prices_mgmt.update_price(1, -1)
