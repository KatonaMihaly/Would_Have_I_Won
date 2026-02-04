import unittest
from unittest.mock import patch, MagicMock
import datetime

import pandas as pd

from backend import WinningNumbers

# Mock streamlit for the whole class
@patch('backend.st', new_callable=MagicMock)
class TestWinningNumbersValidation(unittest.TestCase):
    """Tests for all data validation methods."""

    def test_validity_lottery_ok(self, mock_st):
        """Test that valid lottery IDs are accepted."""
        for lid in ['hu5', 'hu6', 'hu7']:
            with self.subTest(lid=lid):
                wn = WinningNumbers(lid, [])
                self.assertEqual(wn._check_validity_lottery(), lid)

    def test_validity_lottery_invalid_str(self, mock_st):
        """Test that invalid string lottery IDs are rejected."""
        wn = WinningNumbers('invalid_id', [])
        self.assertIsNone(wn._check_validity_lottery())
#
    def test_validity_lottery_invalid_type(self, mock_st):
        """Test that non-string-convertible lottery IDs are rejected."""
        wn_int = WinningNumbers(12345, [])
        self.assertIsNone(wn_int._check_validity_lottery())

    def test_validity_match_count_ok(self, mock_st):
        """Test valid match counts for each lottery."""
        # Test hu5 with valid int
        mock_st.session_state = {"matches_hu5": 5}
        wn_hu5 = WinningNumbers('hu5', [])
        self.assertEqual(wn_hu5._check_validity_match_count(), 5)

        # Test hu6 with valid int
        mock_st.session_state = {"matches_hu6": 5}
        wn_hu6 = WinningNumbers('hu6', [])
        self.assertEqual(wn_hu6._check_validity_match_count(), 5)

        # Test hu7 with valid int
        mock_st.session_state = {"matches_hu7": 5}
        wn_hu7 = WinningNumbers('hu7', [])
        self.assertEqual(wn_hu7._check_validity_match_count(), 5)


    def test_validity_match_count_invalid_range(self, mock_st):
        """Test match counts that are integers but out of range."""
        # Test hu5 with invalid range
        mock_st.session_state = {"matches_hu5": 0}
        wn_hu5 = WinningNumbers('hu5', [])
        self.assertIsNone(wn_hu5._check_validity_match_count())

        # Test hu6 with invalid range
        mock_st.session_state = {"matches_hu6": 0}
        wn_hu6 = WinningNumbers('hu6', [])
        self.assertIsNone(wn_hu6._check_validity_match_count())

        # Test hu7 with invalid range
        mock_st.session_state = {"matches_hu7": 0}
        wn_hu7 = WinningNumbers('hu7', [])
        self.assertIsNone(wn_hu7._check_validity_match_count())

    def test_validity_match_count_invalid_type(self, mock_st):
        """Test match counts that are not valid integers."""
        # Test hu5 with invalid int
        mock_st.session_state = {"matches_hu5": 'a'}
        wn_hu5 = WinningNumbers('hu5', [])
        self.assertIsNone(wn_hu5._check_validity_match_count())

        # Test hu6 with invalid int
        mock_st.session_state = {"matches_hu6": 'a'}
        wn_hu6 = WinningNumbers('hu6', [])
        self.assertIsNone(wn_hu6._check_validity_match_count())

        # Test hu7 with invalid int
        mock_st.session_state = {"matches_hu7": 'a'}
        wn_hu7 = WinningNumbers('hu7', [])
        self.assertIsNone(wn_hu7._check_validity_match_count())

    def test_validity_match_count_invalid_lottery_id(self, mock_st):
        """Test that an invalid session state causes a KeyError in __init__."""
        mock_st.session_state = {"matches_hu8": 5}
        wn = WinningNumbers('hu5', [])
        self.assertIsNone(wn._check_validity_match_count())

        # An invalid lottery_id will cause rules[self._lottery_id] to raise a KeyError,
        mock_st.session_state = {"matches_hu5": 5}
        wn = WinningNumbers('hu8', [])
        self.assertIsNone(wn._check_validity_match_count())

    def test_validity_numbers_hu5_ok(self, mock_st):
        """Test valid hu5 numbers (len 5, range 1-90)."""
        valid_nums = [1, 10, 20, 30, 40]
        wn = WinningNumbers('hu5', valid_nums)
        self.assertEqual(wn._check_validity_numbers(), valid_nums)

    def test_validity_numbers_hu5_invalid_length(self, mock_st):
        """Test hu5 with incorrect number count."""
        invalid_nums = [1, 10, 20, 30]  # Only 4
        wn = WinningNumbers('hu5', invalid_nums)
        self.assertIsNone(wn._check_validity_numbers())

    def test_validity_numbers_hu5_invalid_range(self, mock_st):
        """Test hu5 with numbers out of range (1-90)."""
        invalid_nums_high = [1, 10, 20, 30, 91]  # 91 is too high
        wn_high = WinningNumbers('hu5', invalid_nums_high)
        self.assertIsNone(wn_high._check_validity_numbers())

    def test_validity_numbers_hu6_ok(self, mock_st):
        """Test valid hu6 numbers (len 6, range 1-45)."""
        valid_nums = [1, 10, 20, 30, 40, 45]
        wn = WinningNumbers('hu6', valid_nums)
        self.assertEqual(wn._check_validity_numbers(), valid_nums)

    def test_validity_numbers_hu6_invalid_length(self, mock_st):
        """Test hu6 with incorrect number count."""
        invalid_nums = [1, 10, 20, 30, 40]  # Only 5
        wn = WinningNumbers('hu6', invalid_nums)
        self.assertIsNone(wn._check_validity_numbers())

    def test_validity_numbers_hu6_invalid_range(self, mock_st):
        """Test hu6 with number out of range (1-45)."""
        invalid_nums = [1, 10, 20, 30, 40, 46]  # 46 is too high
        wn = WinningNumbers('hu6', invalid_nums)
        self.assertIsNone(wn._check_validity_numbers())

    def test_validity_numbers_hu7_ok(self, mock_st):
        """Test valid hu7 numbers (len 7, range 1-35)."""
        valid_nums = [1, 5, 10, 15, 20, 25, 35]
        wn = WinningNumbers('hu7', valid_nums)
        self.assertEqual(wn._check_validity_numbers(), valid_nums)

    def test_validity_numbers_hu7_invalid_length(self, mock_st):
        """Test hu7 with incorrect number count."""
        invalid_nums = [1, 5, 10, 15, 20, 25]  # Only 6
        wn = WinningNumbers('hu7', invalid_nums)
        self.assertIsNone(wn._check_validity_numbers())

    def test_validity_numbers_hu7_invalid_range(self, mock_st):
        """Test hu7 with number out of range (1-35)."""
        invalid_nums = [1, 5, 10, 15, 20, 25, 36]  # 36 is too high
        wn = WinningNumbers('hu7', invalid_nums)
        self.assertIsNone(wn._check_validity_numbers())

    def test_validity_numbers_empty(self, mock_st):
        """Test that an empty list is rejected."""
        wn = WinningNumbers('hu5', [])
        self.assertIsNone(wn._check_validity_numbers())

    def test_validity_numbers_non_int(self, mock_st):
        """Test that a list with non-integers is rejected."""
        wn = WinningNumbers('hu5', [1, 2, 'a', 4, 5])
        self.assertIsNone(wn._check_validity_numbers())


@patch('backend.st', new_callable=MagicMock)
class TestWinningNumbersQueries(unittest.TestCase):
    """
    Tests the main check_lottery_numbers method and _run_db_queries
    with mocked database interaction to test the logic.
    """

    def setUp(self):
        """Create a standard date object and match count for mocking."""
        self.mock_date = datetime.datetime(2023, 1, 1)
        self.mock_match_count = 2

    @patch('backend.WinningNumbers._run_db_queries')
    def test_check_lottery_numbers_hu5_success(self, mock_run_db_queries, mock_st):
        """Test the hu5 logic with mocked db results."""
        # 1. Define mock results in the format of check_lottery_numbers output.
        # (date, [draw numbers], match count, draw matches)
        mock_raw_results = [(self.mock_date, [1, 2, 6, 7, 8], 2, 1)]
        mock_total_draws = 50
        mock_run_db_queries.return_value = (mock_raw_results, mock_total_draws)

        # Set the session state for this test
        mock_st.session_state = {"matches_hu5": self.mock_match_count}

        # Set user inputs
        valid_nums = [1, 2, 3, 4, 5]
        wn = WinningNumbers('hu5', valid_nums)

        # 2. Call the main method
        results, total_draws, winning_draws = wn.check_lottery_numbers()

        # 3. Assert the results are correctly formatted
        expected_results = [("2023-01-01", [1, 2, 6, 7, 8], 2)]
        self.assertEqual(results, expected_results)
        self.assertEqual(total_draws, mock_total_draws)
        self.assertEqual(winning_draws, 1)

    @patch('backend.WinningNumbers._run_db_queries')
    def test_check_lottery_numbers_hu6_success(self, mock_run_db_queries, mock_st):
        """Test the hu5 logic with mocked db results."""
        # 1. Define mock results in the format of check_lottery_numbers output.
        # (date, [draw numbers], match count, draw matches)
        mock_raw_results = [(self.mock_date, [1, 2, 7, 8, 9, 10], 2, 1)]
        mock_total_draws = 50
        mock_run_db_queries.return_value = (mock_raw_results, mock_total_draws)

        # Set the session state for this test
        mock_st.session_state = {"matches_hu6": self.mock_match_count}

        # Set user inputs
        valid_nums = [1, 2, 3, 4, 5, 6]
        wn = WinningNumbers('hu6', valid_nums)

        # 2. Call the main method
        results, total_draws, winning_draws = wn.check_lottery_numbers()

        # 3. Assert the results are correctly formatted
        expected_results = [("2023-01-01", [1, 2, 7, 8, 9, 10], 2)]
        self.assertEqual(results, expected_results)
        self.assertEqual(total_draws, mock_total_draws)
        self.assertEqual(winning_draws, 1)

    @patch('backend.WinningNumbers._run_db_queries')
    def test_check_lottery_numbers_hu7_success(self, mock_run_db_queries, mock_st):
        """Test the hu7 logic with mocked db results."""
        # 1. Define mock results in the format of check_lottery_numbers output.
        # (date, [draw numbers], match count, draw matches)
        mock_raw_results = [(self.mock_date, [1, 2, 8, 9, 10, 11, 12], 2, [1, 2, 3, 13, 14, 15, 16], 3, 1)]
        mock_total_draws = 50
        mock_run_db_queries.return_value = (mock_raw_results, mock_total_draws)

        # Set the session state for this test
        mock_st.session_state = {"matches_hu7": self.mock_match_count}

        # Set user inputs
        valid_nums = [1, 2, 3, 4, 5, 6, 7]
        wn = WinningNumbers('hu7', valid_nums)

        # 2. Call the main method
        results, total_draws, winning_draws = wn.check_lottery_numbers()

        # 3. Assert the results are correctly formatted
        expected_results = [("2023-01-01", [1, 2, 8, 9, 10, 11, 12], 2, [1, 2, 3, 13, 14, 15, 16], 3)]
        self.assertEqual(results, expected_results)
        self.assertEqual(total_draws, mock_total_draws)
        self.assertEqual(winning_draws, 1)

    @patch('backend.WinningNumbers._run_db_queries')
    def test_check_lottery_numbers_invalid_id(self, mock_run_db_queries, mock_st):
        """Test that an invalid lottery ID stops execution."""
        mock_st.session_state = {"matches_hu5": self.mock_match_count}
        wn = WinningNumbers('invalid', [1, 2, 3, 4, 5])
        results, total_draws, winning_draws = wn.check_lottery_numbers()
#
        # Assert we get empty results and the db is NOT called
        self.assertEqual(results, [])
        self.assertEqual(total_draws, 0)
        self.assertEqual(winning_draws, 0)
        mock_run_db_queries.assert_not_called()

    @patch('backend.WinningNumbers._run_db_queries')
    def test_check_lottery_numbers_invalid_match_count(self, mock_run_db_queries, mock_st):
        """Test that an invalid lottery ID stops execution."""
        mock_st.session_state = {"matches_hu8": self.mock_match_count}
        wn = WinningNumbers('hu5', [1, 2, 3, 4, 5])
        results, total_draws, winning_draws = wn.check_lottery_numbers()

        # Assert we get empty results and the db is NOT called
        self.assertEqual(results, [])
        self.assertEqual(total_draws, 0)
        self.assertEqual(winning_draws, 0)
        mock_run_db_queries.assert_not_called()

    @patch('backend.WinningNumbers._run_db_queries')
    def test_check_lottery_numbers_h5_invalid_numbers(self, mock_run_db_queries, mock_st):
        """Test that invalid numbers stop execution."""
        mock_st.session_state = {"matches_hu5": self.mock_match_count}
        wn = WinningNumbers('hu5', [1, 2])  # Invalid length
        results, total_draws, winning_draws = wn.check_lottery_numbers()

        # Assert we get empty results and the db is NOT called
        self.assertEqual(results, [])
        self.assertEqual(total_draws, 0)
        self.assertEqual(winning_draws, 0)
        mock_run_db_queries.assert_not_called()

    @patch('backend.WinningNumbers._run_db_queries')
    def test_check_lottery_numbers_h6_invalid_numbers(self, mock_run_db_queries, mock_st):
        """Test that invalid numbers stop execution."""
        mock_st.session_state = {"matches_hu6": self.mock_match_count}
        wn = WinningNumbers('hu6', [1, 2, 3])  # Invalid length
        results, total_draws, winning_draws = wn.check_lottery_numbers()

        # Assert we get empty results and the db is NOT called
        self.assertEqual(results, [])
        self.assertEqual(total_draws, 0)
        self.assertEqual(winning_draws, 0)
        mock_run_db_queries.assert_not_called()

    @patch('backend.WinningNumbers._run_db_queries')
    def test_check_lottery_numbers_h7_invalid_numbers(self, mock_run_db_queries, mock_st):
        """Test that invalid numbers stop execution."""
        mock_st.session_state = {"matches_hu7": self.mock_match_count}
        wn = WinningNumbers('hu6', [1, 2, 3, 4])  # Invalid length
        results, total_draws, winning_draws = wn.check_lottery_numbers()

        # Assert we get empty results and the db is NOT called
        self.assertEqual(results, [])
        self.assertEqual(total_draws, 0)
        self.assertEqual(winning_draws, 0)
        mock_run_db_queries.assert_not_called()

    def test_run_db_queries_success(self, mock_st):
        """Test the _run_db_queries helper method on success."""
        mock_conn = MagicMock()
        mock_df_matches = pd.DataFrame([(self.mock_date, [1, 2, 6, 7, 8], 2)])
        mock_df_total = pd.DataFrame([100])

        mock_conn.query.side_effect = [mock_df_matches, mock_df_total]
        mock_st.connection.return_value = mock_conn

        mock_st.session_state = {"matches_hu5": 2}
        wn = WinningNumbers('hu5', [1, 2, 3, 4, 5])

        results, total_draws = wn._run_db_queries(
            "fake_match_query", {"p": 1}, "fake_total_query", {"p": 2}
        )

        expected_results = [(self.mock_date, [1, 2, 6, 7, 8], 2)]
        self.assertEqual(results, expected_results)
        self.assertEqual(total_draws, 100)

        mock_st.connection.assert_called_once_with("supa_db", type="sql")
        self.assertEqual(mock_conn.query.call_count, 2)
        mock_conn.query.assert_any_call("fake_match_query", params={"p": 1}, ttl="1m")
        mock_conn.query.assert_any_call("fake_total_query", params={"p": 2}, ttl="1m")
        self.assertEqual(results, expected_results)
        self.assertEqual(total_draws, 100)

    def test_run_db_queries_db_error(self, mock_st):
        """
        Test that _run_db_queries catches a connection/query error
        raised by st.connection and returns empty results.
        """
        # 1. Mock st.connection().query to raise an exception
        mock_conn = MagicMock()
        mock_conn.query.side_effect = Exception("Mocked connection failure")
        mock_st.connection.return_value = mock_conn

        # 2. Setup environment and create instance
        mock_st.session_state = {"matches_hu5": 2}
        wn = WinningNumbers('hu5', [1, 2, 3, 4, 5])

        # 3. Call the helper method directly
        results, total_draws = wn._run_db_queries(
            "fake_query", {}, "fake_query_total", {}
        )

        # 4. Assert it catches the error and returns empty results
        self.assertEqual(results, [])
        self.assertEqual(total_draws, 0)


if __name__ == '__main__':
    unittest.main()

