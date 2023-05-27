import os
import requests

# api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
# api_key = 'x9xBtdm9J5ib_uhAJpF4KQ'
# header_dic = {'Authorization': 'Bearer ' + api_key}
# params = {
#'url': 'https://www.linkedin.com/in/rodmorison/',
##'fallback_to_cache': 'on-error',
##'use_cache': 'if-present',
##'skills': 'include',
##'inferred_salary': 'include',
##'personal_email': 'include',
##'personal_contact_number': 'include',
##'twitter_profile_id': 'include',
##'facebook_profile_id': 'include',
##'github_profile_id': 'include',
##'extra': 'include',
# }
# response = requests.get(api_endpoint, params=params, headers=header_dic)


class NotFound(Exception):
    ...


def scrape_linkedin_profile(linkedin_profile_url: str, use_gist=False):
    """scrape information from LinkedIn profiles, Manually scrape the
    information from the LinkedIn profile"""

    if use_gist:
        api_endpoint = "https://gist.githubusercontent.com/rmorison/d61224a1d94169e3c72b8dda887aea14/raw/e7d182bc61b9996cfcaad3650f47b92cc9f00571/rm.json"
        response = requests.get(api_endpoint)
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {
            "Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}",
        }

        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
        )

    if response.status_code != 200:
        raise NotFound

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ({}, [], "", None)
        and k
        not in ("people_also_viewed", "certifications", "recommendations")
    }
    if data.get("groups"):
        for group_dict in data.get(groups):
            group_dict.pop("profile_pic_url")
    if data.get("experiences"):
        data["experiences"] = data["experiences"][:5]

    return data
