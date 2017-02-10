from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = "ThisIsSecret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def validate():
    if len(request.form['names']) < 1:
        flash("You shall not pass! (Mostly because name is empty)")
        return redirect('/')
    else:
            session['name'] = request.form['names']
            session['location'] = request.form['location']
            session['lang'] = request.form['lang']
            session['comment'] = request.form['comment']
            return redirect('/users')

@app.route('/users')
def showUser():
    flash("{}".format(session['name']))
    return render_template('results.html', name=session['name'], email=session['email'])
app.run(debug=True)
