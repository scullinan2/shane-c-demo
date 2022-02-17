
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from random import randint, choice, choices
from string import ascii_lowercase, ascii_uppercase, digits

from faker import Faker

from models import Program, Customer, TeamMember, Saving
from utils import create_db_session, check_records

fake = Faker()

db = create_db_session()

# Create and load each object type
def create_programs(db):
    programs = check_records(db, Program)
    if not programs:
        print('creating programs')
        programs = ['LeadCare', 'SmartGrid 1', 'SmartGrid 2', 'Multi-Family Energy Savings']
        for p in programs:
            program = Program()
            program.name = p
            db.add(program)

def create_team_members(db):
    team_members = check_records(db, TeamMember)
    if not team_members:
        print('creating team members')
        for i in range(8):
            team_member = TeamMember()
            team_member.name = fake.name()
            team_member.billable_rate = randint(1, 5)
            if i < 3:
                team_member.program = 4
            elif i < 5:
                team_member.program = 3
            elif i < 7:
                team_member.program = 2
            else:
                team_member.program = 1
            db.add(team_member)
            #print(team_member.__dict__)

def create_customers_savings(db):
    customers = check_records(db, Customer)
    if not customers:
        print('creating customers and savings')
        num_savings = 0
        for i in range(200):
            customer         = Customer()
            customer.sf_id   = '0030d00002Wf5' + ''.join(choices(ascii_uppercase + ascii_lowercase + digits, k=5))
            customer.name    = fake.name()
            customer.address = fake.address()
            if i < 50:
                # Create monthly savings on SmartGrid 1
                time_on_program = randint(1, 12)
                month_joined    = randint(1, 12)
                year_joined     = choice(['2016', '2017', '2018', '2019', '2020'])
                start_time          = datetime.strptime('{}-{}'.format(month_joined, year_joined), '%m-%Y')
                for i in range(time_on_program):
                    month_savings                = Saving()
                    month_savings.customer       = customer.sf_id
                    month_savings.program        = 2
                    month_savings.stamp          = start_time + relativedelta(months=i)
                    month_savings.money_savings  = randint( 1, 10)
                    month_savings.energy_savings = randint(-2, 10)
                    customer.savings.append(month_savings)
            elif i < 100:
                # Create monthly savings on SmartGrid 2
                time_on_program = randint(1, 9)
                month_joined    = randint(1, 12)
                year_joined     = choice(['2016', '2017', '2018', '2019', '2020'])
                start_time          = datetime.strptime('{}-{}'.format(month_joined, year_joined), '%m-%Y')
                for i in range(time_on_program):
                    month_savings                = Saving()
                    month_savings.customer       = customer.sf_id
                    month_savings.program        = 3
                    month_savings.stamp          = start_time + relativedelta(months=i)
                    month_savings.money_savings  = randint( 1, 10)
                    month_savings.energy_savings = randint(-2, 10)
                    customer.savings.append(month_savings)
            elif i < 150:
                month_joined           = randint(1, 12)
                year_joined            = choice(['2016', '2017', '2018', '2019', '2020'])
                savings_date           = datetime.strptime('{}-{}'.format(month_joined, year_joined), '%m-%Y')
                savings                = Saving()
                savings.customer       = customer.sf_id
                savings.program        = 1
                savings.stamp          = savings_date
                savings.money_savings  = randint(10, 40)
                savings.energy_savings = 0
                customer.savings.append(savings)
            else:
                month_joined           = randint(1, 12)
                year_joined            = choice(['2016', '2017', '2018', '2019', '2020'])
                years_on_program       = randint(1, 3)
                savings_date           = datetime.strptime('{}-{}'.format(month_joined, year_joined), '%m-%Y')
                for i in range(years_on_program):
                    year_savings                = Saving()
                    year_savings.customer       = customer.sf_id
                    year_savings.program        = 4
                    year_savings.stamp          = start_time + relativedelta(years=i)
                    year_savings.money_savings  = randint(10, 50)
                    year_savings.energy_savings = randint(10, 40)
                    customer.savings.append(year_savings)
            db.add(customer)
            num_savings += len(customer.savings)
        print('num of savings: {}'.format(num_savings))
db.commit()
