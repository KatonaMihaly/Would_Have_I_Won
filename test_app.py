import pytest
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# --- Import Edge-specific classes ---
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --- Pytest Fixtures ---
# Set up and tear down resources for your tests.
@pytest.fixture(scope="module")
def app_server():
    """
    Fixture to start and stop the Streamlit app server
    in a separate process.
    """
    # Start the Streamlit app on a specific port
    port = "8511"
    url = f"http://localhost:{port}"

    # Use subprocess.Popen to run Streamlit in the background
    try:
        proc = subprocess.Popen(
            ["streamlit", "run", "streamlit_app.py", "--server.port", port, "--server.headless", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Give the server a few seconds to boot up
        time.sleep(5)

        # Yield the URL to the test function
        yield url

    finally:
        # Teardown: stop the server after the test is done
        proc.kill()


@pytest.fixture(scope="function")
def driver():
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu") # Helpful for PDF rendering issues

    service = EdgeService(executable_path=r"msedgedriver.exe")
    driver_instance = webdriver.Edge(service=service, options=options)
    yield driver_instance
    driver_instance.quit()


# --- Parameterized Test Cases ---
# Each tuple contains the parameters for one full test run.
test_cases = [
    # (test_id, lang_btn, accept_btn, lottery_btn, num_clicks, submit_btn, result_header, success_msg_part)
    ('hu5_en', 'English', '✅ Next', 'Ötöslottó', 5, 'Submit', '🎰 Lottery Results', 'You would have won'),
    ('hu6_en', 'English', '✅ Next', 'Hatoslottó', 6, 'Submit', '🎰 Lottery Results', 'You would have won'),
    ('hu7_en', 'English', '✅ Next', 'Skandináv lottó', 7, 'Submit', '🎰 Lottery Results', 'You would have won'),
    ('hu5_hu', 'Magyar', '✅ Tovább', 'Ötöslottó', 5, 'Lássuk!', '🎰 Eredmények', 'lett volna találatod! 🎉'),
    ('hu6_hu', 'Magyar', '✅ Tovább', 'Hatoslottó', 6, 'Lássuk!', '🎰 Eredmények', 'lett volna találatod! 🎉'),
    ('hu7_hu', 'Magyar', '✅ Tovább', 'Skandináv lottó', 7, 'Lássuk!', '🎰 Eredmények', 'lett volna találatod! 🎉'),
]

@pytest.mark.parametrize(
    "test_id, lang_btn, accept_btn, lottery_btn, num_clicks, submit_btn, result_header, success_msg_part",
    test_cases,
    ids=[case[0] for case in test_cases]  # Use test_id for clean pytest output
)
def test_full_user_journey(
    app_server, driver,
    test_id, lang_btn, accept_btn, lottery_btn, num_clicks, submit_btn, result_header, success_msg_part
):
    """
    Tests the full user flow using parameterized inputs.
    """

    # Get the URL from the app_server fixture
    driver.get(app_server)

    # Set a 10-second wait time for elements to appear
    wait = WebDriverWait(driver, 10)

    try:
        # --- 1. Welcome Page ---
        # Find and click the language button
        lang_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button//*[text()='{lang_btn}']"))
        )
        lang_button.click()
        time.sleep(1)

        # --- 2. Disclaimer Page ---
        # We need to click the correct buttons based on the language (lang_btn)
        # For this example, I'll trigger the Agreement toggle
        # agreement_text = "User Agreement" if lang_btn == "English" else "Felhasználási Feltételek"
        #
        # ua_button = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{agreement_text}')]"))
        # )
        # ua_button.click()
        # time.sleep(2)
        #
        # ua_button = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{agreement_text}')]"))
        # )
        # ua_button.click()
        #
        # policy_text = "Data Policy" if lang_btn == "English" else "Adatkezelési Tájékoztató"
        #
        # dp_button = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{policy_text}')]"))
        # )
        # dp_button.click()
        # time.sleep(2)
        #
        # dp_button = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{policy_text}')]"))
        # )
        # dp_button.click()

        # --- Checkbox Handling ---
        checkbox_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="stCheckbox"]'))
        )

        # Click the label (visual element) to avoid 'ElementNotInteractable'
        checkbox_label = checkbox_container.find_element(By.TAG_NAME, "label")
        checkbox_input = checkbox_container.find_element(By.TAG_NAME, "input")

        if not checkbox_input.is_selected():
            checkbox_label.click()

        # Click Next/Tovább
        accept_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button//*[text()='{accept_btn}']"))
        )
        accept_button.click()

        # --- 3. Selector Page ---
        # Wait for the lottery button to appear and click it
        lottery_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button//*[text()='{lottery_btn}']"))
        )
        lottery_button.click()

        # --- 4. Number Picker Page ---
        # Wait for the number grid to be visible
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button//*[text()='1']"))
        )

        # Click on the required number of numbers
        for i in [1,10,11,12,13,14,15,16]:
            driver.find_element(By.XPATH, f"//button//*[text()='{i}']").click()
            time.sleep(0.2)  # Small pause to register the click

        # Find and click the 'Submit' button
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button//*[text()='{submit_btn}']"))
        )
        submit_button.click()

        # --- 5. Results Page ---
        # Wait for the results header to appear
        results_header_el = wait.until(
            EC.visibility_of_element_located((By.XPATH, f"//h2[contains(., '{result_header}')]"))
        )

        # Assert that the header is displayed
        assert results_header_el.is_displayed()

        # Check for the success message
        success_message = wait.until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{success_msg_part}')]"))
        )
        assert success_message.is_displayed()

    except Exception as e:
        raise e

