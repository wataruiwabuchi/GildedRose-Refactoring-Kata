from typing import Dict, Final

import pytest
from pydantic import BaseModel

from gilded_rose import AGED_BRIE, BACKSTAGE, SULFURAS, GildedRose, Item

DEFAULT_ITEM_NAME: Final[str] = "default"


class _TestCase(BaseModel):
    name: str
    sell_in: int
    quality: int
    expect_sell_in: int
    expect_quality: int


TEST_CASES: Dict[str, _TestCase] = {
    "normal": _TestCase(
        name=DEFAULT_ITEM_NAME, sell_in=1, quality=1, expect_sell_in=0, expect_quality=0
    ),
    "quality is never negative": _TestCase(
        name=DEFAULT_ITEM_NAME,
        sell_in=0,
        quality=0,
        expect_sell_in=-1,
        expect_quality=0,
    ),
    "Once the sell by date has passed, Quality degrades twice as fast": _TestCase(
        name=DEFAULT_ITEM_NAME,
        sell_in=0,
        quality=2,
        expect_sell_in=-1,
        expect_quality=0,
    ),
    "AGED_BRIE's quality increase": _TestCase(
        name=AGED_BRIE, sell_in=1, quality=0, expect_sell_in=0, expect_quality=1
    ),
    "Once the sell by date has passed, AGED_BRIE's quality increase twice as fast": _TestCase(
        name=AGED_BRIE, sell_in=0, quality=0, expect_sell_in=-1, expect_quality=2
    ),  # Once the sell by date has passed, AGED_BRIE's quality increase twice as fast
    "AGED_BRIE's quality is never more than 50": _TestCase(
        name=AGED_BRIE, sell_in=0, quality=50, expect_sell_in=-1, expect_quality=50
    ),
    "SULFURAS's quality never decrease and sell_in never decrease": _TestCase(
        name=SULFURAS, sell_in=10, quality=80, expect_sell_in=10, expect_quality=80
    ),
    "BACKSTAGE's quality increase when there are more than 10 days": _TestCase(
        name=BACKSTAGE, sell_in=12, quality=10, expect_sell_in=11, expect_quality=11
    ),
    "BACKSTAGE's quality increase when there are 10 days or less case 1": _TestCase(
        name=BACKSTAGE, sell_in=11, quality=10, expect_sell_in=10, expect_quality=11
    ),
    "BACKSTAGE's quality increase when there are 10 days or less case 2": _TestCase(
        name=BACKSTAGE, sell_in=10, quality=10, expect_sell_in=9, expect_quality=12
    ),
    "BACKSTAGE's quality increase when there are 5 days or less case 1": _TestCase(
        name=BACKSTAGE, sell_in=6, quality=10, expect_sell_in=5, expect_quality=12
    ),
    "BACKSTAGE's quality increase when there are 5 days or less case 2": _TestCase(
        name=BACKSTAGE, sell_in=5, quality=10, expect_sell_in=4, expect_quality=13
    ),
    "BACKSTAGE's quality drops to 0 after the concert case 1": _TestCase(
        name=BACKSTAGE, sell_in=1, quality=10, expect_sell_in=0, expect_quality=13
    ),
    "BACKSTAGE's quality drops to 0 after the concert case 2": _TestCase(
        name=BACKSTAGE, sell_in=0, quality=10, expect_sell_in=-1, expect_quality=0
    ),
}


@pytest.mark.parametrize("test_case", TEST_CASES.values(), ids=TEST_CASES.keys())
def test_update_quality(test_case: _TestCase):
    items = [Item(test_case.name, test_case.sell_in, test_case.quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert (
        items[0].sell_in == test_case.expect_sell_in
        and items[0].quality == test_case.expect_quality
    )
