
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Program(Base):

    __tablename__ = 'programs'

    id_  = Column('id',   Integer(), primary_key=True)
    name = Column('name', Text()                     )

    team_members = relationship('TeamMember', backref='elevate_program')
    savings      = relationship('Saving',     backref='elevate_program')


class Customer(Base):

    __tablename__ = 'customers'

    sf_id   = Column('sf_id',   Text(), primary_key=True)
    name    = Column('name',    Text()                  )
    address = Column('address', Text()                  )

    savings = relationship('Saving', backref='elevate_customer')


class TeamMember(Base):

    __tablename__ = 'team_members'

    id_           = Column('id',            Integer(), primary_key=True                             )
    name          = Column('name',          Text()                                                  )
    billable_rate = Column('billable_rate', Numeric()                                               )
    program       = Column('program',       Integer(), ForeignKey('programs.id', ondelete='CASCADE'))


class Saving(Base):

    __tablename__ = 'savings'

    id_            = Column('id',             Integer(), primary_key=True                                 )
    customer       = Column('customer_id',    Text(),    ForeignKey('customers.sf_id', ondelete='CASCADE'))
    program        = Column('program_id',     Integer(), ForeignKey('programs.id', ondelete='CASCADE')    )
    stamp          = Column('stamp',          DateTime()                                                  )
    money_savings  = Column('money_savings',  Numeric()                                                   )
    energy_savings = Column('energy_savings', Numeric()                                                   )