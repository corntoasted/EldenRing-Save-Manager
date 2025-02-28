import os, json


item_dict = {
    "Upgrade Materials": {
        "Ancient Dragon Stone": [156, 39],
        "Somber Ancient Dragon Stone": [184, 39],
        "Smithing Stone [1]": [116, 39],
        "Smithing Stone [2]": [117, 39],
        "Smithing Stone [3]": [118, 39],
        "Smithing Stone [4]": [119, 39],
        "Smithing Stone [5]": [120, 39],
        "Smithing Stone [6]": [121, 39],
        "Smithing Stone [7]": [122, 39],
        "Smithing Stone [8]": [123, 39],
        "Smithing Stone [9]": [124, 39],
        "Somber Stone [1]": [176, 39],
        "Somber Stone [2]": [177, 39],
        "Somber Stone [3]": [178, 39],
        "Somber Stone [4]": [179, 39],
        "Somber Stone [5]": [180, 39],
        "Somber Stone [6]": [181, 39],
        "Somber Stone [7]": [182, 39],
        "Somber Stone [8]": [183, 39],
        "Somber Stone [9]": [216, 39]
    },
    "Crafting Materials": {
        "Arteria Leaf": [211,80],
        "Flight Pinion": [212,58],
        "Gold Fireflies": [75,81],
        "Root Resin": [39,81],
        "Old Fang": [192,58],
        "Great Dragonfly Head":[6, 59],
        "Golden Centipede":[84, 81],

    },
    "Runes": {
        "Lords Rune": [103, 11],
        "Hero's Rune [1]":[98, 11],
        "Hero's Rune [4]":[101, 11],
        "Golden Rune [1]": [84, 11],
        "Golden Rune [2]": [85, 11],
        "Golden Rune [3]": [86, 11],
        "Golden Rune [4]": [87, 11],
        "Golden Rune [5]": [88, 11],
        "Golden Rune [6]": [89, 11],
        "Golden Rune [7]": [90, 11],
        "Golden Rune [8]": [91, 11],
        "Golden Rune [9]": [92, 11],
        "Golden Rune [10]": [93, 11],
        "Golden Rune [11]": [94,11],
        "Golden Rune [12]": [95,11],
    },
    "Key Items": {
        "Larval Tear": [249, 31],
        "Sacred Tear": [36,39],
        "Golden Seed": [26,39],
        "Swordstone Key": [64,31],
        'Imbued Sword Key':[250, 31],
        'Cracked Pot':[28, 37],
        'Ritual Pot':[29, 37],
        'Perfume Bottle':[38, 37],
        'Memory Stone':[46, 39],
        'Talisman Pouch':[56, 39],
        'Dragon Heart':[76, 39],
        'Celestial Dew':[82, 8],
    },
    "Tools": {
        "Rune Arc": [190, 0],
        "Starlight Shards":[10, 5],
        "Gold Pickled Foot": [176, 4],
        "Silver Pickled Foot": [166,4],
        "Bewitching Branches": [22,13]
    },
    "Gloveworts": {
        "Grave Glovewort [1]": [148, 42],
        "Grave Glovewort [2]": [149, 42],
        "Grave Glovewort [3]": [150, 42],
        "Grave Glovewort [4]": [151, 42],
        "Grave Glovewort [5]": [152, 42],
        "Grave Glovewort [6]": [153, 42],
        "Grave Glovewort [7]": [154, 42],
        "Grave Glovewort [8]": [155, 42],
        "Grave Glovewort [9]": [156, 42],
        "Great Grave Glovewort": [157, 42],
        "Ghost Glovewort [1]": [158, 42],
        "Ghost Glovewort [2]": [159, 42],
        "Ghost Glovewort [3]": [160, 42],
        "Ghost Glovewort [4]": [161, 42],
        "Ghost Glovewort [5]": [162, 42],
        "Ghost Glovewort [6]": [163, 42],
        "Ghost Glovewort [7]": [164, 42],
        "Ghost Glovewort [8]": [165, 42],
        "Ghost Glovewort [9]": [166, 42],
        "Great Ghost Glovewort": [167, 42],
    },
    "Consumables": {

        "Bloodboil Aromatic": [222,13],
        "Neutralizing Boluses": [132, 3],
        "Stanching Boluses": [142, 3],
        "Thawfrost Boluses": [152, 3],
        "Stimulating Boluses": [162, 3],
        "Preserving Boluses": [172, 3],
        "Rejuvenating Boluses": [182, 3],
        "Clarifying Boluses": [192, 3],
        "Exalted Flesh": [186,4],
        'Spellproof Dried Liver':[126, 4],
        'Fireproof Dried Liver':[136, 4],
        'Lightningproof Dried Liver':[146, 4],
        'Holyproof Dried Liver':[156, 4],
        'Immunizing White Cured Meat':[30, 5],
        'Invigorating White Cured Meat':[40, 5],
        'Clarifying White Cured Meat':[50, 5],
        'Dappled White Cured Meat':[60, 5],

    },

    "Grease": {
        'Fire Grease':[120, 5],
        'Lightning Grease':[130, 5],
        'Magic Grease':[140, 5],
        'Holy Grease':[150, 5],
        'Blood Grease':[160, 5],
        'Soporific Grease':[170, 5],
        'Poison Grease':[180, 5],
        'Freezing Grease':[190, 5],
        'Dragonwound Grease':[200, 5],
        'Rot Grease':[210, 5],
        'Drawstring Fire Grease':[220, 5],
        'Drawstring Lightning Grease':[230, 5],
        'Drawstring Magic Grease':[240, 5],
        'Drawstring Holy Grease':[250, 5],
        'Drawstring Blood Grease':[4, 6],
        'Drawstring Soporific Grease':[14, 6],
        'Drawstring Poison Grease':[24, 6],
        'Drawstring Freezing Grease':[34, 6],
        'Drawstring Rot Grease':[54, 6],
        'Shield Grease':[154, 6],
        'Holy Water Grease':[228, 12],

    },

    "Remembrance": {
        "R- The Grafted":[134,11],
        "R- Starsourge":[135,11],
        "R - Omen King":[136,11],
        "R- Blasphemous":[137,11],
        "R- Rot Goddess":[138,11],
        "R- Blood Lord":[139,11],
        "R- Black Blade":[140,11],
        "R- Hoarah Loux":[141,11],
        "R- DragonLord":[142,11],
        "R- Full Moon Queen":[143,11],
        "R- Lich Dragon":[144,11],
        "R- Fire Giant":[145,11],
        "R- Regal Ancestor":[146,11],
        "R- Elden":[147,11],
        "R- Naturalborn":[148,11],
    },
    "Ash of War": {
        "Lost Ash of War": [86, 39],
    }

}


class Items:
    def __init__(self):
        self.db = item_dict
        if os.path.exists("./data/config.json"):
            with open("./data/config.json", "r") as f:
                js = json.load(f)
                self.db["Custom Items"] = js["custom_ids"]  # ADDS custom IDS from config to itemdb merging with hard coded items
        self.categories = list(self.db.keys())  # Populate 1st dropdown menu


    def get_item_ls(self, cat):
        return list(self.db[cat])  # populate 2nd dropdown menu
