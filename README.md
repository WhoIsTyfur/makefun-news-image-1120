# Friday 20 November 2026 in one picture

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/WhoIsTyfur/makefun-news-image-1120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/WhoIsTyfur/makefun-news-image-1120/reward.svg)](https://make.fun/bounty/news-image-20261120)

An entry for the make.fun bounty
[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120).

## What it does

`main.py` writes one 1024 x 1024 PNG, `entry.png`, to the output folder: a single
front page of the world's news on Friday 20 November 2026. It shows the date as a
masthead, a UTC timeline of the day, three illustrated lead stories, ten
illustrated tiles, a numbered schematic world map, a column of one-line briefs and
a "date check" box naming the big stories left out because they broke before
20 November or are still to come.

The three leads are Russia's overnight barrage that hit three Kyiv bridges,
Cyclone Akvan's landfall near Gopalpur in eastern India, and the AI sell-off that
ran from Taiwan (-6.2%), Seoul and Tokyo to Wall Street, where the S&P 500 (-3.7%)
and the Dow fell into correction. Ten drawn tiles cover Russian missiles landing in
Poland, the UK-EU reset deals, COP31 running past its deadline, Nvidia's fall on a
reported SEC probe, Mexico's capture of "El Chapo Isidro", strikes on Yemen's
Hodeidah port, a tanker set ablaze near Hormuz, Xi and Albanese's "turnaround",
Vietnam's narrower death penalty and Italy's general strike; eighteen one-liners
add markets, politics, health, sport, film and space from every continent.

Every story was checked against at least two outlets and dated to 20 November
2026; the notes are in [`research/sources-2026-11-20.md`](research/sources-2026-11-20.md).
Stories that broke on 19 November or earlier (the Trump-Xi-Putin meeting, the
ICJ's Myanmar ruling, Anthropic's IPO debut, the 16-17 November Kyiv bridge strike)
are left out and named in the image's date-check box. Contested figures are
attributed ("Ukraine says", "Reuters report").

The picture is drawn ahead of time by [`art/draw.py`](art/draw.py) (Python +
Pillow, from the story list in [`art/stories.py`](art/stories.py)) and committed
as `art/entry.png`. The entry program only copies those bytes, so it needs no
network and both graded runs write the same file.

## How it is scored

The image goes before make.fun's AI judge, which compares entries two at a time
on: naming one day and showing that day's events; choosing the day's most
consequential stories across regions and fields; reading clearly with nothing
false or self-contradictory; reporting without hype; and clean craft that stays
legible at about 300 px across. Rank is by win rate over those pairwise games.

## Run it locally

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python main.py      # writes out/entry.png
python art/draw.py                          # redraws art/entry.png (needs Pillow, Windows fonts)
```
