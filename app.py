import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Создаем таблицу с полями для имени и телефона
    cursor.execute('''CREATE TABLE IF NOT EXISTS leads 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, 
                       phone TEXT, 
                       form_type TEXT, 
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order_project():
    # Забираем данные из полей формы
    name = request.form.get('name')
    phone = request.form.get('phone')
    form_type = request.form.get('form_type')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO leads (name, phone, form_type) VALUES (?, ?, ?)', (name, phone, form_type))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/admin')
def admin_panel():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    
    # Чуть более читаемая админка
    html = '''
    <body style="background: #111; color: #fff; font-family: sans-serif; padding: 40px;">
        <h1>Список заявок из БД</h1>
        <table border="1" cellpadding="10" style="border-collapse: collapse; border-color: #333; width: 100%;">
            <tr style="background: #222; color: #e57c35;">
                <th>ID</th><th>Имя</th><th>Телефон</th><th>Откуда форма</th><th>Дата</th>
            </tr>
    '''
    for row in rows:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>'
    html += '</table><br><a href="/" style="color: #e57c35;">Вернуться на сайт</a></body>'
    return html

if __name__ == '__main__':
    init_db()
    app.run(debug=True)