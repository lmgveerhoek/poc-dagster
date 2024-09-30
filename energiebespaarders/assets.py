import random
from datetime import datetime
from dagster import asset, AssetExecutionContext

class SimulatedDatabase:
    def __init__(self):
        self.data = []
        self.rmse_history = []

    def insert_data(self, date, value):
        self.data.append((date, value))

    def get_last_4_weeks_data(self):
        return self.data[-28:]  # Assuming 1 data point per day

    def insert_rmse(self, rmse):
        self.rmse_history.append((datetime.now(), rmse))

    def get_last_rmse(self):
        return self.rmse_history[-1][1] if self.rmse_history else None

simulated_db = SimulatedDatabase()

@asset
def raw_data():
    # Simulate fetching data
    current_date = datetime.now().date()
    simulated_db.insert_data(current_date, random.randint(1, 100))
    return simulated_db.get_last_4_weeks_data()

@asset
def processed_data(raw_data):
    # Simulate processing
    rmse = random.uniform(20, 100)
    return {"rmse": rmse}

@asset
def comparison_result(processed_data):
    current_rmse = processed_data["rmse"]
    last_rmse = simulated_db.get_last_rmse()
    
    if last_rmse is None:
        # If there's no previous RMSE, generate one for comparison
        last_rmse = random.uniform(20, 100)
    
    is_improved = current_rmse < last_rmse
    
    simulated_db.insert_rmse(current_rmse)

    return {
        "is_improved": is_improved,
        "current_rmse": current_rmse,
        "last_rmse": last_rmse
    }

@asset(required_resource_keys={"discord_webhook"})
def discord_notification(context: AssetExecutionContext, comparison_result):
    current_rmse = comparison_result["current_rmse"]
    last_rmse = comparison_result["last_rmse"]
    
    if comparison_result["is_improved"]:
        message = f"✅ Task completed successfully. RMSE improved from {last_rmse:.2f} to {current_rmse:.2f}."
    else:
        message = f"⚠️ Task completed successfully. RMSE worsened from {last_rmse:.2f} to {current_rmse:.2f}."

    context.resources.discord_webhook(message)