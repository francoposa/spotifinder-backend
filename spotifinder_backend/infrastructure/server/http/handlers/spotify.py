import aiohttp
from typing import Mapping

async def get_resource_analysis(request: aiohttp.web.Request) -> aiohttp.web.Response:
	query_params = request.query 
	return aiohttp.web.json_response({"spotify_uri":query_params["spotify_uri"]})


async def _do_post(self, url: str, payload: Mapping):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                self._reporter.info("-> Response: {0}".format(resp.status))
                self._reporter.info(await resp.json())
    except Exception as e:
        self._reporter.info("ERR: {}".format(e))