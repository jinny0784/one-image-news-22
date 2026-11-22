# One Image News — Sunday 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/jinny0784/one-image-news-22/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/jinny0784/one-image-news-22/reward.svg)](https://make.fun/bounty/news-image-20261122)

One image summing up the world's news of **Sunday 22 November 2026** — built
for make.fun's ["Sum up 22 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261122)
($100 in USDC).

## The image

A dense front page drawn from scratch: masthead, a big lead scene, then nine
region sections with 65 verified stories plus the lead — 66 items in all.

- **Lead — Gulf on fire:** three tankers hit in the Strait of Hormuz, a
  Bahraini industrial facility struck, Iran vowing to break the US blockade.
- **Europe:** COP31 collapses in Antalya — no climate deal as the EU rejects
  the weak draft; the longest COP on record.
- **Sport:** Verstappen wins the Las Vegas GP (Norris 2nd, Piastri 3rd, 35 lead
  changes); the ATP Finals final tonight: Alcaraz v Zverev.
- **Business:** Nasdaq's worst week since March 2020, $1.94 trillion wiped in
  a session; Nvidia −14% on an SEC probe report; Bitcoin's two-year low and
  rebound; BepiColombo enters Mercury's orbit after eight years.
- Plus South Asia / India, Middle East / West Asia, US / Americas, East Asia,
  Southeast Asia & Pacific, and Africa.

Every story is one verified event reported on 22 November 2026, with a short
label and a small drawn icon. No photographs, no copied artwork.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`). It creates the
output directory if needed, clears its contents entry by entry, and never
deletes the directory itself. Both runs write identical bytes.

## License

MIT — see [LICENSE](LICENSE).
