#  Import necessary libraries 
import streamlit as st
import backend as sc
import os



class StreamlitFrontend:
    """
    Main class for the Streamlit application.
    Manages UI state and component rendering.
    """

    #  Text Dictionary 
    # All display text is stored here, keyed by language.
    TEXT = {
        "en": {
            "welcome_title": "Choose your language!",
            "welcome_activity": "🎯 Check how many times you would have won the hungarian lottery!",
            "welcome_goals": "🍀 Submit your lucky numbers and check how many times you would have won the lottery if"
                             " you had played every game since the beginning of the lottery!",
            "disclaimer_title": "⚠️ User agreement and Data Policy",
            "disclaimer_text": """I confirm that I have read the User Agreement and Data Policy documents
                               and agree to the terms of the service.""",
            "user_agreement": "User Agreement",
            "data_policy": "Data Policy",
            "user_agreement_doc": "agreement_en.pdf",
            "data_policy_doc": "policy_en.pdf",
            "accept_button": "✅ Next",
            "back_button": "⬅️ Back",
            "selector_title": "Choose the type of lottery!",
            "rules_title": "📜 Rules and guide",
            "rules_file": "rules_en.txt",
            "selector_matches": "🎯 Pick the number of matches.",
            "picker_title_hu5": "🎲 Pick your 5 lottery numbers.",
            "picker_title_hu6": "🎲 Pick your 6 lottery numbers.",
            "picker_title_hu7": "🎲 Pick your 7 lottery numbers.",
            "submit_button": "Submit",
            "results_header": "🎰 Lottery Results",
            "results_lucky": "🍀 Your lucky numbers:",
            "results_match": "🎯 Match count:",
            "date_col": "🗓️ Draw Date",
            "draw_numbers": "🎰 Numbers",
            "matches_col": "⭐ Matches",
            "numbers_mech_col": "🎰 Mechanical draw",
            "matches_mech_col": "⭐ Matches",
            "numbers_manual_col": "🎰 Manual draw",
            "matches_manual_col": "⭐ Matches",
            "success_hu5_hu6": "🎉 You would have won in {wins} draws out of {length} draws since the start of the lottery! 🎉",
            "success_hu7": "🎉 You would have won in {wins} draws out of {length} draws since the start of the lottery! 🎉",
            "last_update": "🔄 Last database update: 02/11/2025",
            "limit": "*results are limited to 20 rows for efficient display."
        },
        "hu": {
            "welcome_title": "Válassz nyelvet!",
            "welcome_activity": "🎯 Tudd meg, hányszor nyertél volna a magyar lottón!",
            "welcome_goals": "🍀 Add meg a nyerőszámaid, és tudd meg, hányszor nyertél volna a lottón, ha a lottó"
                             " kezdete óta minden húzáson részt vettél volna!",
            "disclaimer_title": "⚠️ Felhasználási Feltételek és Adatkezelési Tájékoztató",
            "disclaimer_text": """Megerősítem, hogy elolvastam a Felhasználási Feltételek és Adatkezelési Tájékoztató
                               dokumentumokat, és elfogadom a szolgáltatás feltételeit.""",
            "user_agreement": "Felhasználási Feltételek",
            "data_policy": "Adatkezelési Tájékoztató",
            "user_agreement_doc": "agreement_hu.pdf",
            "data_policy_doc": "policy_hu.pdf",
            "accept_button": "✅ Tovább",
            "back_button": "⬅️ Vissza",
            "selector_title": "🎰 Válaszd ki a lottó típusát!",
            "selector_matches": "🎯 Válaszd ki a találatok számát!",
            "rules_title": "📜 Szabályok és útmutató",
            "rules_file": "rules_hu.txt",
            "picker_title_hu5": "🎲 Add meg az 5 nyerőszámod!",
            "picker_title_hu6": "🎲 Add meg a 6 nyerőszámod!",
            "picker_title_hu7": "🎲 Add meg a 7 nyerőszámod!",
            "submit_button": "Lássuk!",
            "results_header": "🎰 Eredmények",
            "results_lucky": "🍀 Nyerőszámaid:",
            "results_match": "🎯 Találatok száma:",
            "date_col": "🗓️ Húzás dátuma",
            "draw_numbers": "🎰 Kihúzott számok",
            "matches_col": "⭐ Találatok száma",
            "numbers_mech_col": "🎰 Gépi húzás",
            "matches_mech_col": "⭐ Találatok száma",
            "numbers_manual_col": "🎰 Kézi húzás",
            "matches_manual_col": "⭐ Találatok száma",
            "success_hu5_hu6": "🎉 Az eddigi {length} húzásból {wins} húzáson lett volna találatod! 🎉",
            "success_hu7": "🎉 Az eddigi {length} húzásból {wins} húzáson lett volna találatod! 🎉",
            "last_update": "🔄 Adatbázis utolsó frissítése: 2025.11.02.",
            "limit": "*az eredmények 20 sorra vannak korlátozva."
        }
    }

    #  Rules Dictionary 
    # This dictionary drives the dynamic number picker page, with the lottery rules.
    LOTTERY_RULES = {
        'hu5': {
            'limit': 5,
            'max_num': 90,
            'cols': 10,
            'session_key': 'selected_numbers_hu5'
        },
        'hu6': {
            'limit': 6,
            'max_num': 45,
            'cols': 9,
            'session_key': 'selected_numbers_hu6'
        },
        'hu7': {
            'limit': 7,
            'max_num': 35,
            'cols': 7,
            'session_key': 'selected_numbers_hu7'
        }
    }

    #  Helper Methods

    def _clear_session_keys(self, keys_to_clear):
        """
        A helper function to remove a list of keys from session_state.
        Used for 'Back' buttons to reset state.
        """
        for key in keys_to_clear:
            st.session_state.pop(key, None)

    #  Page Rendering Methods 

    def _welcome_page(self):
        """Streamlit Welcome Page for language selection."""
        st.set_page_config(page_title='Would I have won?', page_icon="🎲", layout="wide")

        st.title(self.TEXT["hu"]["welcome_activity"])
        st.title(self.TEXT["en"]["welcome_activity"])
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.title(self.TEXT["hu"]["welcome_title"])
        with col2:
            st.title(self.TEXT["en"]["welcome_title"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Magyar", width='stretch', type="secondary"):
                st.session_state["language"] = "hu"
                st.rerun()
            st.image("hu.png", width='stretch')

        with col2:
            if st.button("English", width='stretch', type="secondary"):
                st.session_state["language"] = "en"
                st.rerun()
            st.image("en.png", width='stretch')

    def _disclaimer_page(self, txt):

        # Initialize session state for UI toggles and PDF memory caching
        if "pdf_cache" not in st.session_state:
            st.session_state.pdf_cache = {"agreement": None, "policy": None}
        if "show_docs" not in st.session_state:
            st.session_state.show_docs = {"agreement": False, "policy": False}

        st.set_page_config(page_title='Would I have won?', page_icon="🎲", layout="wide")
        st.title(txt["disclaimer_title"])

        col1, col2 = st.columns(2)

        with col1:
            # 1. Ensure the URL is in cache before showing the button
            if not st.session_state.pdf_cache.get("agreement"):
                # We fetch this once so the link is ready
                st.session_state.pdf_cache["agreement"] = sc.get_pdf(txt["user_agreement_doc"])

        # 2. Render the link button
        # This automatically opens in a new tab and avoids pop-up blockers
        st.link_button(
            txt["user_agreement"],
            st.session_state.pdf_cache["agreement"],
            use_container_width=True,
            type="secondary"
        )

        with col2:
            # 1. Ensure the URL is in cache
            if not st.session_state.pdf_cache.get("policy"):
                st.session_state.pdf_cache["policy"] = sc.get_pdf(txt["data_policy_doc"])

        # 2. Render the link button
        st.link_button(
            txt["data_policy"],
            st.session_state.pdf_cache["policy"],
            use_container_width=True,
            type="secondary"
        )

        st.divider()

        agreed = st.checkbox(txt["disclaimer_text"])

        if agreed:
            if st.button(txt["accept_button"], type="secondary"):
                st.session_state["disclaimer_accepted"] = True
                st.rerun()

        st.button(txt["back_button"], on_click=self._clear_session_keys, args=(['language'],))

    def _lottery_type_page(self, txt):
        """
        Display the main lottery selection buttons.
        """
        st.set_page_config(page_title='Would I have won?', page_icon="🎲", layout="centered")
        st.title(txt["selector_title"])

        col1, col2, col3 = st.columns(3)

        # Highlight button if it's the currently selected lottery
        def get_button_type(lottery_id):
            if "lottery_id" not in st.session_state:
                return "secondary"
            return "primary" if st.session_state["lottery_id"] == lottery_id else "secondary"

        with col1:
            if st.button("Ötöslottó", width='stretch', type=get_button_type("hu5")):
                st.session_state["lottery_id"] = "hu5"
                st.rerun()

        with col2:
            if st.button("Hatoslottó", width='stretch', type=get_button_type("hu6")):
                st.session_state["lottery_id"] = "hu6"
                st.rerun()

        with col3:
            if st.button("Skandináv lottó", width='stretch', type=get_button_type("hu7")):
                st.session_state["lottery_id"] = "hu7"
                st.rerun()

        col4, col5 = st.columns([1, 2])

        with col4:
            # Back button resets the disclaimer and all lottery-related states
            back_keys = [
                "disclaimer_accepted", "lottery_id",
                "selected_numbers_hu5", "selected_numbers_hu6", "selected_numbers_hu7",
                "get_winning_numbers",
            ]
            st.button(txt["back_button"], on_click=self._clear_session_keys, width='stretch', args=(back_keys,))

        with col5:
            if st.button(txt["rules_title"], width='stretch', type=get_button_type("rules")):
                st.session_state["rules"] = True
                st.rerun()

    def rules_page(self, txt):
        st.set_page_config(page_title='Would have I won?', page_icon="🎲", layout="centered")
        st.title(txt["rules_title"])

        # Back button resets the disclaimer and all lottery-related states
        back_keys = [
            "lottery_id", 'rules'
        ]
        st.button(txt["back_button"], on_click=self._clear_session_keys, args=(back_keys,))

        # Sanity check: Try to read the disclaimer file.
        try:
            with open(txt["rules_file"], 'r', encoding='utf-8') as file:
                st.write(file.read())
        except FileNotFoundError:
            st.error(f"Error: Rules file not found at '{os.path.abspath(txt['rules_file'])}'.")
            # Still show buttons so user can go back.
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")

    def _number_picker_page(self, _lottery_id, txt):
        """
        A single, dynamic page for picking numbers.
        """
        st.set_page_config(page_title='Would I have won?', page_icon="🎲", layout="centered")

        # Get the rules for this lottery
        try:
            rules = self.LOTTERY_RULES[_lottery_id]
        except KeyError:
            st.error("Invalid lottery type selected. Please go back.")
            st.button(txt["back_button"], on_click=self._clear_session_keys, args=(['lottery_id'],))
            return

        limit = rules['limit']
        max_num = rules['max_num']
        num_cols = rules['cols']

        # Main session key for picked numbers
        session_key = rules['session_key']

        # Dynamic session key for selected matches
        matches_key = f"matches_{_lottery_id}"

        #  Initialize/Validate state for match filter
        if (matches_key not in st.session_state or
                st.session_state[matches_key] > limit):
            st.session_state[matches_key] = limit

        #  Main number picking logic (unchanged) 
        def toggle_number(num: int, lim):
            """Helper function to add/remove a number from the set."""
            if num in st.session_state[session_key]:
                st.session_state[session_key].remove(num)
            elif len(st.session_state[session_key]) < lim:
                st.session_state[session_key].add(num)

        # Helper function for match filter
        def set_matches(num: int):
            """Helper function to set the number of matches to filter for."""
            st.session_state[matches_key] = num

        st.title(txt["selector_matches"])

        #  Match filter selector
        cols = st.columns(num_cols)
        for j in range(1, limit + 1):
            col_index = (j - 1) % num_cols
            colp = cols[col_index]

            with colp:
                # Check against the dynamic session state variable
                selected = (j == st.session_state[matches_key])
                btn_type = "primary" if selected else "secondary"

                if st.button(str(j), key=f"match_{_lottery_id}_{j}", width='stretch', type=btn_type):
                    set_matches(j)
                    st.rerun()

            if j % num_cols == 0 and j != limit:
                cols = st.columns(num_cols)

        #  Main number picker
        st.title(txt[f"picker_title_{_lottery_id}"])

        # Initialize main number set
        if session_key not in st.session_state:
            st.session_state[session_key] = set()

        #  Draw the number grid dynamically
        cols = st.columns(num_cols)
        for i in range(1, max_num + 1):
            col_index = (i - 1) % num_cols
            col = cols[col_index]

            with col:
                selected = i in st.session_state[session_key]
                btn_type = "primary" if selected else "secondary"

                if st.button(str(i), key=f"num_{_lottery_id}_{i}", width='stretch', type=btn_type):
                    toggle_number(i, limit)
                    st.rerun()

            # Start a new row
            if i % num_cols == 0 and i != max_num:
                cols = st.columns(num_cols)

        #  Dynamic Submit Button
        is_disabled = len(st.session_state[session_key]) != limit
        if st.button(txt["submit_button"], type="primary", width='stretch', disabled=is_disabled):
            st.session_state.get_winning_numbers = True
            st.rerun()

    def _results_page(self, _language, _lottery_id, _user_input, txt):
        """
        Fetches and displays the results.
        """

        #  Call Backend 
        # Show a spinner while fetching data
        with st.spinner("Checking results..."):
            try:
                results, length, wins = sc.WinningNumbers(_lottery_id, _user_input).check_lottery_numbers()
            except Exception as e:
                st.error(f"An error occurred while fetching results: {e}")
                st.button(txt["back_button"], on_click=self._clear_session_keys, args=(['get_winning_numbers'],))
                return

        st.set_page_config(page_title='Would I have won?', page_icon="🎲", layout="wide")
        st.header(txt["results_header"])
        st.header(txt["last_update"])
        col1, col2 = st.columns([2,1])
        with col1:
            st.header(txt["results_lucky"]+f" {', '.join([str(s) for s in _user_input])}")
        with col2:
            st.header(txt["results_match"]+f" {st.session_state[f"matches_{_lottery_id}"]}")

        st.write(txt["limit"])


        #  Display Results
        if _lottery_id == "hu7":
            # 5-column layout for hu7
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.subheader(txt["date_col"])
            with col2:
                st.subheader(txt["numbers_mech_col"])
            with col3:
                st.subheader(txt["matches_mech_col"])
            with col4:
                st.subheader(txt["numbers_manual_col"])
            with col5:
                st.subheader(txt["matches_manual_col"])

            st.divider()

            for r in results:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.write(r[0])  # Date
                with col2:
                    st.write(', '.join([str(s) for s in r[1]]))  # Numbers A
                with col3:
                    st.write(r[2])  # Match A
                with col4:
                    st.write(', '.join([str(s) for s in r[3]]))  # Numbers A
                with col5:
                    st.write(r[4])  # Match B

            # Complex win calculation for hu7
            st.success(txt["success_hu7"].format(wins=wins, length=length))

        elif _lottery_id == "hu5" or _lottery_id == "hu6":
            # 3-column layout for hu5/hu6
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(txt["date_col"])
            with col2:
                st.subheader(txt["draw_numbers"])
            with col3:
                st.subheader(txt["matches_col"])

            st.divider()

            for r in results:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(r[0])  # Date
                with col2:
                    st.write(', '.join([str(s) for s in r[1]])) # Numbers
                with col3:
                    st.write(r[2])  # Match Count

            # Simple win calculation
            st.success(txt["success_hu5_hu6"].format(wins=wins, length=length))

        # Back button to return to the number picker
        st.button(txt["back_button"], on_click=self._clear_session_keys, args=(['get_winning_numbers'],))

    def call_pages(self, page, language=None, txt=None, lottery_id=None, selected_numbers=None):
        """
        Calls the correct page rendering method based on the 'page' string.
        """

        if page == 'welcome':
            return self._welcome_page()

        elif page == 'disclaimer':
            return self._disclaimer_page(txt)

        elif page == 'selector':
            return self._lottery_type_page(txt)

        elif page == 'rules':
            return self.rules_page(txt)

        elif page == 'picker':
            return self._number_picker_page(lottery_id, txt)

        elif page == 'results':
            return self._results_page(language, lottery_id, selected_numbers, txt)

        else:
            raise ValueError(f"Invalid page ID: {page}")

def run_app():
    """
    Main application router.
    Uses a "guard clause" pattern to show the correct page.
    The script stops execution with 'return' after rendering each page.
    """
    frontend = StreamlitFrontend()

    #  Page 1: Welcome / Language Selection 
    if "language" not in st.session_state:
        frontend.call_pages('welcome')
        return

    #  Language is set, get the correct text 
    # Default to English if language state is somehow invalid
    txt = frontend.TEXT.get(st.session_state["language"], frontend.TEXT["en"])

    #  Page 2: Disclaimer 
    if not st.session_state.get("disclaimer_accepted", False):
        frontend.call_pages('disclaimer', txt=txt)
        return

    #  Page 3: Lottery Selector 
    if ("language" in st.session_state and
            st.session_state.get("disclaimer_accepted", True) and
            "get_winning_numbers" not in st.session_state and
            "rules" not in st.session_state
    ):
        frontend.call_pages('selector', txt=txt)

    # Subpage 1: Rules
    if ("language" in st.session_state and
            st.session_state.get("disclaimer_accepted", True) and
            "rules" in st.session_state
    ):
        frontend.call_pages('rules', txt=txt)

    #  Page 4: Number Picker 
    # Check this *before* the lottery selector.
    if ("language" in st.session_state and
            st.session_state.get("disclaimer_accepted", True) and
            "lottery_id" in st.session_state and
            "get_winning_numbers" not in st.session_state and
            "rules" not in st.session_state
    ):
        frontend.call_pages('picker', lottery_id=st.session_state["lottery_id"], txt=txt)

    #  Page 5: Results Page 
    if "get_winning_numbers" in st.session_state:
        lottery_id = st.session_state["lottery_id"]
        rules = frontend.LOTTERY_RULES[lottery_id]
        session_key = rules['session_key']
        selected_numbers = list(st.session_state.get(session_key, []))

        frontend.call_pages('results', st.session_state["language"], txt, lottery_id, selected_numbers)
        return

#  Main execution 
if __name__ == "__main__":
    run_app()
