from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from models import db, Expense, Income
from datetime import datetime
from sqlalchemy import func
import io
import pandas as pd

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/dashboard')
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total_expenses = sum(exp.amount for exp in expenses)
    categories = [[row[0], float(row[1])] for row in db.session.query(Expense.category, func.sum(Expense.amount)).filter_by(user_id=current_user.id).group_by(Expense.category).all()]
    monthly = [[row[0], float(row[1])] for row in db.session.query(func.strftime('%Y-%m', Expense.date), func.sum(Expense.amount)).filter_by(user_id=current_user.id).group_by(func.strftime('%Y-%m', Expense.date)).all()]
    
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    total_income = sum(inc.amount for inc in incomes)
    income_categories = [[row[0], float(row[1])] for row in db.session.query(Income.source, func.sum(Income.amount)).filter_by(user_id=current_user.id).group_by(Income.source).all()]
    monthly_income = [[row[0], float(row[1])] for row in db.session.query(func.strftime('%Y-%m', Income.date), func.sum(Income.amount)).filter_by(user_id=current_user.id).group_by(func.strftime('%Y-%m', Income.date)).all()]
    
    net_savings = total_income - total_expenses
    
    return render_template('dashboard.html', total=total_expenses, categories=categories, monthly=monthly,
                           total_income=total_income, income_categories=income_categories, monthly_income=monthly_income,
                           net_savings=net_savings)

@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        notes = request.form.get('notes', '')
        expense = Expense(user_id=current_user.id, category=category, amount=amount, date=date, notes=notes)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully.')
        return redirect(url_for('expenses.view_expenses'))
    return render_template('add_expense.html')

@expenses_bp.route('/view')
@login_required
def view_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    return render_template('view_expenses.html', expenses=expenses)

@expenses_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('expenses.view_expenses'))
    if request.method == 'POST':
        expense.category = request.form['category']
        expense.amount = float(request.form['amount'])
        expense.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        expense.notes = request.form.get('notes', '')
        db.session.commit()
        flash('Expense updated successfully.')
        return redirect(url_for('expenses.view_expenses'))
    return render_template('edit_expense.html', expense=expense)

@expenses_bp.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('expenses.view_expenses'))
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully.')
    return redirect(url_for('expenses.view_expenses'))

@expenses_bp.route('/export/<string:file_format>')
@login_required
def export_expenses(file_format):
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    data = [{
        'Category': e.category,
        'Amount': e.amount,
        'Date': e.date.strftime('%Y-%m-%d'),
        'Notes': e.notes
    } for e in expenses]
    df = pd.DataFrame(data)
    if file_format == 'csv':
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='expenses.csv')
    elif file_format == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Expenses')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='expenses.xlsx')
    else:
        flash('Invalid export format.')
        return redirect(url_for('expenses.view_expenses'))

@expenses_bp.route('/import', methods=['POST'])
@login_required
def import_expenses():
    file = request.files.get('file')
    if not file:
        flash('No file selected.')
        return redirect(url_for('expenses.view_expenses'))
    filename = file.filename.lower()
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file)
        else:
            flash('Unsupported file format. Please upload CSV or Excel file.')
            return redirect(url_for('expenses.view_expenses'))
        required_columns = {'Category', 'Amount', 'Date'}
        if not required_columns.issubset(df.columns):
            flash(f'Missing required columns: {required_columns}')
            return redirect(url_for('expenses.view_expenses'))
        for _, row in df.iterrows():
            category = str(row['Category'])
            amount = float(row['Amount'])
            date = pd.to_datetime(row['Date']).date()
            notes = str(row['Notes']) if 'Notes' in df.columns else ''
            expense = Expense(user_id=current_user.id, category=category, amount=amount, date=date, notes=notes)
            db.session.add(expense)
        db.session.commit()
        flash('Expenses imported successfully.')
    except Exception as e:
        flash(f'Error importing file: {e}')
    return redirect(url_for('expenses.view_expenses'))

# Income routes

@expenses_bp.route('/income/add', methods=['GET', 'POST'])
@login_required
def add_income():
    if request.method == 'POST':
        source = request.form['source']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        notes = request.form.get('notes', '')
        income = Income(user_id=current_user.id, source=source, amount=amount, date=date, notes=notes)
        db.session.add(income)
        db.session.commit()
        flash('Income added successfully.')
        return redirect(url_for('expenses.view_income'))
    return render_template('add_income.html')

@expenses_bp.route('/income/view')
@login_required
def view_income():
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).all()
    return render_template('view_income.html', incomes=incomes)

@expenses_bp.route('/income/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_income(id):
    income = Income.query.get_or_404(id)
    if income.user_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('expenses.view_income'))
    if request.method == 'POST':
        income.source = request.form['source']
        income.amount = float(request.form['amount'])
        income.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        income.notes = request.form.get('notes', '')
        db.session.commit()
        flash('Income updated successfully.')
        return redirect(url_for('expenses.view_income'))
    return render_template('edit_income.html', income=income)
