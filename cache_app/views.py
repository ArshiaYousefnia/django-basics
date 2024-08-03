import time

from django.http import HttpResponse
from django.shortcuts import render

from django.core.cache import cache


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

    cache.set(cache_key, out, timeout=60*60)  # Cache for 1 hour

    return out, False
