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
    (dt_time(9, 0), dt_time(13, 0)),   # 9:00 AM - 1:00 PM
    (dt_time(13, 30), dt_time(15, 30)), # 1:30 PM - 3:30 PM
    (dt_time(16, 0), dt_time(18, 0))   # 4:00 PM - 6:00 PM
]


def get_current_shift():
    now = datetime.now().time()
    for idx, (start, end) in enumerate(shifts):
        if start <= now <= end:
            return idx
    return None


def create_and_insert_data():
    try:
        # Initialize a dictionary to track the machine states
        machine_states = {machine_id: {"value": None, "time": None} for machine_id in range(1, 13)}
        current_shift = get_current_shift()
        state_start_time = datetime.now()

        while True:
            current_shift = get_current_shift()
            if current_state["value"] == 2:
                current = 2.3
            if current_shift is not None:
                shift_start, shift_end = shifts[current_shift]

                # Check if it's time for a break
                if shift_start <= datetime.now().time() <= shift_start.replace(minute=shift_start.minute + 2):
                    time.sleep(180)  # Sleep for 3 minutes

            # Loop over five machines
            for machine_id in range(1, 13):
                # Get the current state of the machine
                current_state = machine_states[machine_id]

                if current_state["value"] == 0 and current_state["time"] is not None:
                    elapsed_time = (datetime.now() - current_state["time"]).seconds
                    if elapsed_time >= 120 and elapsed_time <= 180:
                        # Continue generating 0 value
                        current = 0.0
                        voltage = 0.0
                    else:
                        # Generate random non-zero values
                        current = round(random.uniform(5.0, 15.0), 1)
                        voltage = round(random.uniform(200.0, 250.0), 1)
                        machine_states[machine_id]["value"] = current
                        machine_states[machine_id]["time"] = None
                else:
                    if random.random() < 0.2:  # 20% chance to generate zero values
                        current = 0.0
                        voltage = 0.0
                        machine_states[machine_id]["value"] = 0
                        machine_states[machine_id]["time"] = datetime.now()

                    else:
                        # Generate random non-zero values
                        current = round(random.uniform(5.0, 15.0), 1)
                        voltage = round(random.uniform(200.0, 250.0), 1)
                        machine_states[machine_id]["value"] = current
                        machine_states[machine_id]["time"] = None

                # Create a new session for each machine
                with SessionLocal() as session:
                    try:
                        # Create a new Live object and assign random values
                        new_live_data = Live(machine_id=machine_id, current=current, voltage=voltage, created_at=datetime.now())

                        live_recent_data = session.query(LiveRecent).filter_by(machine_id=machine_id).first()

                        if live_recent_data:
                            # Update the existing row with new values
                            live_recent_data.current = current
                            live_recent_data.voltage = voltage
                            live_recent_data.created_at = datetime.now()
                        else:
                            # Create a new LiveRecent object and assign values
                            new_live_recent_data = LiveRecent(machine_id=machine_id, current=current, voltage=voltage,
                                                              created_at=datetime.now())
                            # Add the new_live_recent_data object to the session
                            session.add(new_live_recent_data)

                        # Add the new_live_data object to the session
                        session.add(new_live_data)

                        # Commit the transaction to the database
                        session.commit()

                        # Optionally, print the newly created Live object
                        print("Inserted Live Data for Machine ID:", machine_id)
                        print("ID:", new_live_data.id)
                        print("Current:", new_live_data.current)
                        print("Voltage:", new_live_data.voltage)
                        print("Created At:", new_live_data.created_at)

                    except Exception as e:
                        session.rollback()
                        print("Error:", e)

            # Wait for 2 seconds before inserting the next random data for all machines
            time.sleep(2)

    except Exception as e:
        print("Error:", e)

# Call the function to create a session and insert random data every 5 seconds
create_and_insert_data()
