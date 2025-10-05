# Expense Tracker Web Application

## Features
- User registration, login, and logout
- Add, view, update, and delete expenses
- Dashboard with expense summary and charts (using Chart.js)
- Export expenses to CSV and Excel files
- Import multiple expenses from CSV or Excel files
- Responsive and clean UI with HTML, CSS, and Jinja2 templates
- SQLite3 database backend with Flask and SQLAlchemy

## Installation

1. Clone the repository or download the source code.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install flask flask_sqlalchemy flask_login werkzeug pandas openpyxl
   ```

## Running the Application

1. Run the Flask app:
   ```bash
   python app.py
   ```
2. Open your browser and go to `http://127.0.0.1:5000`.

## Usage

- Register a new user account.
- Login with your credentials.
- Add, edit, or delete expenses.
- View your expenses list.
- Use the dashboard to see summaries and charts.
- Export your expenses as CSV or Excel files.
- Import multiple expenses by uploading a CSV or Excel file.

## Project Structure

- `app.py`: Main Flask application setup and route registration.
- `models.py`: Database models for User and Expense.
- `routes/`: Contains route blueprints for authentication and expenses.
- `templates/`: HTML templates using Jinja2.
- `static/css/`: CSS stylesheets.
- `static/js/`: JavaScript files including Chart.js integration.

## Notes

- Ensure your CSV or Excel import files have columns: `Category`, `Amount`, `Date`, and optionally `Notes`.
- Date format should be `YYYY-MM-DD`.
- The app uses SQLite3 database stored as `expenses.db` in the project directory.

## License

This project is open source and free to use.
