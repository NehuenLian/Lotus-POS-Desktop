from unittest.mock import patch

from sqlalchemy import select

from src.business_logic.manage_prices import PriceManagement
from src.controllers.manage_prices import PricesManagementController
from src.data_access.database_tables import Stock

from ..conftest import get_memory_session, mock_session_scope
from ..views.fake_views import FakePriceViewManager


def test_manage_prices_success(insert_data_in_memory_db):

    BARCODE = "7790895000997"

    fake_view = FakePriceViewManager()
    manage_prices_business = PriceManagement()
    
    prices_mgmt = PricesManagementController(manage_prices_business)
    prices_mgmt.view = fake_view

    with patch("src.business_logic.manage_prices.session_scope", mock_session_scope):
        prices_mgmt.get_product(BARCODE)
        prices_mgmt.update_price(1, 4000.00)

    # verify price has changed:
    session = get_memory_session()
    product = session.execute(select(Stock).filter_by(db_barcode=BARCODE)).scalar_one()
    assert product.db_final_price_to_consumer == 4000.00


def test_manage_prices_product_not_found():
    fake_view = FakePriceViewManager()
    manage_prices_business = PriceManagement()
    
    prices_mgmt = PricesManagementController(manage_prices_business)
    prices_mgmt.view = fake_view

    with patch("src.business_logic.manage_prices.session_scope", mock_session_scope):
        prices_mgmt.get_product("1111111111")

    assert fake_view.notifications_list[0] == "Producto no encontrado."

def test_manage_prices_invalid_price():
    fake_view = FakePriceViewManager()
    manage_prices_business = PriceManagement()
    
    prices_mgmt = PricesManagementController(manage_prices_business)
    prices_mgmt.view = fake_view

    with patch("src.business_logic.manage_prices.session_scope", mock_session_scope):
        prices_mgmt.get_product("7790895000997")
        prices_mgmt.update_price(1, -1)

    assert fake_view.notifications_list[0] == "El nuevo precio no puede ser negativo o menor a $1."
