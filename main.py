from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message
import requests
from datetime import date


app = Flask(__name__)
app.secret_key = "c224rf"
portfolio_url = "https://api.npoint.io/f2a8320c085e54c0bc83"
year = date.today().strftime("%Y")

app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'classiccream@yahoo.com'
app.config['MAIL_PASSWORD'] = 'prvvnlftpzsckshu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


class MyForm(FlaskForm):
    email = StringField(label='Your Email', validators=[Email(), DataRequired()], render_kw={"class": 'form-control form-style', "placeholder": "Name"})
    name = StringField(label='Your Name', validators=[DataRequired()], render_kw={"class": 'form-control form-style', "placeholder": "Your Name"})
    subject = StringField(label='Subject', validators=[DataRequired()], render_kw={"class": 'form-control form-style', "placeholder": "Subject"})
    body = TextAreaField(label='Your Message', render_kw={"class": 'form-control form-style', "placeholder": "Type your message here", "s": "50"})
    submit = SubmitField(label='Send', render_kw={"class": 'btn btn-secondary'})


response = requests.get(portfolio_url)
portfolios = response.json()
total = len(portfolios) - 1


@app.route('/', methods=["GET", "POST"])
def index():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        print(f"Name is {name}")
        print(f"Email is {form.email.data}")
        print(f"The message is {form.body.data}")
        msg = Message(form.subject.data, sender='classiccream@yahoo.com', recipients=['classiccream@yahoo.com'])
        msg.body = f"Name: {form.name.data}\n Email: {form.email.data}\n content: {form.body.data}"
        mail.send(msg)
        print("Message sent")
        return redirect(url_for('index'))
    return render_template('index.html', portfolios=portfolios, total=total, form=form, year=year)


@app.route('/portfolio/<int:num>')
def get_portfolio(num):
    for portfolio in portfolios:
        if portfolio['id'] == num:
            requested_portfolio = portfolio
    return render_template('portfolio.html', p_folio=requested_portfolio)


if __name__ == '__main__':
    app.run(debug=True)