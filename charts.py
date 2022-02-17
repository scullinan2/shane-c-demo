
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from matplotlib import rc
from os import environ, path

from models import Saving, TeamMember
from utils import create_db_session

def create_money_savings_by_program_by_yr(db, overwrite=False):
    image_dir = path.join(environ['HOME_DIR'], 'static/images/')
    savings = db.query(Saving).all()
    plt.clf()
    # Break out savings by program
    divisions = list(set([s.stamp.year for s in savings]))
    for program in list(set([s.program for s in savings])):
        ttl_program_savings = [s for s in savings if s.program == program]
        savings_by_yr = {year: 0 for year in divisions}
        for saving in ttl_program_savings:
            savings_by_yr[saving.stamp.year] += saving.money_savings
        plt.plot(divisions, list(savings_by_yr.values()), label=ttl_program_savings[0].elevate_program.name)
    plt.legend()
    plt.title('$ Savings Program By Years')
    plt.savefig(path.join(image_dir, 'money_savings_program_yr.png'))

def energy_savings_by_program_by_yr(db, overwrite=False):
    image_dir = path.join(environ['HOME_DIR'], 'static/images/')
    savings = db.query(Saving).all()
    plt.clf()
    # Break out savings by program
    divisions = list(set([s.stamp.year for s in savings]))
    for program in list(set([s.program for s in savings])):
        ttl_program_savings = [s for s in savings if s.program == program]
        savings_by_yr = {year: 0 for year in divisions}
        for saving in ttl_program_savings:
            savings_by_yr[saving.stamp.year] += saving.energy_savings
        plt.plot(divisions, list(savings_by_yr.values()), label=ttl_program_savings[0].elevate_program.name)
    plt.legend()
    plt.title('Energy Savings by Program by Year')
    plt.savefig(path.join(image_dir, 'energy_savings_program_yr.png'))

def create_savings_by_metric_by_yr(db, overwrite=False):
    image_dir = path.join(environ['HOME_DIR'], 'static/images/')
    savings = db.query(Saving).all()
    plt.clf()
    divisions = list(set([s.stamp.year for s in savings]))
    money_savings  = {year: 0 for year in divisions}
    energy_savings = {year: 0 for year in divisions}
    for saving in savings:
        money_savings[saving.stamp.year]  += saving.money_savings
        energy_savings[saving.stamp.year] += saving.energy_savings
    n = len(divisions)
    ind = np.arange(n)
    plt.ylim(0, max(list(money_savings.values())) + 500)
    plt.bar(ind, list(money_savings.values()), 0.3, label='money', color='#396377')
    plt.bar(ind + 0.3, list(energy_savings.values()), 0.3, label='energy', color='#ffc107')
    plt.ylabel('Year')
    plt.title('Total Savings by Metric by Year')
    plt.xticks(ind + 0.3 / 2, (divisions))
    plt.legend()
    plt.savefig(path.join(image_dir, 'savings_by_metric_by_yr.png'))

def create_np_savings_money_by_yr(db):
    image_dir = path.join(environ['HOME_DIR'], 'static/images/')
    savings = db.query(Saving).all()
    team_members = db.query(TeamMember).all()
    plt.clf()
    divisions = list(set([s.stamp.year for s in savings]))
    # Each program bills at different rates
    programs = list(set([t.elevate_program.name for t in team_members]))
    program_billables = {p: 0 for p in programs}
    #saving_counts  = {year: 0 for year in divisions}
    for program in programs:
        savings_cost = sum([t.billable_rate for t in team_members if t.elevate_program.name == program])
        program_billables[program] = savings_cost
    for program in programs:
        ttl_program_savings = [s for s in savings if s.elevate_program.name == program]
        saving_counts  = {year: 0 for year in divisions}
        for saving in ttl_program_savings:
            saving_counts[saving.stamp.year] += program_billables[saving.elevate_program.name] - 3
        plt.plot(divisions, list(saving_counts.values()), label=ttl_program_savings[0].elevate_program.name)
    plt.legend()
    plt.title('NP Money Savings by Program by Year')
    plt.savefig(path.join(image_dir, 'np_money_savings_program_yr.png'))

def create_np_savings_energy_by_yr(db, smart_grid_hrs=0.75, other_hrs=1, shane_hrs=0.5):
    image_dir = path.join(environ['HOME_DIR'], 'static/images/')
    savings = db.query(Saving).all()
    team_members = db.query(TeamMember).all()
    plt.clf()
    divisions = list(set([s.stamp.year for s in savings]))
    # Each program bills at different rates
    programs = list(set([t.elevate_program.name for t in team_members]))
    program_billables = {p: 0 for p in programs}
    #saving_counts  = {year: 0 for year in divisions}
    for program in programs:
        if 'Smart' in program:
            savings_cost = len([t for t in team_members if t.elevate_program.name == program]) * smart_grid_hrs
        else:
            savings_cost = len([t for t in team_members if t.elevate_program.name == program]) * other_hrs
        program_billables[program] = savings_cost
    for program in programs:
        ttl_program_savings = [s for s in savings if s.elevate_program.name == program]
        saving_counts  = {year: 0 for year in divisions}
        for saving in ttl_program_savings:
            saving_counts[saving.stamp.year] += program_billables[saving.elevate_program.name] - shane_hrs
        plt.plot(divisions, list(saving_counts.values()), label=ttl_program_savings[0].elevate_program.name)
    plt.legend()
    plt.title('NP Energy Savings by Program by Year')
    plt.savefig(path.join(image_dir, 'np_energy_savings_program_yr.png'))


if __name__ == '__main__':
    db = create_db_session()
    create_money_savings_by_program_by_yr(db)
    energy_savings_by_program_by_yr(db)
    create_savings_by_metric_by_yr(db)
    create_np_savings_money_by_yr(db)
    create_np_savings_energy_by_yr(db)
    #create_combined_savings(db)
    #plt.bar(money_savings.keys(), list(money_savings.values()), label='money', color='#396377')
    #plt.bar(money_savings.keys(), list(energy_savings.values()), bottom=list(money_savings.values()), label='energy', color='#fd7e14')
    # ffc107 = yellow


