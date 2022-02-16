
import io
import matplotlib.pyplot as plt

from flask import Flask, render_template
from sqlalchemy.sql import func

from models import Program, Saving, Customer, TeamMember
from utils import create_db_session

app = Flask(__name__)

db = create_db_session()

@app.route('/')
def hello_world():
    return shane_c_demo()

@app.route('/savings.png')
def savings_png():
    pass

def shane_c_demo():
    total_people_helped = db.query(Customer.sf_id).count()
    money_saved         = db.query(func.sum(Saving.money_savings)).scalar()
    energy_saved        = db.query(func.sum(Saving.energy_savings)).scalar()
    #print(type(total_people_helped[0]))
    """return render_template(
        'service_metrics.html',
        name='Cool Business Dashboard',
        total_people_helped=total_people_helped,
        money_saved=money_saved,
        energy_saved=energy_saved,
        url='/static/images/combined_savings.png',
        url2='/static/images/energy_savings.png'
    )"""
    return render_template('service_metrics2.html')

if __name__ == '__main__':
    app.run()
