# 🎯 Would I have won? App

### This Streamlit-based application allows users to check how many times a given set of "lucky numbers" would have resulted in a winning match (based on a user-defined match count) in Hungarian lotteries since the game began. It connects to a PostgreSQL database to query public historical draw data. The project is for entertainment and educational purposes only.

### 🤝 This project is a Capstone project for [NCLab Advanced Python Developer Training Program](https://nclab.com/pg-py/). I would like to thank the NCLab team for their guidance and assistance during the program. You are all awesome!

## 🤖 User Guide

![userguide.gif](userguide.gif)

1) Choose your language.
2) Accept the user agreement and data policy.
3) Select the lottery or check rules and guide.
4) Choose the match count.
5) Choose your lucky numbers.
6) Press the Submit button.
7) Enjoy the results.

If there are no listed results and the app displays
*"You would have won in 0 draws out of 0 draws since the start of the lottery!"*,
then an error occurred during data retrieval. Please refresh the application.
If this doesn’t solve the issue, contact the developer at:
📧 **katona.mihaly@outlook.hu**

If the number of draws is not zero but the list is empty, it means your selected numbers have never matched in any draw up to the current database update.

Some winning lucky numbers are the following, to check how the app should work. These will yield a non-empty list.
- Ötöslottó: 1, 2, 3, 4, 5 / match count: 1
- Hatoslottó: 1, 2, 3, 4, 5, 6 / match count: 1
- Heteslottó: 1, 2, 3, 4, 5, 6, 7 / match count: 1

## 🔔 Lottery rules

## 5️⃣ Ötöslottó (5/90 Lottery)

In the Ötöslottó game, you must choose **5 numbers out of 90**.
The goal is to match as many as possible of the **5 winning numbers** drawn each week.
Possible numbers of matches: **1, 2, 3, 4, or 5**.

### Winning Odds

| Matches | Odds |
|----------|-------|
| 5 matches | 1 : 43 949 268 |
| 4 matches | 1 : 103 410 |
| 3 matches | 1 : 1 231 |
| 2 matches | 1 : 44 |

> That means your chance of winning *any* prize in the Ötöslottó game is **1 : 43**.

This description is an excerpt from the detailed rules available on the [Ötöslottó](https://bet.szerencsejatek.hu/jatekok/otoslotto/leiras) website.

---

## 6️⃣ Hatoslottó (6/45 Lottery)

In the Hatoslottó game, you must choose **6 numbers out of 45**.
The goal is to match as many as possible of the **6 winning numbers** drawn.
Possible numbers of matches: **1, 2, 3, 4, 5, or 6**.

### Winning Odds

| Matches | Odds |
|----------|-------|
| 6 matches | 1 : 8 145 060 |
| 5 matches | 1 : 34 808 |
| 4 matches | 1 : 733 |
| 3 matches | 1 : 45 |

> That means your chance of winning *any* prize in the Hatoslottó game is **1 : 42**.

This description is an excerpt from the detailed rules available on the [Hatoslottó](https://bet.szerencsejatek.hu/jatekok/hatoslotto/leiras) website.

---

## 7️⃣ Skandináv Lottó (7/35 Lottery)

In the Skandináv Lottó game, you must choose **7 numbers out of 35**.
Each week there are **two draws** – one manual and one mechanical – both drawing 7 numbers.
Possible numbers of matches: **1, 2, 3, 4, 5, 6, or 7**.

### Winning Odds

| Matches | Odds |
|----------|-------|
| 7 matches | 1 : 3 362 260 |
| 6 matches | 1 : 17 155 |
| 5 matches | 1 : 424 |
| 4 matches | 1 : 30 |

> That means your chance of winning *any* prize in the Skandináv Lottó game is **1 : 28**.

This description is an excerpt from the detailed rules available on the [Skandináv Lottó](https://bet.szerencsejatek.hu/jatekok/skandinavlotto/leiras) website.

## 👀 Behind the scenes

The app works as follows coded in [streamlit_app.py](streamlit_app.py). When a user selects the language then a _language state variable_ is registered.
The app checks the _state variables list_ after every interaction. If the _language state variable_ is in the  _state variables list_
then the User Agreement and Data Policy page pops up. The app continues only if the User Agreement and Data Policy is accepted, thus
the _diclaimer state variable = True_ appears in the _state variables list_. If it is there, then the lottery picker page appears.
There you can select the lottery, but if you are not sure, you can get help by pressing "Rules and guide" button.
When the lottery is selected the _lottery_id state variable_ is set connected to the lottery and a grid of numbers appears.
From the grid, you can select your lucky numbers. From another grid you can select for how many matches you want to filter for.
It all depends on the  _lottery_id state variable_. If you press the "Submit" button then [backend.py](backend.py) is called which handles the 
SQL query. An SQL query is sent to the database which check if any item matches the lucky numbers and provides a list containing those draws.
The [backend.py](backend.py) then formats the list and send it back to [streamlit_app.py](streamlit_app.py), while the 
_results state variable_ appears in the _state variables list_. If it is there the results are listed in the app. Enjoy the results!

Anytime you can use the "Back" button to go one page back.

## 📁 Project Structure

The project is structured into frontend, backend logic, configuration, and testing files:

```
.
├── .streamlit/
│   └── secrets.toml          # Database connection configuration
├── backend.py                # Core application logic and database querying
├── streamlit_app.py          # Streamlit frontend UI and session state management
├── requirements.txt          # Python dependencies
├── queries.py                # SQL queries
├── test_backend.py           # Unit tests for the backend logic
└── test_app.py               # End-to-end (E2E) tests using Selenium
```

## 📋 File Descriptions

| File Name        | Purpose                                                                                                                                                                                                                                                                    |
|:-----------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| streamlit_app.py | Frontend (UI & Routing). Contains the StreamlitFrontend class, which manages the application's multilingual text, dynamic number pickers, session state navigation (Welcome, Disclaimer, Selector, Picker, Results), and displays the final data fetched from the backend. |
| backend.py       | Backend (Logic & Data). Contains the WinningNumbers class. It handles all critical logic, including input validation (lottery ID, number count, number range), SQL query construction for the lotteries, and executing database operations via st.connection.              |
| requirements.txt | Dependencies. Lists all necessary Python packages, including streamlit, psycopg2-binary (PostgreSQL adapter), and sqlalchemy.                                                                                                                                              |
| queries.py       | SQL queries. Contains all the necessary SQL queries, for cleaner backend.                                                                                                                                                                                                  |
| test_backed.py   | Unit Tests. Uses unittest and unittest.mock to verify the validation methods (_check_validity_lottery, _check_validity_numbers, _check_validity_match_count) and data interaction logic (check_lottery_numbers and _run_db_queries).                                       |
| test_app.py      | E2E Tests. Uses pytest and selenium with Edge WebDriver to simulate a full user journey through the Streamlit app, checking that pages load and buttons correctly transition between states across both English and Hungarian languages.                                   |

## ⚙️ Local Setup of 🎯 Would I have won? App

### 1. Prerequisites

Must have:

- Python 3.8+ installed.
- A self-hosted PostgreSQL database containing the public lottery draw data.
- Microsoft Edge WebDriver executable (msedgedriver.exe) installed locally, as test_app.py is configured to use it.
  - Download from https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads
  - Add to the root directory of the app.

### 2. Installation

- Clone the Repository (or download the files).
- Create a virtual environment and activate it (recommended).
- Install dependencies: ```pip install -r requirements.txt```

### 3. Database Configuration (.streamlit/secrets.toml)

Streamlit securely handles database credentials using the .streamlit/secrets.toml file. You must create this folder and file in your project root directory and populate it with your PostgreSQL connection details.

- Create the folder: ```mkdir .streamlit```
- Create the file:
    ```
    Set-Content -Path .streamlit/secrets.toml -Value '# Never upload to anywhere!
    # Required connection parameters for st.connection("postgresql", type="sql")
    # Replace the placeholders below with your PostgreSQL server details.
    [connections.postgresql]
    dialect = "postgresql"
    host = "localhost"
    port = "5432"
    database = "your_DB"
    username = "your_USERNAME"
    password = "your_password"
    '
    ```
- Add to .gitignore: ```/.streamlit/secrets.toml```


### 4. Running the Application

Execute the streamlit_app.py file from your terminal: ```streamlit run streamlit_app.py```

This will launch the app in your default web browser (usually at http://localhost:8501).

### 5. Running Tests

To run the full suite of unit and end-to-end tests:

- Ensure you have the required testing dependencies installed (included in requirements.txt).
- Ensure the Edge WebDriver is accessible to test_app.py.

Execute the tests:
- unit test: ```python -m unittest test_backend.py```
- end-to-end test: ```pytest test_app.py```

# ☁️ Host on Streamlit Community Cloud and Supabase

- Fork the repository: https://github.com/KatonaMihaly/did-i-win-the-lottery.git
- Go to Streamlit Community Cloud: https://share.streamlit.io/
- Choose "Deploy a public app from Github" and follow the process
- Click "Advanced settings" and paste the content of your secrets.toml to secrets.

If you host your database on Supabase, then change your secrets to:

[connections.supa_db]

url = "postgresql://postgres.[your Supabase project ID]:[your DB password]@[your pooler ID].pooler.supabase.com:6543/postgres"

[connections.supabase]

SUPABASE_URL = "https://[your Supabase project ID].supabase.co"

SUPABASE_KEY = "[your anon key from Supabase]"

# ⬇️ Download public Hungarian lottery data
- Go to https://www.szerencsejatek.hu/
- Find the lottery Ötöslottó, Hatoslottó or Skandináv lottó
- Click "Korábbi sorsolások"
- Download in XLS

# 🔄 Update lottery data manually
- Change the downloaded XLS to match the following structure:

| date | lottery_id | n1 | n2 | ... | nm |
|:--------|:--------|:--------|:--------|:--------|:--------|

where the lottery_id is:
- hu5 for Ötöslottó
- hu6 for Hatoslottó
- hu7 for Skandináv lottó

where the m is the range for each lottery:
- 5 for hu5
- 6 for hu6
- 7 for hu7


- Save the restructured XLS to .csv named:
  -  [draw_numbers_hu5.csv](data_refining/Hu5/draw_numbers_hu5.csv) for Ötöslottó
  - [draw_numbers_hu6.csv](data_refining/Hu6/draw_numbers_hu6.csv) for Hatoslottó
  - [draw_numbers_hu7a.csv](data_refining/Hu7/draw_numbers_hu7a.csv) for Skandináv lottó mechanical draw
  - [draw_numbers_hu7b.csv](data_refining/Hu7/draw_numbers_hu7b.csv) for Skandináv lottó manual draw


- Paste it into the related folder in **data_refining** folder.
- Run the related *draw_numbers_hu*_refine.py* file. It creates an SQL compatible txt in **SQL_commands** folder.
- Update [lottery.sql](data_refining/SQL_commands/lottery.sql) and paste it into your database hosts SQL query.

# 📜 License
MIT License

Copyright (c) 2025 Mihály Katona

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


