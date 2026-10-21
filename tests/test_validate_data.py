import unittest
from validate_data import check_line_totals


class TestLineTotals(unittest.TestCase):

    def test_invalid_line_total_is_detected(self):
        test_items = [
            {
                "order_item_id": "9999",
                "unit_price": "10.00",
                "quantity": "2",
                "line_total": "25.00"
            }
        ]

        result = check_line_totals(test_items)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
