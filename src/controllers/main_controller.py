import os

from PySide6.QtWidgets import QApplication

from src.business_logic.check_stock import CheckStock
from src.business_logic.manage_prices import PriceManagement
from src.business_logic.register_sale import SaleManagement
from src.controllers.check_stock import StockManagementController
from src.controllers.manage_prices import PricesManagementController
from src.controllers.register_sale import SalesManagementController
from src.controllers.settings import SettingsController
from src.data_access.connection import DataBaseConnection
from src.utils.logger import console_logger, controller_logger
from src.views.check_stock import CheckStockViewManager
from src.views.main_views import GeneralViewsManager
from src.views.manage_prices import PriceViewManager
from src.views.register_sale import SalesViewManager
from src.views.settings import SettingsViewManager


class MainController:
    def __init__(self, db_url: str):
        # Business controllers
        self.stock_manager = CheckStock()
        self.prices_manager = PriceManagement()
        self.sales_manager = SaleManagement()

        # Domain controllers
        self.stock_controller = StockManagementController(self.stock_manager)
        self.price_controller = PricesManagementController(self.prices_manager)
        self.sales_controller = SalesManagementController(self.sales_manager)
        self.settings_controller = SettingsController()

        # Domain views
        self.check_stock_view = CheckStockViewManager(self.stock_controller)
        self.price_view = PriceViewManager(self.price_controller)
        self.sales_view = SalesViewManager(self.sales_controller)
        self.settings_view = SettingsViewManager(self.settings_controller)

        # Initialize all views in general views
        self.ui = GeneralViewsManager(
            self,
            self.check_stock_view,
            self.price_view,
            self.sales_view,
            self.settings_view
        )

        self.stock_controller.view = self.check_stock_view
        self.price_controller.view = self.price_view
        self.sales_controller.view = self.sales_view
        self.settings_controller.view = self.settings_view

        self._connect_db(db_url)

    def _connect_db(self, db_url: str) -> None:
        try:
            connection = DataBaseConnection(db_url)
            connection.connect()

        except Exception as e:
            controller_logger.warning("No URL provided; connection failed, but the app was initialized anyway.")
        
    def quit_app(self) -> None:
        QApplication.quit()

