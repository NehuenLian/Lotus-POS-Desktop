from typing import Optional


class FakeCheckStockViewManager():
    def __init__(self):
        self.notifications_list = []

    def display_product(self, 
                        product_id: int, 
                        product_barcode: Optional[str], 
                        product_name: str, 
                        available_quantity: Optional[int]
                    ) -> None:
        pass

    def show_notification_from_controller(self, message: str) -> None:
        self.notifications_list.append(message)


class FakePriceViewManager():
    def __init__(self):
        self.notifications_list = []

    def display_product(self, 
                        product_id: int, 
                        product_barcode: Optional[str], 
                        product_name: str, 
                        product_price: Optional[int]
                    ) -> None:
        pass

    def show_notification_from_controller(self, message: str) -> None:
        self.notifications_list.append(message)


class FakeSalesViewManager():
    def __init__(self):
        self.notifications_list = []

    def create_view_product(self, product):
        pass

    def show_notification_from_controller(self, message: str) -> None:
        self.notifications_list.append(message)