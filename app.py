from flask import Flask, request, redirect, make_response

app = Flask(__name__)

@app.route('/')
def index():
    username = request.cookies.get('user')
    if username:
        return f"Hello {username}! <a href='/logout'>Logout</a> | <a href='/transfer'>Transfer</a>"
    return "<a href='/login'>Login</a>"

@app.route('/login')
def login():
    resp = make_response(redirect('/'))
    resp.set_cookie('user', 'Komal')
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('user')
    return resp

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    username = request.cookies.get('user')
    if not username:
        return "Unauthorized", 401

    if request.method == 'POST':
        to = request.form['to']
        amount = request.form['amount']
        return f"{amount} transferred to {to} by {username}!"

    return '''
        <form method="POST">
            Send To: <input name="to"><br>
            Amount: <input name="amount"><br>
            <button type="submit">Transfer</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)