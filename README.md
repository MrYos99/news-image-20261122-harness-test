# news-image-20261122-harness-test

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/MrYos99/news-image-20261122-harness-test/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/MrYos99/news-image-20261122-harness-test/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A throwaway diagnostic probe, not the real entry. It asks the make.fun entry sandbox one empirical question: is Pillow importable here, and can it load a TrueType font shipped in the repository? The answer is painted into the image itself, so the harness reproduction carries the verdict: red means Pillow is missing, blue means Pillow works but the font does not load, green means both work. Every branch always writes a valid PNG and exits 0, so a missing library can never crash the probe. The result decides whether the real news-image entry can be rebuilt with real fonts and a graphics library instead of hand-drawn pixels.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
