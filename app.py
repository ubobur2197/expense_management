from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'devkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomi = db.Column(db.String(100), nullable=False)
    summa = db.Column(db.Float, nullable=False)
    kategoriya = db.Column(db.String(50), nullable=False)
    sana = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


KATEGORIYALAR = ["oziq-ovqat", "transport", "kommunal"]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/expenses')
def get_expenses():
    expenses = Expense.query.order_by(Expense.sana.desc()).all()
    return render_template('expenses.html', expenses=expenses)


@app.route('/expenses/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        nomi = request.form.get('nomi')
        summa = request.form.get('summa')
        kategoriya = request.form.get('kategoriya')

        if not all([nomi, summa, kategoriya]):
            flash('Barcha maydonlarni to\'ldiring!', 'error')
            return redirect(url_for('add_expense'))

        if kategoriya not in KATEGORIYALAR:
            flash('Noto\'g\'ri kategoriya!', 'error')
            return redirect(url_for('add_expense'))

        try:
            summa = float(summa)
            if summa <= 0:
                raise ValueError
        except:
            flash('Summa musbat raqam bo\'lishi kerak!', 'error')
            return redirect(url_for('add_expense'))

        new = Expense(nomi=nomi, summa=summa, kategoriya=kategoriya)
        db.session.add(new)
        db.session.commit()
        flash('Xarajat qo\'shildi!', 'success')
        return redirect(url_for('get_expenses'))

    return render_template('add.html', kategoriyalar=KATEGORIYALAR)


@app.route('/expenses/category/<kategoriya>')
def by_category(kategoriya):
    if kategoriya not in KATEGORIYALAR:
        flash('Bunday kategoriya yo\'q!', 'error')
        return redirect(url_for('home'))

    expenses = Expense.query.filter_by(kategoriya=kategoriya).order_by(Expense.sana.desc()).all()
    return render_template('category.html', expenses=expenses, kategoriya=kategoriya)


@app.route('/expenses/total')
def total():
    total = db.session.query(db.func.sum(Expense.summa)).scalar() or 0
    return render_template('total.html', total=round(total, 2))


@app.route('/expenses/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        flash('Xarajat topilmadi!', 'error')
    else:
        db.session.delete(expense)
        db.session.commit()
        flash('Xarajat o\'chirildi!', 'success')
    return redirect(url_for('get_expenses'))


@app.route('/expenses/month/<int:oy>')
def monthly(oy):
    if oy < 1 or oy > 12:
        flash('Oy 1-12 oralig\'ida bo\'lishi kerak!', 'error')
        return redirect(url_for('home'))

    expenses = Expense.query.filter(db.extract('month', Expense.sana) == oy).order_by(Expense.sana.desc()).all()
    return render_template('expenses.html', expenses=expenses, title=f"{oy}-oy xarajatlari")


if __name__ == '__main__':
    app.run(debug=True)

