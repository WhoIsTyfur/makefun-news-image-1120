# PLACEHOLDER layout test content: replaced by researched stories.
MAST_SIZE = 84
TOPLINE = "31 STORIES · 7 REGIONS · EVERY ONE FROM FRIDAY 20 NOVEMBER 2026"
SUBLINE = "Placeholder subline one · placeholder two · placeholder three · four"
TIMELINE = [("00:00", "Event one"), ("02:30", "Event two"), ("05:30", "Event three"),
            ("09:00", "Event four"), ("13:00", "Event five"), ("16:00", "Event six"),
            ("21:00", "Event seven")]
LEADS = [
    dict(n=1, region="Europe", place="Kyiv, Ukraine · war", tag="KYIV", src_tag="Officials' count",
         ill=("kyiv",), head="Placeholder headline that runs to two lines",
         dek="Placeholder dek text that runs over two or three lines to test wrapping in the lead column here."),
    dict(n=2, region="Asia", place="Odisha, India · cyclone", tag="CYCLONE", src_tag="Weather office",
         ill=("cyclone",), head="Placeholder headline that runs to two lines",
         dek="Placeholder dek text that runs over two or three lines to test wrapping in the lead column here."),
    dict(n=3, region="Global", place="World · markets", tag="MARKETS", src_tag="Closing prices",
         ill=("markets", dict(rows=[("S&P 500", "-0.0%"), ("Nasdaq", "-0.0%"), ("Taiwan", "-0.0%"), ("Nikkei", "-0.0%")])),
         head="Placeholder headline that runs to two lines",
         dek="Placeholder dek text that runs over two or three lines to test wrapping in the lead column here."),
]
_ills = [("ukeu",), ("cop",), ("field_missile",), ("tanks",), ("crowd", dict(sign="STRIKE")),
         ("bars",), ("building",), ("derrick",), ("ballot",), ("cricket",)]
TILES = [dict(n=4 + i, region="Europe", place="Place · field", tag="TAG %d" % i, ill=_ills[i],
              head="Placeholder tile headline here", dek="Placeholder dek line.") for i in range(10)]
BRIEFS = [(14 + i, "Place", "placeholder one-line brief text", "Asia") for i in range(18)]
PINS = [(1, 30.5, 50.4, "Europe"), (2, 85, 20, "Asia"), (3, 121, 25, "Asia")]
DATE_CHECK = ("Placeholder date check text that runs over two lines to see how it wraps in the box at the "
              "bottom of the page, with enough words to reach a second line of text.")
FOOT_L = "Every story here happened, or was first reported, on Friday 20 November 2026."
FOOT_R = "Sources named beside each story · original drawings"
