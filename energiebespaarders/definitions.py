import os
from dagster import Definitions, load_assets_from_modules, define_asset_job, ScheduleDefinition
from . import assets
from .resources import discord_webhook_resource

all_assets = load_assets_from_modules([assets])

data_processing_job = define_asset_job(
    name="data_processing_job",
    selection=all_assets,
)

data_processing_schedule = ScheduleDefinition(
    job=data_processing_job,
    cron_schedule="*/2 * * * *",  # Run every 2 minutes
)

defs = Definitions(
    assets=all_assets,
    jobs=[data_processing_job],
    schedules=[data_processing_schedule],
    resources={
        "discord_webhook": discord_webhook_resource.configured(
            {"discord_webhook_url": os.environ.get("DISCORD_WEBHOOK_URL", "")}
        )
    }
)