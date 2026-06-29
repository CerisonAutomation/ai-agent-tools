"""
Guesty sync workflow — fetches reservations and syncs to internal store.
Registered in the workflow registry as 'guesty.sync_reservations'.
"""

import httpx
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


async def guesty_sync_reservations(input_data: dict) -> dict:
    """
    Fetch reservations from Guesty for a date window and return summary.
    input_data: { api_token, base_url, days_ahead (optional, default 30) }
    """
    api_token = input_data["api_token"]
    base_url  = input_data.get("base_url", "https://open-api.guesty.com/v1")
    days      = int(input_data.get("days_ahead", 30))

    from_date = datetime.utcnow()
    to_date   = from_date + timedelta(days=days)

    headers = {"Authorization": f"Bearer {api_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/reservations",
            headers=headers,
            params={
                "checkIn[gte]": from_date.date().isoformat(),
                "checkIn[lte]": to_date.date().isoformat(),
                "limit": 100,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

    reservations = data.get("results", [])
    logger.info(f"Guesty sync: fetched {len(reservations)} reservations")

    return {
        "count": len(reservations),
        "from": from_date.date().isoformat(),
        "to": to_date.date().isoformat(),
        "reservation_ids": [r["_id"] for r in reservations],
    }
