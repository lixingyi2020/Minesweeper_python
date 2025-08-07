import unittest
from mine_field import _get_around

class GetAroundTest(unittest.TestCase):
    def test_center_position(self):
        """Test getting surrounding coordinates for a center position (x=15, y=8) with default width and height."""
        x = 15
        y = 8
        expected = [(14, 7), (14, 8), (14, 9), (15, 7), (15, 9), (16, 7), (16, 8), (16, 9)]
        result = _get_around(x, y)
        self.assertEqual(result, expected)

    def test_top_left_corner_position(self):
        """Test getting surrounding coordinates for the top-left corner (x=0, y=0)"""
        x = 0
        y = 0
        expected = [(0, 1), (1, 0), (1, 1)]
        result = _get_around(x, y)
        self.assertEqual(result, expected)

    def test_bottom_right_corner_position(self):
        """Test getting surrounding coordinates for the bottom-right corner (x=29, y=15) with default width and height"""
        x = 29
        y = 15
        expected = [(28, 14), (28, 15), (29, 14)]
        result = _get_around(x, y)
        self.assertEqual(result, expected)

    def test_left_edge_position(self):
        """Test getting surrounding coordinates for a position on the left edge (x=0, y=8)"""
        x = 0
        y = 8
        expected = [(0,7), (0,9), (1,7), (1,8), (1,9)]
        result = _get_around(x, y)
        self.assertEqual(result, expected)

    def test_right_edge_position(self):
            """Test getting surrounding coordinates for a position on the right edge (x=29, y=8)"""
            x = 29
            y = 8
            expected = [(28,7), (28,8), (28,9), (29,7), (29,9)]
            result = _get_around(x, y)
            self.assertEqual(result, expected)

    def test_top_edge_position(self):
            """Test getting surrounding coordinates for a position on the top edge (x=15, y=0)"""
            x = 15
            y = 0
            expected = [(14,0), (14,1), (15,1), (16,0), (16,1)]
            result = _get_around(x, y)
            self.assertEqual(result, expected)  

    def test_bottom_edge_position(self):
        """Test getting surrounding coordinates for a position on the bottom edge (x=15, y=15)"""
        x = 15
        y = 15
        expected = [(14, 14), (14, 15), (15, 14), (16, 14), (16, 15)]
        result = _get_around(x, y)
        self.assertEqual(result, expected)

    def test_get_around_single_cell_grid(self):
        """Test getting surrounding coordinates in a 1x1 grid"""
        x, y = 0, 0
        width, height = 1, 1
        result = _get_around(x, y, width, height)
        self.assertEqual(result, [], "Should return empty list for single cell grid")

    def test_get_around_negative_coordinates(self):
        """Test getting surrounding coordinates for negative input coordinates"""
        # Input
        x = -1
        y = -1
        
        # Expected outcome
        expected = []
        
        # Call the function
        result = _get_around(x, y)
        
        # Assert the result matches expected
        self.assertEqual(result, expected)

    def test_get_around_coordinates_beyond_grid_dimensions(self):
        """Test getting surrounding coordinates for coordinates beyond grid dimensions"""
        # Input
        x = 31
        y = 18
        width = 30
        height = 16
        
        # Expected outcome
        expected = []
        
        # Call the function
        result = _get_around(x, y, width, height)
        
        # Assert the result matches expected outcome
        self.assertEqual(result, expected)

    def test_minimum_valid_grid_size(self):
        """Test getting surrounding coordinates in a 2x2 grid"""
        x = 0
        y = 0
        width = 2
        height = 2
        expected = [(0, 1), (1, 0), (1, 1)]
        result = _get_around(x, y, width, height)
        self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()
