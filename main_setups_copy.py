from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from main_machine_monitoring.database.orm_class import Live, LiveRecent

# Assuming your models are defined in a file named 'models.py'
import time
import random
from datetime import datetime, time as dt_time


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:siri2251105@localhost/gerb"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:siri2251105@172.18.7.66/gerb"

# Create the engine and bind it to the base
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
Base.metadata.bind = engine

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define shift timings
shifts = [
    (dt_time(9, 0), dt_time(13, 0)),    # 9:00 AM - 1:00 PM
    (dt_time(13, 30), dt_time(15, 30)), # 1:30 PM - 3:30 PM
    (dt_time(16, 0), dt_time(18, 0))    # 4:00 PM - 6:00 PM
]


def get_current_shift():
    now = datetime.now().time()
    for idx, (start, end) in enumerate(shifts):
        if start <= now <= end:
            return "on"
    return "off"


# Set the initial state and start time
state = "off"
start_time = datetime.now().time()

# Check the shift status and update the state and start time
current_shift_status = get_current_shift()
if current_shift_status == "on":
    state = "production"
    start_time = datetime.now().time()

# Example usage
print(f"State: {state}")
print(f"Start time: {start_time}")