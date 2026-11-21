# Variant "fewer, bigger": the same leads and tiles as stories.py plus five more
# drawn tiles in place of the one-line list.  Render with STORIES=stories_big.
from stories import (MAST_SIZE, SUBLINE, TIMELINE, LEADS, TILES as _TILES,  # noqa: F401
                     DATE_CHECK, FOOT_L, FOOT_R, COLORS)

LAYOUT = "big"
TOPLINE = "18 STORIES · 7 REGIONS · EVERY ONE FROM FRIDAY 20 NOVEMBER 2026"

TILES = list(_TILES) + [
    dict(n=14, region="Europe", place="Frankfurt · markets", tag="EUROPE: STOCKS", cap="STOXX 600 −2.0%",
         ill=("bars", dict(up=False)), head="European shares end worst week since March",
         dek="ASML falls 8.7% in tech rout."),
    dict(n=15, region="Asia", place="Tokyo · economy", tag="JAPAN: PRICES", cap="Core CPI 2.2%",
         ill=("bars", dict(up=True)), head="Japan's core inflation rises to 2.2%",
         dek="Up from 2.1% in September."),
    dict(n=16, region="Africa", place="DR Congo · health", tag="EBOLA", cap="WHO update",
         ill=("virus",), head="WHO: Congo Ebola cases pass 11,600",
         dek="5,678 deaths; still an emergency."),
    dict(n=17, region="Asia", place="Rawalpindi · cricket", tag="PAKISTAN WIN", cap="Won by 8 wickets",
         ill=("cricket",), head="Pakistan beat Sri Lanka to take series",
         dek="First Test series win in 2 years."),
    dict(n=18, region="Americas", place="Washington · tech", tag="DATA CENTRES", cap="No rate given",
         ill=("building",), head="Trump threatens tax on offshore data centres",
         dek="Alphabet, Amazon shares slip."),
]

SHORT = {
    4: ("Russian missiles land in Poland", "No one hurt, Poland says."),
    5: ("UK and EU sign “reset” deals", "Food, carbon, youth visas."),
    6: ("COP31 misses deadline, no deal", "Split over fossil fuels."),
    7: ("Nvidia falls 14% on SEC report", "Reuters: SEC eyes accounts."),
    8: ("Mexico seizes FBI-wanted capo", "“El Chapo Isidro” held."),
    9: ("Coalition strikes Yemen port", "Houthis threaten Saudi ports."),
    10: ("Tanker set ablaze off Oman", "No casualties, UKMTO says."),
    11: ("Xi hails Australia “turnaround”", "Meets Albanese in Shenzhen."),
    12: ("Vietnam curbs death penalty", "Drug trafficking dropped."),
    13: ("Italy holds general strike", "Rallies in 100+ cities."),
    14: ("European stocks slide 2%", "Worst week since March."),
    15: ("Japan core inflation hits 2.2%", "Up from 2.1% in September."),
    16: ("Congo Ebola cases pass 11,600", "WHO update; 5,678 deaths."),
    17: ("Pakistan beat Sri Lanka 1-0", "First Test series win in 2 years."),
    18: ("Trump threatens data-centre tax", "Aimed at sites abroad."),
}
TILES = [dict(t, head=SHORT[t["n"]][0], dek=SHORT[t["n"]][1]) for t in TILES]
