from flask import Flask, request, render_template_string, session
from flask_session import Session  # Flask-Session for server-side session management

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# HTML template with CSS styling
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Calculator</title>
  <style>
    body { text-align: center; }
    .calculator { 
      display: inline-block;
      margin-top: 50px;
      background: #f0f0f0;
      border-radius: 10px;
      padding: 10px;
    }
    .calculator-screen {
      width: 300px;
      margin-bottom: 10px;
      background-color: #e6e6e6;
      text-align: right;
      padding: 10px;
      border: none;
      border-radius: 5px;
      font-size: 24px;
    }
    .calculator-keys button {
      height: 60px;
      width: 60px;
      margin: 5px;
      font-size: 24px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    .calculator-keys {
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="calculator">
    <input type="text" class="calculator-screen" value="{{ result }}" disabled>
    <div class="calculator-keys">
      <form method="post">
        <button type="submit" name="number" value="7">7</button>
        <button type="submit" name="number" value="8">8</button>
        <button type="submit" name="number" value="9">9</button>
        <button type="submit" name="operation" value="divide">/</button>
        <br>
        <button type="submit" name="number" value="4">4</button>
        <button type="submit" name="number" value="5">5</button>
        <button type="submit" name="number" value="6">6</button>
        <button type="submit" name="operation" value="multiply">*</button>
        <br>
        <button type="submit" name="number" value="1">1</button>
        <button type="submit" name="number" value="2">2</button>
        <button type="submit" name="number" value="3">3</button>
        <button type="submit" name="operation" value="subtract">-</button>
        <br>
        <button type="submit" name="number" value="0">0</button>
        <button type="submit" name="decimal" value=".">.</button>
        <button type="submit" name="clear" value="clear">C</button>
        <button type="submit" name="operation" value="add">+</button>
        <br>
        <button type="submit" name="equals" value="equals" style="width: 250px;">=</button>
      </form>
    </div>
  </div>
</body>
</html>
"""


oper = {'add': '+', 'subtract': '-', 'multiply': '*', 'divide': '/'}


@app.route('/', methods=['GET', 'POST'])
def calculator():
    if 'current' not in session:
        session['result'] = 0
        session['operation'] = ''
        session['current'] = ''

    if request.method == 'POST':
        if 'number' in request.form:
            session['current'] += request.form['number']
        elif 'operation' in request.form and request.form['operation'] in oper:
            # Добавить символ операции в current
            session['current'] += oper[request.form['operation']]
            session['operation'] = request.form['operation']
        elif 'equals' in request.form:
            # Проверить наличие операции в current
            if session['operation']:
                try:
                    # Разделить current на числа и оператор
                    parts = session['current'].split(oper[session['operation']])
                    if len(parts) == 2:
                        session['result'] = perform_operation(session['operation'], *parts)
                        session['current'] = str(session['result'])
                    else:
                        session['current'] = 'Error'
                except Exception as e:
                    session['current'] = 'Error'
                session['operation'] = ''


        elif 'decimal' in request.form:
            # Проверяем, есть ли операция в текущем вводе
            if any(op in session['current'] for op in oper.values()):
                # Получаем часть после операции
                after_operation = session['current'].split(oper[session['operation']])[-1]
                if '.' not in after_operation:
                    session['current'] += '.'
            else:
                # Добавляем точку, если это первое число
                if '.' not in session['current']:
                    session['current'] += '.'

        elif 'clear' in request.form:
            session['result'] = 0
            session['operation'] = ''
            session['current'] = ''

    return render_template_string(HTML_TEMPLATE, result=session['current'])


def perform_operation(operation, num1, num2):
    if operation == 'add':
        return float(num1) + float(num2)
    elif operation == 'subtract':
        return float(num1) - float(num2)
    elif operation == 'multiply':
        return float(num1) * float(num2)
    elif operation == 'divide':
        if float(num2) == 0.0:
            return 'Error: Division by zero'
        return float(num1) / float(num2)
    return 0

if __name__ == '__main__':
    app.run(debug=True)
    