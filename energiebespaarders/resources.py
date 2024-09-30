import requests
from dagster import resource

class DiscordWebhook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def __call__(self, message):
        requests.post(self.webhook_url, json={"content": message})

@resource(config_schema={"discord_webhook_url": str})
def discord_webhook_resource(context):
    return DiscordWebhook(webhook_url=context.resource_config["discord_webhook_url"])