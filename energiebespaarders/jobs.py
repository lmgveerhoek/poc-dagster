from dagster import job
from .assets import raw_data, processed_data, comparison_result
from .ops import send_teams_message

@job
def data_processing_job():
    comparison = comparison_result(processed_data(raw_data()))
    send_teams_message(comparison)