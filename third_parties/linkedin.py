import json
from pathlib import Path
from datetime import datetime
import os
import requests

DATA_DIR = Path(__file__).parent.parent / "data"


def scrape_linkedin_profile(
    linkedin_profile_url: str,
    max_activities=5,
    max_experiences=5,
    data_file: str | None = None,
):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

    if data_file is not None:
        with open(data_file, "r") as json_file:
            data = json.load(json_file)
    else:
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers={
                "Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'
            },
        )
        data = response.json()
        now = datetime.utcnow().isoformat()
        filename = f"proxycurl-{now}.json"
        with open(DATA_DIR / filename, "w") as json_file:
            json.dump(data, json_file, indent=2)
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    activities = data.get("activities", list())
    if activities and isinstance(activities, list):
        data["activities"] = activities[:max_activities]

    experiences = data.get("experiences", list())
    if experiences and isinstance(experiences, list):
        data["experiences"] = activities[:max_experiences]

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
