from pathfinding.cell import Cell
from utils.position import Position
from nose.tools import *


class TestCell:
    def test_area_should_return_width_by_height(self):
        # Given
        height = 41;
        width = 42;
        cell = Cell(width, height, 0, 0)

        # When
        actual_area = cell.area()

        # Then
        expected_area = width * height
        assert_equals(expected_area, actual_area)

    def test_contains_point_should_return_true_if_point_is_inside_cell_boundaries(self):
        # Given
        height = 10;
        width = 10;
        cell = Cell(width, height, 5, 5)
        point = Position(3, 3)

        # When
        is_contained = cell.contains_point(point)

        # Then
        assert_true(is_contained)

    def test_contains_point_should_return_false_if_point_is_not_inside_cell_boundaries(self):
        # Given
        height = 10;
        width = 10;
        cell = Cell(width, height, 5, 5)
        point = Position(15, 15)

        # When
        is_contained = cell.contains_point(point)

        # Then
        assert_false(is_contained)

