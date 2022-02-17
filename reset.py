from charts import create_money_savings_by_program_by_yr, energy_savings_by_program_by_yr, create_savings_by_metric_by_yr, \
    create_np_savings_money_by_yr, create_np_savings_energy_by_yr
from db_load import create_team_members, create_customers_savings
from models import Customer, TeamMember, Saving
from utils import create_db_session, check_records

def reset():
    db = create_db_session()
    db.query(Customer).delete()
    db.query(TeamMember).delete()
    db.query(Saving).delete()
    create_team_members(db)
    create_customers_savings(db)
    db.commit()

    create_money_savings_by_program_by_yr(db)
    energy_savings_by_program_by_yr(db)
    create_savings_by_metric_by_yr(db)
    create_np_savings_money_by_yr(db)
    create_np_savings_energy_by_yr(db)

if __name__ == '__main__':
    reset()