#!/usr/bin/env python
# encoding: utf-8
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


from pyshorteners import Shortener, shorteners
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener(shorteners.SENTALA_SHORTENER)
shorten = 'http://senta.la/test'
expanded = 'http://www.test.com'


@responses.activate
def test_sentala_short_method():
    # mock responses
    params = urlencode({
        'dever': 'encurtar',
        'format': 'simple',
        'url': expanded,
    })
    mock_url = '{}?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=shorten,
                  match_querystring=True)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded


@responses.activate
def test_sentala_short_method_bad_response():
    # mock responses
    params = urlencode({
        'dever': 'encurtar',
        'format': 'simple',
        'url': expanded,
    })
    mock_url = '{}?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=shorten, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)
