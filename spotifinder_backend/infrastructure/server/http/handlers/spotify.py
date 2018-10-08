import aiohttp
from typing import Mapping

from spotifinder_backend.usecases.constants import *

AUTH_URL = 'https://accounts.spotify.com/api/token'
RECOMMEND_URL = 'https://api.spotify.com/v1/recommendations'

LIMIT = 'limit'

async def get_resource_analysis(request: aiohttp.web.Request) -> aiohttp.web.Response:
	auth_response = await _do_post_with_auth(AUTH_URL, request.app[SPOTIFY_CLIENT_ID], request.app[SPOTIFY_CLIENT_SECRET], {'grant_type': 'client_credentials'})
	auth_token = auth_response["access_token"]
	query_params = request.query
	return aiohttp.web.json_response({"spotify_uri":query_params["spotify_uri"]})


async def _do_get_with_auth(url, token, **kwargs):
	pass

async def _do_post_with_auth(url: str, client_id: str, client_secret:str, payload: Mapping):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, auth=aiohttp.BasicAuth(client_id, client_secret), data=payload) as resp:
                print("-> Response: {0}".format(resp.status))
                return await resp.json()
    except Exception as e:
        print("ERR: {}".format(e))