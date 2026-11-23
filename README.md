# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/novia2698/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/novia2698/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up Monday 23 November 2026: six illustrated front-page stories — the Russian cargo ship burning off Finland after a drone attack, 14 missing after a Russian drone hit a home in the Kyiv region, the COP31 climate talks collapsing with no fossil-fuel deal, the ICJ ruling Myanmar committed genocide against the Rohingya, the Indonesia factory fire with dozens missing, and South Korea's education minister resigning over an AI exam-cheating scandal — plus an "also today" ticker. `main.py` copies the pre-rendered `entry.png` to the output directory; the page itself is rendered at build time by `render_news.py`.

## Run it

```sh
python3 main.py
```

Set `MAKEFUN_OUTPUT_DIR` to choose where `entry.png` lands (default `/output`).

To re-render the front page from scratch (needs Pillow on the builder machine):

```sh
python3 render_news.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=bpr1tvsc&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
