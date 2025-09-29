You are an expert Python/Django Software Engineer. Your task is to act as an **Autonomous Code Agent** to scaffold the initial version of a web application based on the requirements below.

**GOAL:** Create a **Personal Finance Tracker and Budgeting Application** (CRUD system) using the Django framework. The application must allow users to track their income, expenses, and manage budgets against different categories.

**CONTEXT:** This project is the final assignment for a Software Engineering course focused on applying AI in software development, requiring strict adherence to modern development practices, including access control, testing, and CI/CD readiness.

**TECHNICAL AND FUNCTIONAL REQUIREMENTS:**

### 1. Project Setup and Structure
* **Framework:** **Django 5.x** (or the latest stable version).
* **Database:** Use **SQLite** for simplicity in the initial scaffold, with configuration ready for PostgreSQL/MySQL (e.g., using environment variables for settings).
* **Project Name:** `FinanceTracker` or similar.
* **App Structure:** Create a main Django app named `transactions` or `finance`.

### 2. User Authentication and Access Control (Mandatory)
* Implement Django's built-in **User Authentication** system.
* The application must include basic **Login, Logout, and Registration** views/templates.
* All financial data (transactions, categories) must be **strictly linked to the logged-in user** (using `ForeignKey` to `User`).
* Unauthorized users attempting to access financial views (e.g., `/transactions/`) must be redirected to the login page (use `@login_required`).

### 3. Data Management (CRUD - Mandatory)
* Define the following **Django Models**:
    * **Category:** Name (e.g., 'Groceries', 'Rent', 'Salary'). Must be user-specific.
    * **Transaction:**
        * User (`ForeignKey`)
        * Type (`CharField`, choices: 'Income' or 'Expense')
        * Amount (`DecimalField`)
        * Date (`DateField`)
        * Category (`ForeignKey` to Category)
        * Description (`CharField`)
    * **Budget:**
        * User (`ForeignKey`)
        * Category (`ForeignKey`)
        * Limit (`DecimalField`)
        * Period (e.g., 'Monthly')
* Implement **Class-Based Views (CBVs)** for the full CRUD cycle for **Transactions**:
    * `TransactionListView`
    * `TransactionCreateView`
    * `TransactionUpdateView`
    * `TransactionDeleteView`

### 4. Core Business Logic (Mandatory)
* **Dashboard View:** Create a main view that calculates and displays the following for the current month for the logged-in user:
    * **Current Balance/Net Worth** (Income - Expenses).
    * **Total Income** for the month.
    * **Total Expenses** for the month.
* **Budget Tracking:** Implement a function/method to check the user's spending against a defined budget limit for a specific category and display the percentage used on the dashboard.

### 5. Testing (Mandatory)
* Provide at least **one unit test** using Django's `TestCase` (or `pytest-django`).
* The test must verify the **Core Business Logic** from section 4: e.g., "Verify that the calculated monthly balance is correct after adding one income and one expense transaction."

### 6. Deployment Readiness (CI/CD Scaffold - Mandatory)
* Provide a basic **`Dockerfile`** for containerizing the application.
* Provide a basic **`requirements.txt`** file listing all necessary Python dependencies (Django, etc.).
* (Optional but recommended) Include a brief outline of how a **GitHub Actions** workflow would be structured to: 1) Build the Docker image, and 2) Run the tests.

---

**AGENT OUTPUT STEPS:**

1.  **Generate `requirements.txt`**.
2.  **Generate `Dockerfile`**.
3.  **Generate the main `settings.py`** (with basic DB config).
4.  **Generate the `models.py`** file with the required `Category`, `Transaction`, and `Budget` models.
5.  **Generate the `views.py`** file with the required CBVs (CRUD for Transaction) and the **Dashboard View** (implementing the business logic).
6.  **Generate the `urls.py`** file for the app.
7.  **Generate the `tests.py`** file with the mandatory test case.
8.  **Provide a simple `base.html`** and a basic **`dashboard.html`** template to show the logic in action.