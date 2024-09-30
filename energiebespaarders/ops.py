from dagster import op
import requests

@op(required_resource_keys={"teams_webhook"})
def send_teams_message(context, comparison_result):
    webhook_url = context.resources.teams_webhook

    if comparison_result["is_improved"]:
        message = f"Task completed successfully. RMSE improved from {comparison_result['last_rmse']:.2f} to {comparison_result['current_rmse']:.2f}."
    else:
        message = f"Task completed successfully. RMSE worsened from {comparison_result['last_rmse']:.2f} to {comparison_result['current_rmse']:.2f}."

    requests.post(webhook_url, json={"text": message})