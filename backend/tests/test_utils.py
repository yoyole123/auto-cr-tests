"""Unit tests for the helper functions."""
from app.utils import clamp_page_size, mask_email, slugify


def test_slugify():
    assert slugify("  Hello World!  ") == "hello-world"
    assert slugify("a/b__c") == "a-b-c"
    assert slugify("") == ""


def test_clamp_page_size():
    assert clamp_page_size(None) == 20
    assert clamp_page_size(0) == 1
    assert clamp_page_size(5) == 5
    assert clamp_page_size(10_000) == 100


def test_mask_email():
    assert mask_email("jane@example.com") == "j***@example.com"
    assert mask_email("not-an-email") == "***"
