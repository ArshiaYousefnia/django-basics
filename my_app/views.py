import time
import aiohttp
import asyncio
from django.http import HttpResponse
import requests
from django.core.cache import cache
import logging

from django.views.decorators.cache import cache_page


# logging.basicConfig(
#    filename="app.log",
#    encoding="utf-8",
#    filemode="a",
#    level=logging.DEBUG,
#    format="{asctime} - {levelname} - {message}",
#    style="{",
#    datefmt="%Y-%m-%d %H:%M",
# )


# Create your views here.

def index(request, integer):
    t_1 = time.time()
    output, was_cached = factorial(integer)
    t_2 = time.time()

    return HttpResponse(f"Hello, world. You're at the polls index.\n"
                        f"the factorial of {integer} is {output}\ntime: {t_2 - t_1}\nwas cached: {was_cached}")


def factorial(integer):
    cache_key = f"expensive_function_{integer}"
    result = cache.get(cache_key)
    if result is not None:
        return result, True

    out = 1
    for i in range(1, integer + 1):
        out *= i
    time.sleep(2)

    cache.set(cache_key, out, timeout=60 * 60)  # Cache for 1 hour

    return out, False


@cache_page(timeout=60 * 30)
async def fetch_pokemon(poke_id: int):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as res:
            pokemon_data = await res.json()

            return pokemon_data['name']


@cache_page(timeout=60 * 30)
async def fact_report(request, num):
    start_time = time.time()

    tasks = [fetch_pokemon(i + 20) for i in range(1, num + 1)]

    ## asyncio.run(fetch_random_user(40))

    data = await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time

    output = {"time": elapsed_time, 'data': data}

    my_logger = logging.getLogger("my_custom_logger")
    my_logger.warning(f"async pokemon request: num: {num}, time: {elapsed_time}", exc_info=True)

    return HttpResponse(str(output))


def serial_poke(request, num):
    start_time = time.time()

    data = [requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_id}").json()['name'] for poke_id in
            range(1, num + 1)]

    end_time = time.time()
    elapsed_time = end_time - start_time

    output = {"time": elapsed_time, 'data': data}

    my_logger = logging.getLogger("my_custom_logger")
    my_logger.warning(f"sync pokemon request: num: {num}, time: {elapsed_time}", exc_info=True)

    return HttpResponse(str(output))
