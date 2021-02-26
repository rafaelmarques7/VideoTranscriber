import pytest
from .main import validate_youtube_url


def test_validate_youtube_url():
    url = "https://youtube.com"
    assert validate_youtube_url(url)

    url = "https://www.youtube.com/watch?v=_obW_cBWfUU"
    assert validate_youtube_url(url)

    url = "https://youtu.be/_obW_cBWfUU"
    assert validate_youtube_url(url)

    url = "http://youtu.be/_obW_cBWfUU"
    assert validate_youtube_url(url)


def test_validate_youtube_url_rejects_bad_input():
    url = None
    assert not validate_youtube_url(url)

    url = "http://invalid.domain"
    assert not validate_youtube_url(url)
