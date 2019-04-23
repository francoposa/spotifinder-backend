import aiohttp
from typing import Dict

from spotifinder_backend.usecases.constants import *

AUTH_URL = "https://accounts.spotify.com/api/token"
ANALYZE_URL = "https://api.spotify.com/v1/audio-features"
RECOMMEND_URL = "https://api.spotify.com/v1/recommendations"

LIMIT = "limit"


async def get_resource_analysis(request: aiohttp.web.Request) -> aiohttp.web.Response:
    _, auth_response = await _do_post_with_auth(
        AUTH_URL,
        request.app[SPOTIFY_CLIENT_ID],
        request.app[SPOTIFY_CLIENT_SECRET],
        {"grant_type": "client_credentials"},
    )
    auth_token = auth_response["access_token"]
    query_params = request.query
    response_status, analyze_response = await _do_get_with_resource_id(
        ANALYZE_URL, auth_token, query_params["spotify_uri"]
    )
    print(analyze_response)
    return aiohttp.web.json_response(analyze_response, status=response_status)


async def get_recommendations(request: aiohttp.web.Request) -> aiohttp.web.Response:
    _, auth_response = await _do_post_with_auth(
        AUTH_URL,
        request.app[SPOTIFY_CLIENT_ID],
        request.app[SPOTIFY_CLIENT_SECRET],
        {"grant_type": "client_credentials"},
    )
    auth_token = auth_response["access_token"]
    query_params = request.query
    response_status, recommendation_response = await _do_get_with_query_string(
        RECOMMEND_URL, auth_token, query_params
    )
    print(str(recommendation_response))
    return aiohttp.web.json_response(recommendation_response, status=response_status)


async def _do_get_with_query_string(base_url: str, token: str, query_params: Dict):
    headers = {"Authorization": "Bearer {0}".format(token)}
    query_string = "?"
    for key, value in query_params.items():
        query_string += str(key) + "=" + str(value) + "&"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url + query_string, headers=headers) as resp:
                print("-> Response: {0}".format(resp.status))
                return resp.status, await resp.json()
    except Exception as e:
        print("ERR: {}".format(e))


async def _do_get_with_resource_id(base_url, token, resource_id):
    headers = {"Authorization": "Bearer {0}".format(token)}
    url = base_url.rstrip("/") + "/" + resource_id
    print(url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                print("-> Response: {0}".format(resp.status))
                return resp.status, await resp.json()
    except Exception as e:
        print("ERR: {}".format(e))


async def _do_post_with_auth(
    url: str, client_id: str, client_secret: str, payload: Dict
):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, auth=aiohttp.BasicAuth(client_id, client_secret), data=payload
            ) as resp:
                print("-> Response: {0}".format(resp.status))
                return resp.status, await resp.json()
    except Exception as e:
        print("ERR: {}".format(e))
