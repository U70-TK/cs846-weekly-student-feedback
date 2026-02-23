import unittest
import math

from calc_rev import calculate_total_revenue


class TestRevenueValid(unittest.TestCase):
    def test_happy_path(self):
        """Test basic functionality with valid transactions"""
        transactions = [
            {"product": "Widget A", "quantity": 5, "price": 10.50},
            {"product": "Widget B", "quantity": 3, "price": 15.00},
            {"product": "Widget C", "quantity": 2, "price": 8.75}
        ]
        
        result = calculate_total_revenue(transactions)
        expected = 5 * 10.50 + 3 * 15.00 + 2 * 8.75  # = 52.5 + 45 + 17.5 = 115.0
        self.assertEqual(result, expected)
        self.assertAlmostEqual(result, 115.0, places=2)

    def test_single_transaction(self):
        """Test with a single transaction"""
        transactions = [
            {"product": "Widget", "quantity": 10, "price": 5.50}
        ]
        
        result = calculate_total_revenue(transactions)
        self.assertEqual(result, 55.0)

    def test_large_quantities(self):
        """Test with large quantities"""
        transactions = [
            {"product": "Widget", "quantity": 1000, "price": 0.01}
        ]
        
        result = calculate_total_revenue(transactions)
        self.assertEqual(result, 10.0)

    def test_float_prices(self):
        """Test with floating point prices"""
        transactions = [
            {"product": "Widget A", "quantity": 2, "price": 3.333},
            {"product": "Widget B", "quantity": 3, "price": 4.444}
        ]
        
        result = calculate_total_revenue(transactions)
        expected = 2 * 3.333 + 3 * 4.444
        self.assertAlmostEqual(result, expected, places=10)

    def test_many_transactions(self):
        """Test with many transactions"""
        transactions = [
            {"product": f"Widget {i}", "quantity": i, "price": 1.0}
            for i in range(1, 101)
        ]
        
        result = calculate_total_revenue(transactions)
        expected = sum(i * 1.0 for i in range(1, 101))
        self.assertEqual(result, expected)

    def test_empty_string_product(self):
        """Test that empty string product is rejected"""
        transactions = [
            {"product": "", "quantity": 5, "price": 10.50}
        ]
        
        with self.assertRaises(ValueError):
            calculate_total_revenue(transactions)

    def test_whitespace_only_product(self):
        """Test that whitespace-only product is rejected"""
        transactions = [
            {"product": "   ", "quantity": 5, "price": 10.50}
        ]
        
        with self.assertRaises(ValueError):
            calculate_total_revenue(transactions)


class TestRevenueInvalid(unittest.TestCase):
    def test_none_transactions(self):
        """Test that None transactions raises ValueError"""
        with self.assertRaises(ValueError) as context:
            calculate_total_revenue(None)
        self.assertIn("none", str(context.exception).lower())

    def test_empty_list(self):
        """Test that empty list raises ValueError"""
        with self.assertRaises(ValueError) as context:
            calculate_total_revenue([])
        self.assertIn("cannot be empty", str(context.exception).lower())

    def test_non_list_input(self):
        """Test that non-list input raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_total_revenue("not a list")
        
        with self.assertRaises(ValueError):
            calculate_total_revenue(123)
        
        with self.assertRaises(ValueError):
            calculate_total_revenue({"key": "value"})

    def test_missing_keys(self):
        """Test that missing required keys raise ValueError"""
        # Missing product
        with self.assertRaises(ValueError) as context:
            calculate_total_revenue([{"quantity": 5, "price": 10.50}])
        self.assertIn("missing", str(context.exception).lower())
        
        # Missing quantity
        with self.assertRaises(ValueError) as context:
            calculate_total_revenue([{"product": "Widget", "price": 10.50}])
        self.assertIn("missing", str(context.exception).lower())
        
        # Missing price
        with self.assertRaises(ValueError) as context:
            calculate_total_revenue([{"product": "Widget", "quantity": 5}])
        self.assertIn("missing", str(context.exception).lower())

    def test_invalid_product_type(self):
        """Test that non-string product raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": 123, "quantity": 5, "price": 10.50}])
        
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": None, "quantity": 5, "price": 10.50}])

    def test_invalid_quantity(self):
        """Test that invalid quantity raises ValueError"""
        # Non-numeric quantity
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": "five", "price": 10.50}])
        
        # Zero quantity
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": 0, "price": 10.50}])
        
        # Negative quantity
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": -5, "price": 10.50}])
        
        # Float quantity (should be integer)
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": 5.5, "price": 10.50}])
        
        # NaN quantity
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": float("nan"), "price": 10.50}])

    def test_invalid_price(self):
        """Test that invalid price raises ValueError"""
        # Non-numeric price
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": 5, "price": "ten"}])
        
        # Zero price
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": 5, "price": 0}])
        
        # Negative price
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": 5, "price": -10.50}])
        
        # NaN price
        with self.assertRaises(ValueError):
            calculate_total_revenue([{"product": "Widget", "quantity": 5, "price": float("nan")}])

    def test_non_dict_transaction(self):
        """Test that non-dict transactions raise ValueError"""
        with self.assertRaises(ValueError):
            calculate_total_revenue(["not a dict"])
        
        with self.assertRaises(ValueError):
            calculate_total_revenue([123])

    def test_mixed_valid_invalid(self):
        """Test that invalid transaction in list raises ValueError"""
        transactions = [
            {"product": "Widget A", "quantity": 5, "price": 10.50},
            {"product": "Widget B", "quantity": -3, "price": 15.00}  # Invalid
        ]
        
        with self.assertRaises(ValueError):
            calculate_total_revenue(transactions)


if __name__ == "__main__":
    unittest.main()
