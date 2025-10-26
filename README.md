# expense_management
# Xarajatlar Hisoblagichi

**Bitta `app.py` faylida** to‘liq Flask ilova:  
xarajatlarni qo‘shish, ko‘rish, o‘chirish, filtr va umumiy summa.

## Nima uchun?
- 1 ta fayl — o‘rnatish oson  
- O‘rganish uchun ideal  
- `templates` ham ichida

## Qanday ishlatish?

```
pip install flask flask-sqlalchemy
python app.py
```

Brauzer: http://127.0.0.1:5000
Imkoniyatlar

/ – bosh sahifa
/expenses – ro‘yxat
/expenses/add – qo‘shish
/expenses/total – jami
/expenses/category/transport – filtr
/expenses/month/6 – 6-oy


expenses.db avto yaratiladi.
Kod: app.py 
