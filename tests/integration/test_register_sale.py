from unittest.mock import patch

from src.business_logic.register_sale import SaleManagement
from src.controllers.register_sale import SalesManagementController

from ..conftest import mock_session_scope
from ..views.fake_views import FakeSalesViewManager

def thread_mock(facturation_handler):
    return facturation_handler()

def test_register_sale_success(insert_data_in_memory_db):
    fake_view = FakeSalesViewManager()
    sales_management_business = SaleManagement()

    register_sale_mgmt = SalesManagementController(sales_management_business)
    register_sale_mgmt.view = fake_view

    with patch("src.business_logic.register_sale.session_scope", mock_session_scope):

        register_sale_mgmt.get_product("7790895000997") # product id 1
        register_sale_mgmt.get_product("7790895000997") # product id 1
        register_sale_mgmt.get_product("7798339251141") # product id 2
        register_sale_mgmt.get_product("7790490998309") # product id 3
        register_sale_mgmt.remove_product(2) # remove product with id 2

        register_sale_mgmt.select_pay_method("Cash")

        with patch("src.controllers.register_sale.use_other_thread", thread_mock):
            register_sale_mgmt.complete_sale()