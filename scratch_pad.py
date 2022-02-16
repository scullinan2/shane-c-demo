
import matplotlib.pyplot as plt

from datetime import datetime
from os import environ, path

from models import Saving
from utils import create_db_session



if __name__ == '__main__':
    db = create_db_session()
    image_dir = path.join(environ['HOME_DIR'], 'static/images/')
    savings = db.query(Saving).all()
    divisions = list(set([s.stamp.year for s in savings]))
    money_savings  = {year: 0 for year in divisions}
    energy_savings = {year: 0 for year in divisions}
    for saving in savings:
        money_savings[saving.stamp.year]  += saving.money_savings
        energy_savings[saving.stamp.year] += saving.energy_savings
    plt.bar(money_savings.keys(), list(money_savings.values()), label='money')
    plt.bar(money_savings.keys(), list(energy_savings.values()), bottom=list(money_savings.values()), label='energy')
    plt.legend()
    #plt.show()
    plt.savefig(path.join(image_dir, 'combined_savings.png'))
