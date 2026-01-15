import datetime
from decimal import Decimal
from typing import Tuple


class FakeRegisterSaleDAO:
    def __init__(self, session):
        pass

    def get_product(self, barcode: str) -> Tuple[int, str, str, int, Decimal, Decimal, Decimal]:
        return (
                1, 
                "1234567890123", 
                "COCA COLA", 
                50, 
                Decimal("15.00"),
                Decimal("18.15"), 
                Decimal("20.00")
            )
    
    def update_stock_table(self, product_id: int, quantity_purchased: int) -> None:
        pass

    def insert_sale_record(self, 
                           total_quantity: int, 
                           amount: Decimal, 
                           amount_excl_vat: Decimal, 
                           amount_only_vat: Decimal, 
                           pay_method: str, 
                           sale_date: datetime.date, 
                           sale_hour: datetime.time) -> int:
        return 1
    
    def insert_sale_detail(self, sale_id: int, product_id: int, quantity: int, unit_price: Decimal, subtotal: Decimal) -> None:
        pass

    def update_sale_fiscal_status(self, sale_id: int, status: bool) -> None:
        pass


class FakeManagePricesDAO:
    def __init__(self, session):
        pass

    def select_id_name_price(self, barcode: str) -> Tuple[int, str, str, Decimal]:
        return 1, "1234567890123", "COCA COLA", 20 

    def update_price_in_db(self, product_id: int, new_price: float) -> None:
        pass


class FakeCheckStockDAO:
    def __init__(self, session):
        pass

    def select_name_quantity(self, barcode: str) -> Tuple[int, str, str, int]:
        return 1, "1234567890123", "COCA COLA", 2