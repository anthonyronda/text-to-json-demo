monster_template="""
{
  "name": "the query as a string. If there's a comma in the query, put everything after the comma at the beginning of the string and omit the comma ",
  "type": "monster",
  "img": "icons/magic/nature/stealth-hide-beast-eyes-green.webp",
  "items": [ SPECIAL INSTRUCTION: FOR EACH bulleted item in the source article for this query, make an object inside this array following the 1 example below. If the article says to see another article, please include bulleted items from that article too
    {
      "_id": "replace with a different random 16 digit alphanumeric string for each object",
      "name": "the word(s) inside the three single quotes as a string (omit the colon)",
      "type": "ability",
      "sort": 100000,
      "flags": {},
      "img": "icons/sundries/books/book-tooled-eye-gold-red.webp",
      "effects": [],
      "folder": null,
      "system": {
        "description": "<p>The unformatted text after the colon, but anything inside three single quotes should be wrapped in <strong> HTML tags</p>",
        "save": "",
        "pattern": "white",
        "requirements": "",
        "roll": "if there's a percentage between 1-99%% in the beginning of the bulleted description, put 1d100 here as a string. If there's a phrase such as 3-in-6 chance, put 1d6 here as a string.",
        "rollType": "below",
        "rollTarget": either the aforementioned percentage, or number given in "-out-of-6 chance", written as an integer,
        "blindroll": false,
        "tags": []
      },
      "ownership": {
        "default": 0
      },
    },
     END OF EXAMPLE
     SPECIAL INSTRUCTION: for each english word/phrase (NOT numbers or symbols or #d#) after at= in the source article for this query, create an object, also inside this array
    {
      "_id": "replace with a different random 16 digit alphanumeric string for each object",
      "name": "The word or phrase (first word capitalized) as a string",
      "type": "weapon",
      "sort": 600000,
      "flags": {},
      "img": "icons/skills/melee/swords-parry-block-blue.webp",
      "effects": [],
      "folder": null,
      "system": {
        "description": "<p>If there's a bulleted item description matching the word/phrase used in the name above, copy it here too</p>",
        "quantity": {
          "value": 1,
          "max": 0
        },
        "weight": 0,
        "cost": 0,
        "containerId": "",
        "save": "if the description says save as ___, put that word here as a string",
        "equipped": false,
        "range": {
          "short": 0,
          "medium": 0,
          "long": 0
        },
        "pattern": "yellow",
        "damage": "if there is a notation such as 1d6+2 in parenthesis after the word/phrase, copy 1d6 here as a string. Otherwise leave it as an empty string",
        "bonus": if there is a notation such as 1d6+2 in parenthesis after the word/phrase, copy 2 here as an integer. If there isn't an integer number added, put 0 here",
        "tags": [],
        "slow": if the article says it's slow, put true here as a boolean, otherwise put false
        "missile": false,
        "melee": true,
        "counter": {
          "value": if there's a number and × before the word or phrase, copy that number here as an integer. Otherwise put 1 as an integer
          "max": use the same integer here as the value above
        }
      },
      "ownership": {
        "default": 0
      },
    },
    END OF EXAMPLE
  ],
  "effects": [],
  "folder": null,
  "system": {
    "retainer": {
      "enabled": false,
      "loyalty": 0,
      "wage": ""
    },
    "hp": {
      "hd": "a string such as \"1d8\" where 1 is replaced with the number in the article after hd|",
      "value": the hp value as an integer,
      "max": the hp value again, as an integer
    },
    "ac": {
      "value":  number right after ac= as an integer,
      "mod": 0
    },
    "aac": {
      "value": the aac value as an integer (the number to the right of the ac inside square brackets),
      "mod": 0
    },
    "thac0": {
      "value": number right after th= as an integer,
      "bba": the number inside the brackets after the thac0 value as an integer (omit the + sign),
      "mod": {
        "missile": 0,
        "melee": 0
      }
    },
    "saves": {
      "death": {
        "value": the number after D in the sv= line as integer
      },
      "wand": {
        "value": the number after W in the sv= line as integer
      },
      "paralysis": {
        "value": the number after P in the sv= line as integer
      },
      "breath": {
        "value": the number after B in the sv= line as integer
      },
      "spell": {
        "value": the number after S in the sv= line as integer
      }
    },
    "movement": {
      "base": the first number in the mv= line as integer (omit symbols),
      "encounter": the second number in the mv= line (inside parenthesis) as integer,
      "value": ""
    },
    "initiative": {
      "value": 0,
      "mod": 0
    },
    "spells": {
      "1": {
        "max": 0
      },
      "2": {
        "max": 0
      },
      "3": {
        "max": 0
      },
      "4": {
        "max": 0
      },
      "5": {
        "max": 0
      },
      "6": {
        "max": 0
      },
      "enabled": false
    },
    "details": {
      "biography": "The full description at the top of the article as a string, each paragraph wrapped in <p> HTML tags, and each portion inside three single quotes wrapped inside <strong> HTML tags, all as a string",
      "alignment": "word after al= as a string",
      "xp": "number after xp= as an integer",
      "specialAbilities": "number of times specialability is repeated in the hd= line, as an integer",
      "treasure": {
        "table": "@UUID[Compendium.ose-advancedfantasytome.tables.RollTable.xeGURxYqgotXb68P]",
        "type": ""
      },
      "appearing": {
        "d": "the expression after na= such as \"1d8\" as a string",
        "w": "the expression inside parenthesis in the na= line as a string. If it's not there leave an empty string"
      },
      "morale": the number after ml= as an integer,
      "movement": "the full line after mv= as a string"
    },
    "encumbrance": {
      "value": null,
      "max": null
    },
    "config": {},
    "languages": {}
  },
}
"""

spell_template="""
{
    
}
"""

ability_template="""
{
    
}
"""

weapon_template="""
{
  "name": "the query as a string. If there's a comma in the query, put everything after the comma at the beginning of the string and omit the comma",
  "type": "weapon",
  "img": "icons/weapons/maces/mace-flanged-steel.webp",
  "effects": [],
  "folder": null,
  "system": {
    "description": "For each comma-separated keyword at the end of the query's row in the article, put a new paragraph inside <p> HTML tags, and copy the keyword here with a following colon, all inside <strong> HTML tags, and finally use the description for that keyword found at the bottom of the article",
    "quantity": {
      "value": 1,
      "max": 0
    },
    "weight": second number after the query in the table, as an integer,
    "cost": first number after the query in the table, as an integer,
    "containerId": "",
    "save": "",
    "equipped": false,
    "range": {
      "short": 0,
      "medium": 0,
      "long": 0
    },
    "pattern": "white",
    "damage": "in the expression such as \"1d6+2\" in the table after the query (third column after query's column), copy \"1d6\" here as a string",
    "bonus": in the expression such as \"1d6+2\" in the table after the query (third column after query's column), copy 2 here as an integer",
    "tags": [ SPECIAL INSTRUCTION: FOR EACH comma separated keyword in the query's row in the article, create a new object here inside the array
        "title": "keyword as a string",
        "value": "keyword as a string, again"
      }
      END OF EXAMPLE
    ],
    "slow": if \"Slow\" was one of the keywords, put true here as a boolean, otherwise put false,
    "missile": if \"Missile\" was a word inside one of the keywords, put true here as a boolean, otherwise put false,
    "melee": if \"Melee\" was a word inside one of the keywords, put true here as a boolean, otherwise put false,
    "counter": {
      "value": 0,
      "max": 0
    }
  },
}
"""

item_template="""
{
  "name": "the query as a string. If there's a comma in the query, put everything after the comma at the beginning of the string and omit the comma",
  "type": "item",
  "img": "icons/commodities/treasure/token-gold-cross.webp",
  "effects": [],
  "folder": null,
  },
  "system": {
    "description": "<p></p>",
    "quantity": {
      "value": 1,
      "max": 1
    },
    "weight": null,
    "cost": 25,
    "containerId": "",
    "treasure": false,
    "tags": []
  },
}
"""

treasure_table_template="""
{
    
}
"""

pokemon_template="""
{
 "team": [
 SPECIAL INSTRUCTION: put at least one, but no more than six, JSON objects in this array. Each pokemon in the team requested is its own object
 {
    "name": "the name of the pokemon as a string",
    "types": [ SPECIAL INSTRUCTION: put each type of the pokemon found after |type= in the base stats table as a string
        "grass",
        END OF EXAMPLE
    ]
    "baseStats": {
      "hp": the number after |HP= as an integer,
      "attack": the number after |Attack= as an integer,
      "defense": the number after |Defense= as an integer,
      "speed": the number after |Speed= as an integer,
      "special": the number after |Special= as an integer
    },
    "moves": [ SPECIAL INSTRUCTION: put each move selected for the current pokemon as a string. There can be no fewer than one, and no more than four
        "Quick Attack",
        END OF EXAMPLE
    ]
 }
 END OF EXAMPLE
 ],

}

"""
nethack_monster_template="""
{
  "name": "the query as a string. If there's a comma in the query, put everything after the comma at the beginning of the string and omit the comma",
  "type": "monster",
  "img": "icons/magic/nature/stealth-hide-beast-eyes-green.webp",
  "items": [ SPECIAL INSTRUCTION: FOR EACH query-related factoid (e.g. "\{query\} can lay eggs") in the given articles, make an object inside this array
    {
      "_id": "replace with a different random 16 digit alphanumeric string for each object. for example (do not copy example): Pu7Tk9A7hypZMqMb",
      "name": "the attack or factoid (first word capitalized) as a string",
      "type": "ability",
      "sort": 100000,
      "flags": {},
      "img": "icons/sundries/books/book-tooled-eye-gold-red.webp",
      "effects": [],
      "folder": null,
      "system": {
        "description": "<p>The unformatted text describing the attack or factoid in the provided articles, but anything inside three single quotes should be wrapped in <strong> HTML tags. Anything wrapped in [[double brackets]] should receive a new ability object, but only if information about that factoid is available.</p><p>Separate thoughts into multiple paragraph tags.</p>",
        "save": "",
        "pattern": "white",
        "requirements": "",
        "roll": "if there's a percentage between 1-99%% in the description, put 1d100 here as a string. If there's a phrase such as 3-in-6 chance, put 1d6 here as a string.",
        "rollType": "below",
        "rollTarget": either the aforementioned percentage, or number given in "-out-of-6 chance", written as an integer,
        "blindroll": false,
        "tags": []
      },
      "ownership": {
        "default": 0
      },
    },
     END OF EXAMPLE
     SPECIAL INSTRUCTION: FOR EACH comma-delimited word/phrase in the table written next to |attacks= create an object, also inside this array
    {
      "_id": "replace with a different random 16 digit alphanumeric string for each object",
      "name": "The word/phrase (first word capitalized) as a string",
      "type": "weapon",
      "sort": 600000,
      "flags": {},
      "img": "icons/skills/melee/swords-parry-block-blue.webp",
      "effects": [],
      "folder": null,
      "system": {
        "description": "<p>The unformatted text describing the attack or factoid in the provided articles, but anything inside three single quotes should be wrapped in <strong> HTML tags. Anything wrapped in [[double brackets]] should receive a new ability object, but only if information about that factoid is available.</p><p>Separate thoughts into multiple paragraph tags.</p>",
        "quantity": {
          "value": 1,
          "max": 0
        },
        "weight": 0,
        "cost": 0,
        "containerId": "",
        "save": "",
        "equipped": false,
        "range": {
          "short": 0,
          "medium": 0,
          "long": 0
        },
        "pattern": "yellow",
        "damage": "if there is a notation such as 1d6+2 in parenthesis after the word/phrase, copy 1d6 here as a string. Otherwise leave it as an empty string",
        "bonus": if there is a notation such as 1d6+2 in parenthesis after the word/phrase, copy 2 here as an integer. If there isn't an integer number added, put 0 here",
        "tags": [],
        "slow": if the article says it's slow, put true here as a boolean, otherwise put false
        "missile": false,
        "melee": true,
        "counter": {
          "value": if there's a number and × before the word or phrase, copy that number here as an integer. Otherwise put 1 as an integer
          "max": use the same integer here as the value above
        }
      },
      "ownership": {
        "default": 0
      },
    },
    END OF EXAMPLE
  ],
  "effects": [],
  "folder": null,
  "system": {
    "retainer": {
      "enabled": false,
      "loyalty": 0,
      "wage": ""
    },
    "hp": {
      "hd": "a string such as \"1d8\" where 1 is replaced with the number in the article after |level=",
      "value": the average rolled hd value (xD8) rounded up as an integer,
      "max": the hp value determined above, again, as an integer
    },
    "ac": {
      "value":  number right after |AC= as an integer,
      "mod": 0
    },
    "details": {
      "biography": "The full description at the top of the article as a string, each paragraph wrapped in <p> HTML tags, and each portion inside three single quotes wrapped inside <strong> HTML tags, all as a string",
      "alignment": "if the number after |align= is positive, put \"Lawful\" here as a string. If it's negative, put \"Chaotic\" here as a string, otherwise put \"Neutral\" here as a string",
      "xp": "number after |experience= as an integer",",
      "treasure": {
        "table": "@UUID[Compendium.ose-advancedfantasytome.tables.RollTable.xeGURxYqgotXb68P]",
        "type": ""
      },
    },
    "encumbrance": {
      "value": null,
      "max": null
    },
    "config": {},
    "languages": {}
  },
}
"""