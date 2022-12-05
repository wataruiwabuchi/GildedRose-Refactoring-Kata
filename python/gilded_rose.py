from typing import Final

AGED_BRIE: Final[str] = "Aged Brie"
BACKSTAGE: Final[str] = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS: Final[str] = "Sulfuras, Hand of Ragnaros"


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == AGED_BRIE:
                self._update_aged_brie(item)
            elif item.name == BACKSTAGE:
                self._update_backstage(item)
            elif item.name == SULFURAS:
                self._update_sulfuras(item)
            else:
                self._update_default(item)

    @staticmethod
    def _update_default(item) -> None:
        new_sell_in = item.sell_in - 1
        if new_sell_in >= 0:
            new_quality = item.quality - 1
        else:
            new_quality = item.quality - 2

        item.sell_in = new_sell_in
        item.quality = new_quality if new_quality >= 0 else 0

    @staticmethod
    def _update_aged_brie(item):
        assert item.name == AGED_BRIE

        new_sell_in = item.sell_in - 1
        if new_sell_in >= 0:
            new_quality = item.quality + 1
        else:
            new_quality = item.quality + 2

        item.sell_in = new_sell_in
        item.quality = new_quality if new_quality <= 50 else 50

    @staticmethod
    def _update_backstage(item):
        assert item.name == BACKSTAGE

        new_sell_in = item.sell_in - 1
        if new_sell_in < 0:
            new_quality = 0
        elif new_sell_in < 5:
            new_quality = item.quality + 3
        elif new_sell_in < 10:
            new_quality = item.quality + 2
        else:
            new_quality = item.quality + 1

        item.sell_in = new_sell_in
        item.quality = new_quality if new_quality <= 50 else 50

    @staticmethod
    def _update_sulfuras(item):
        assert item.name == SULFURAS


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
