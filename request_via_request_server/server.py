import logging
from typing import Any

import aiohttp
import requests
import uvicorn
from dns import message, query, rdatatype
from fastapi import FastAPI
from request_via_request_server.models import Doh, RequestGet, RequestPost

log = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None)


async def make_request(method: str, url: str, proxy: str | None = None, json: dict[str, Any] | None = None, answer_type: str | None = None) -> Any:

    valid_answers = {'status_code', 'json', 'content', 'headers'}
    if answer_type is not None and answer_type not in valid_answers:
        raise ValueError('Unknown answer.')

    async with aiohttp.ClientSession() as session:
        async with session.request(method=method, url=url, proxy=proxy, json=json, ssl=False, timeout=15) as resp:
            if answer_type is None or answer_type == 'status_code':
                return resp.status
            elif answer_type == 'json':
                try:
                    resp_json: dict[str, Any] = await resp.json()
                    return resp_json
                except aiohttp.ContentTypeError as error:
                    log.error('Response content type is not json, %s', error)
            elif answer_type == 'content':
                resp_content: str = await resp.text()
                return resp_content
            elif answer_type == 'headers':
                return resp.headers
    return None


@app.post("/curl/get")
async def curl_get(request_schema: RequestGet, proxy: bool = False) -> Any:
    req = {**request_schema.dict()}
    if not proxy:
        log.info('Request GET without proxy, %s', req)
        response = await make_request(method='get', url=request_schema.url, answer_type=req['answer_type'])
        return response
    else:
        if req['proxy_server'] is None:
            raise ValueError('Proxy settings not given.')
        log.info('Request GET via proxy,  %s', req)
        response = await make_request(
            method='get',
            proxy=f"{req['proxy_server']['proxy_url']}:{req['proxy_server']['port']}",
            url=request_schema.url,
            answer_type=req['answer_type'],
        )
        return response


@app.post("/curl/post")
async def curl_post(request_schema: RequestPost, proxy: bool = False) -> Any:
    req = {**request_schema.dict()}
    if not proxy:
        log.info('Request POST without proxy, %s', req)
        response = await make_request(method='post', url=request_schema.url, json=req['data'], answer_type=req['answer_type'])
        return response
    else:
        if req['proxy_server'] is None:
            raise ValueError('Proxy settings not given.')
        log.info('Request POST via proxy,  %s', req)
        response = await make_request(
            method='post',
            proxy=f"{req['proxy_server']['proxy_url']}:{req['proxy_server']['port']}",
            url=request_schema.url,
            json=req['data'],
            answer_type=req['answer_type'],
        )
        return response


@app.post("/doh")
async def doh(request_schema: Doh) -> Any:
    doh_response = None
    req = {**request_schema.dict()}
    with requests.Session() as session:
        get_query = message.make_query(req['domain'], rdatatype.A)
        doh_request = query.https(get_query, req['doh_server'], session=session)
        for answer in doh_request.answer:
            doh_response = str(answer)
    return {"doh_response": doh_response}


@app.get("/ping")
async def ping() -> str:
    return "pong"


def main():
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()
