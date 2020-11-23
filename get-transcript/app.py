from flask import Flask, render_template, request, url_for, redirect
import createemail

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def home():
	if request.method == 'POST':
		id = request.form['id']
		email_address = request.form['email']
		createemail.email(id, email_address)
		return redirect(url_for('report'))

	return render_template('index.html')

@app.route('/report', methods=('GET', 'POST'))
def report():
	return render_template('report.html')