# Story list for the 20 November 2026 page. Every item is in
# research/sources-2026-11-20.md with two or more dated sources.
MAST_SIZE = 84
TOPLINE = "31 STORIES · 7 REGIONS · EVERY ONE FROM FRIDAY 20 NOVEMBER 2026"
SUBLINE = ("Russia hits Kyiv's bridges · Cyclone Akvan strikes India · "
           "AI rout sinks Wall Street · UK and EU sign deals")
COLORS = 256

TIMELINE = [
    ("Night", "Kyiv barrage"),
    ("02:30", "Akvan landfall"),
    ("05:30", "Taiwan ends −6.2%"),
    ("07:00", "UK retail +0.7%"),
    ("16:30", "Europe stocks −2%"),
    ("21:00", "S&P 500 ends −3.7%"),
    ("Late", "COP31 overtime"),
]

LEADS = [
    dict(n=1, region="Europe", place="Kyiv, Ukraine · war", tag="KYIV", src_tag="Ukraine's count",
         ill=("kyiv",),
         head="Russian barrage hits three Kyiv bridges",
         dek="Kyiv says about 110 missiles and 400 drones were fired; at least 8 killed, "
             "power cut in 11 regions. Moscow calls it retaliation."),
    dict(n=2, region="Asia", place="Odisha, India · cyclone", tag="CYCLONE AKVAN", src_tag="India weather office",
         ill=("cyclone",),
         head="Cyclone Akvan comes ashore in eastern India",
         dek="Crossed near Gopalpur at 02:00–03:00 UTC with 70–80 km/h winds. "
             "Over 300,000 moved to shelters; no deaths reported."),
    dict(n=3, region="Global", place="Taipei · Tokyo · New York", tag="AI SELL-OFF", src_tag="Closing prices",
         ill=("markets", dict(title="FRIDAY'S CLOSE", rows=[
             ("Taiwan", "−6.2%"), ("Seoul", "−5.2%"), ("Tokyo", "−5.1%"),
             ("Nasdaq", "−5.3%"), ("S&P 500", "−3.7%")])),
         head="AI rout drives Wall Street into correction",
         dek="Nasdaq wipes out its 2026 gain; Taiwan caps its worst week since 1991; "
             "Nvidia sinks 14%."),
]

TILES = [
    dict(n=4, region="Europe", place="SE Poland · NATO", tag="POLAND: MISSILES", ill=("field_missile",),
         head="Russian missiles land inside Poland", dek="No one hurt, Poland says."),
    dict(n=5, region="Europe", place="Brussels · trade", tag="UK–EU DEAL", ill=("ukeu",),
         head="UK and EU sign Brexit “reset” deals", dek="Food, carbon, youth visas."),
    dict(n=6, region="Middle East", place="Antalya · climate", tag="COP31: NO DEAL", ill=("cop",),
         head="COP31 misses its deadline, no deal", dek="Split over fossil-fuel wording."),
    dict(n=7, region="Americas", place="New York · tech", tag="NVIDIA −14%", ill=("chip",),
         head="Nvidia sinks on SEC accounting report", dek="Reuters report; no comment yet."),
    dict(n=8, region="Americas", place="Sinaloa · crime", tag="MEXICO: ARREST", ill=("flag_mx",),
         head="Mexico captures FBI most-wanted capo", dek="“El Chapo Isidro” is held."),
    dict(n=9, region="Middle East", place="Hodeidah · Yemen", tag="YEMEN: STRIKES", ill=("port_strike",),
         head="Saudi-led coalition hits Yemen port", dek="Houthis threaten Saudi ports."),
    dict(n=10, region="Middle East", place="Off Oman · shipping", tag="HORMUZ: TANKER", ill=("ship_fire",),
         head="Tanker hit and set ablaze near Hormuz", dek="UKMTO: no casualties reported."),
    dict(n=11, region="Global", place="Science · AI", tag="MATHS: CLAIM", ill=("board",),
         head="AI-aided Riemann proof claimed", dek="Experts are still checking it."),
    dict(n=12, region="Asia", place="Hanoi · justice", tag="VIETNAM: LAW", ill=("gavel",),
         head="Vietnam drops death penalty for drugs", dek="Capital crimes cut from 10 to 4."),
    dict(n=13, region="Europe", place="Italy · labour", tag="ITALY: STRIKE", ill=("crowd", dict(sign="SCIOPERO")),
         head="General strike and protests in Europe", dek="Rallies in 100+ Italian cities."),
]

# (number, place, text, region) — one line each
BRIEFS = [
    (14, "Europe", "STOXX 600 has worst week since March", "Europe"),
    (15, "London", "UK retail sales up 0.7% in October", "Europe"),
    (16, "Paris", "France puts Boone forward for ECB board", "Europe"),
    (17, "Munich", "Bayern held 1-1 by Köln; Kane hurt", "Europe"),
    (18, "Israel", "Eisenkot sets out 3 paths to a government", "Middle East"),
    (19, "Iran", "IRGC says Hormuz stays shut for now", "Middle East"),
    (20, "Pretoria", "Police: 581 women killed in 3 months", "Africa"),
    (21, "Congo", "WHO: Ebola cases pass 11,600", "Africa"),
    (22, "Shenzhen", "Xi hails “turnaround” with Australia", "Oceania"),
    (23, "Tokyo", "Japan core inflation rises to 2.2%", "Asia"),
    (24, "Shenzhen", "Singapore, China open trade-pact talks", "Asia"),
    (25, "Bangkok", "Gen Z rally tells PM Anutin to quit", "Asia"),
    (26, "Rawalpindi", "Pakistan beat Sri Lanka, win series", "Asia"),
    (27, "New York", "Pannun plotter jailed for 19 years", "Americas"),
    (28, "Washington", "Trump threatens offshore data-centre tax", "Americas"),
    (29, "Wall St", "Anthropic shares fall ~9% on day two", "Americas"),
    (30, "Washington", "Report: Hegseth memo limits Canada ties", "Americas"),
    (31, "Crypto", "Bitcoin falls below $60,000", "Global"),
]

# map pins: (number, lon, lat, region)
PINS = [
    (1, 30.5, 50.4, "Europe"), (2, 84.9, 19.3, "Asia"), (3, 121.5, 25.0, "Global"),
    (4, 23.0, 51.0, "Europe"), (5, 4.4, 50.8, "Europe"), (6, 30.7, 36.9, "Middle East"),
    (7, -74.0, 40.7, "Americas"), (8, -108.5, 25.6, "Americas"), (9, 42.9, 14.8, "Middle East"),
    (10, 56.2, 26.2, "Middle East"), (12, 105.8, 21.0, "Asia"), (13, 12.5, 41.9, "Europe"),
    (20, 28.2, -25.7, "Africa"), (21, 23.6, -2.9, "Africa"), (22, 151.2, -33.9, "Oceania"),
]

DATE_CHECK = ("Left out because they broke on 19 November or earlier: the Trump–Xi–Putin meeting in "
              "Shenzhen, the ICJ's Myanmar genocide ruling, Anthropic's IPO debut and the 16–17 Nov strike "
              "on Kyiv's bridges. Not yet decided: COP31's final text.")
FOOT_L = "Every story here happened, or was first reported, on Friday 20 November 2026."
FOOT_R = "Contested claims are attributed · original drawings"
