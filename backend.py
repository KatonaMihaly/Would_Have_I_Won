# --- Import necessary libraries ---
import streamlit as st
import queries
from st_supabase_connection import SupabaseConnection


class WinningNumbers:
    """A class to calculate winning numbers"""

    def __init__(self, _lottery_id, _input_numbers):
        """Initialize the class with lottery ID and the user's numbers."""
        self._lottery_id = _lottery_id
        self._input_numbers = _input_numbers

        try:
            self._match_count = st.session_state[f"matches_{_lottery_id}"]
        except KeyError:
            self._match_count = None

        # All DB variables are handled by st.connection
        # and defined in .streamlit/secrets.toml file.

        # Placeholders to store the SQL queries.
        self.query_matches = ""
        self.query_total = ""

    def _check_validity_lottery(self):
        """Validate lottery ID is in the allowed list."""
        # Ensure the lottery_id is a string for comparison
        try:
            lottery_id_str = str(self._lottery_id)

            # Define the list of supported lotteries
            allowed_lotteries = ['hu5', 'hu6', 'hu7']

            # Check if the provided ID is in our allowed list
            if lottery_id_str not in allowed_lotteries:
                # Print an error if invalid and return None
                print(f"Invalid lottery_id value: {lottery_id_str}. Must be one of {allowed_lotteries}")
                return None  # Invalid

            return lottery_id_str  # Return the valid string ID

        except TypeError:
            print("Invalid lottery ID type. Cannot convert to string.")
            return None  # Invalid

    def _check_validity_match_count(self):
        """
        Validates the match count for the current lottery ID from session state.
        Returns the valid match count (int) on success, or None on failure.
        """
        try:
            # 1. Get the rules for the current lottery
            rules = {'hu5': [1, 2, 3, 4, 5], 'hu6': [1, 2, 3, 4, 5, 6], 'hu7': [1, 2, 3, 4, 5, 6, 7]}

            # 2. Get the match range
            match_range = rules[self._lottery_id]

            # 3. Convert to integer
            # This will raise ValueError/TypeError if it's not a valid int
            match_count = int(self._match_count)

            # 4. Check if the integer is in the valid range
            if match_count in match_range:
                return match_count
            else:
                # It's an int, but out of range (e.g., 0 or 8 for a 6-limit)
                return None

        except (KeyError, ValueError, TypeError):
            print(f"Error validating match count for {self._lottery_id}.")
            return None

    def _check_validity_numbers(self):
        """
        Validate numbers:
        - Convert to list of integers.
        - Check for correct length and range based on lottery_id.
        Returns list of valid integers or None if validation fails.
        """
        # Convert input from a set to a list if necessary
        if isinstance(self._input_numbers, set):
            self._input_numbers = list(self._input_numbers)

        # Check if the input list is empty
        if not self._input_numbers:
            print("Error: No numbers provided.")
            return None

        try:
            # Convert all numbers in the list to integers
            numbers_list = [int(n) for n in self._input_numbers]
        except (ValueError, TypeError):
            # Fail if any number cannot be converted to an integer
            print("Error: All input numbers must be convertible to integers.")
            return None  # Failed validation

        # Define validation rules for each lottery type
        rules = {
            'hu5': {'length': 5, 'min': 1, 'max': 90},  # 5 numbers, 1-90
            'hu6': {'length': 6, 'min': 1, 'max': 45},  # 6 numbers, 1-45
            'hu7': {'length': 7, 'min': 1, 'max': 35}  # 7 numbers, 1-35
        }

        # Get the specific rule set for the current lottery_id
        lottery_rule = rules.get(self._lottery_id)

        # Apply the rules if they exist
        if lottery_rule:
            # Check if the correct number of numbers was provided
            if len(numbers_list) != lottery_rule['length']:
                print(
                    f"Error: Lottery '{self._lottery_id}' requires {lottery_rule['length']}"
                    f" numbers, but {len(numbers_list)} were provided.")
                return None  # Failed validation

            # Check if all numbers are within the allowed min/max range
            for num in numbers_list:
                if not (lottery_rule['min'] <= num <= lottery_rule['max']):
                    print(
                        f"Error: Number {num} is out of range for '{self._lottery_id}'"
                        f" ({lottery_rule['min']}-{lottery_rule['max']}).")
                    return None  # Failed validation

        # If all checks pass, return the validated list of integers
        return numbers_list

    def _run_db_queries(self, query_matches, match_params, query_total, total_params):
        """Helper method to connect to the DB and execute queries using st.connection."""
        try:
            # 1. Initialize the connection.
            # This uses secrets.toml by default.
            conn = st.connection("supa_db", type="sql")

            # 2. First query: find all matching draws
            # conn.query() returns a Pandas DataFrame.
            # Pass parameters using the 'params' argument.
            df_matches = conn.query(query_matches, params=match_params, ttl="1m")

            # 3. Second query: find the total number of draws
            df_total = conn.query(query_total, params=total_params, ttl="1m")

            # Convert the matches DataFrame to a list of tuples,
            results = list(df_matches.itertuples(index=False, name=None))

            # Extract the single count value from the total_draws DataFrame
            total_draws = int(df_total.iloc[0, 0])

            # Return the data in the format your other methods expect
            return results, total_draws

        except Exception as e:
            # Handle any query or connection errors
            print(f"Database query error: {e}")
            return [], 0

    def check_lottery_numbers(self):
        """
        Main method to check lottery numbers against the database.
        It validates input, defines queries, runs them, and formats the output.
        """

        formatted_results, total_draws, winning_draws = [], 0, 0

        # Step 1: Validate the lottery ID
        lottery = self._check_validity_lottery()
        if not lottery:
            return formatted_results, total_draws, winning_draws  # Invalid lottery_id, return empty results

        # Step 2: Validate the user's numbers
        numbers = self._check_validity_numbers()
        if not numbers:
            return formatted_results, total_draws, winning_draws  # Invalid numbers, return empty results

        # Step 3: Validate the user's match count
        match_count = self._check_validity_match_count()
        if not match_count:
            return formatted_results, total_draws, winning_draws  # Invalid match count, return empty results

        # Initialize variables
        formatted_results = []
        total_draws = 0

        # --- Logic for 'hu7' (which has two sets of numbers) ---
        if self._lottery_id == 'hu7':
            self.query_matches = queries.MATCHES_HU7
            self.query_total = queries.MATCHES_TOTAL

            match_params = {
                "numbers_a": numbers,
                "id_a": 'hu7a',
                "numbers_b": numbers,
                "id_b": 'hu7b',
                "match_count": match_count
            }
            total_params = {"id": 'hu7a'}

            # Get raw data from DB using the helper method
            raw_results, total_draws = self._run_db_queries(
                self.query_matches, match_params, self.query_total, total_params
            )

            # --- Format results for hu7 (Date, Match A, Match B) ---
            formatted_results = [(row[0].strftime("%Y-%m-%d"), row[1], row[2], row[3], row[4]) for row in
                                 raw_results]

            winning_draws = raw_results[0][-1] if raw_results else 0

        # --- Logic for 'hu5' or 'hu6' (which have one set of numbers) ---
        elif self._lottery_id == 'hu5' or self._lottery_id == 'hu6':
            self.query_matches = queries.MATCHES_HU5_HU6
            self.query_total = queries.MATCHES_TOTAL

            match_params = {"number": numbers, "id": lottery, 'match_count': match_count}
            total_params = {"id": lottery}

            # Get raw data from DB using the helper method
            raw_results, total_draws = self._run_db_queries(
                self.query_matches, match_params, self.query_total, total_params
            )

            # --- Format results for hu5/hu6 (Date, Match Count) ---
            formatted_results = [(row[0].strftime("%Y-%m-%d"), row[1], row[2]) for row in raw_results]

            winning_draws = raw_results[0][-1] if raw_results else 0

        # Return the final formatted results and the total draw count
        return formatted_results, total_draws, winning_draws


# In your Supabase connection logic
def get_pdf_url(document):
    conn = st.connection("supabase", type=SupabaseConnection)
    # Generate a signed URL valid for 15 minutes
    # This URL is a direct link to the Supabase CDN
    return conn.client.storage.from_("Documents").create_signed_url(document, expires_in=900)

