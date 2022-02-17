
import io
import matplotlib.pyplot as plt

from flask import Flask, render_template, request
from sqlalchemy.sql import func

from models import Program, Saving, Customer, TeamMember
from reset import reset
from utils import create_db_session

app = Flask(__name__)

db = create_db_session()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return get_nonprofit_page()
    if request.method == 'POST':
        # Get the correct page based on whatever
        if request.form.get('metrics') == 'nonprofit':
            return get_nonprofit_page()
        else:
            return get_business_page()

@app.route('/reset/', methods=['POST'])
def call_reset():
    reset()
    return 'numbers and charts are reset. Please navigate home'

def get_metrics(m_type: str):
    metrics = dict()
    if m_type == 'nonprofit':
        metrics['total_people_helped'] = '{} team members'.format(db.query(TeamMember.id_).count())
        metrics['money_saved']         = '${:,.2f}'.format(float(db.query(func.sum(Saving.money_savings)).scalar()) * 2.1)
        metrics['energy_saved']        = '{:.2f}'.format(float(db.query(func.count(Saving.id_)).scalar()) * 0.25) + ' hours'
    else:
        metrics['total_people_helped'] = '{} customers'.format(db.query(Customer.sf_id).count())
        metrics['money_saved']         = '${:,.2f}'.format(float(db.query(func.sum(Saving.money_savings)).scalar()))
        metrics['energy_saved']        = '{:.2f}'.format(float(db.query(func.sum(Saving.energy_savings)).scalar())) + ' kwh'

    return metrics

def get_business_page():
    metrics = get_metrics('')
    return render_template(
        'dashboard.html',
        name='Cool Business Dashboard',
        total_people_helped=metrics['total_people_helped'],
        money_saved=metrics['money_saved'],
        energy_saved=metrics['energy_saved'],
        numbers='business numbers',
        chart='/static/images/savings_by_metric_by_yr.png',
        chart2='/static/images/energy_savings_program_yr.png',
        chart3='/static/images/money_savings_program_yr.png'
        #url='/static/images/combined_savings.png',
        #url2='/static/images/energy_savings.png'
    )

def get_nonprofit_page():
    metrics = get_metrics('nonprofit')
    return render_template(
        'dashboard.html',
        name='Cool Business Dashboard',
        total_people_helped=metrics['total_people_helped'],
        money_saved=metrics['money_saved'],
        energy_saved=metrics['energy_saved'],
        numbers='np numbers',
        chart='/static/images/np_energy_savings_program_yr.png',
        chart2='/static/images/np_money_savings_program_yr.png',
        chart3=None
    )


def shane_c_demo():

    return render_template(
        'dashboard.html',
        name='Cool Business Dashboard',
        total_people_helped=total_people_helped,
        money_saved=money_saved,
        energy_saved=energy_saved,
        url='/static/images/combined_savings.png',
        url2='/static/images/energy_savings.png'
    )
    return render_template('dashboard.html')

def shane_c_demo2():

    total_people_helped = 50000
    #money_saved         = '${:,.2f}'.format(float(db.query(func.sum(Saving.money_savings)).scalar()))
    money_saved = 50000
    energy_saved = 50000
    #energy_saved        = '{:.2f}'.format(float(db.query(func.sum(Saving.energy_savings)).scalar())) + ' kwh'
    #print(type(total_people_helped[0]))
    return render_template(
        'dashboard.html',
        name='Cool Business Dashboard',
        total_people_helped=total_people_helped,
        money_saved=money_saved,
        energy_saved=energy_saved,
        url='/static/images/combined_savings.png',
        url2='/static/images/energy_savings.png'
    )
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()
