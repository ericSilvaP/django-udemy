from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=2,
        )
        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=3,
        )
        self.assertEqual([2, 3, 4, 5], pagination["pagination"])

    def test_last_range_is_static_if_current_page_is_greater_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 11)),
            pages_qty=4,
            current_page=8,
        )
        self.assertEqual([7, 8, 9, 10], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 11)),
            pages_qty=4,
            current_page=9,
        )
        self.assertEqual([7, 8, 9, 10], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 11)),
            pages_qty=4,
            current_page=10,
        )
        self.assertEqual([7, 8, 9, 10], pagination["pagination"])

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=10,
        )["pagination"]
        self.assertEqual([9, 10, 11, 12], pagination)

        # Current page = 14 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=12,
        )["pagination"]
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        # Current page = 18 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=18,
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 19 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=19,
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 20 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=20,
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 21 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages_qty=4,
            current_page=21,
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)
