# Path 1 (N1) Literature Review

| File | What it is |
|---|---|
| `Path1_Literature_Synthesis.md` | The report. Part 1: six themes. Part 2: consensus (20 points) and debates (12). Part 3: research gaps and how N1 builds on them (G1–G15, M1–M6). Appendix A: paper key. Appendix B: detailed notes for every paper. |
| `papers.csv` | The 60 papers: id, group, year, authors, title, venue, PDF/page URL, which N1 item each one feeds, and why to read it |
| `papers/` | The 60 PDFs, named `ID_FirstauthorYear_FirstTitleWords.pdf` |
| `download.py` | Re-downloads any missing PDFs from `papers.csv`. Run: `python download.py`. Accepts `local:` paths for the faculty PDFs and checks each file's PDF header and trailer. |

**Groups:**
- A: PQ-TLS deployment (9)
- B: mobile-app TLS and finance apps (9)
- C: PQ-TLS cost (6)
- D: hybrid KEMs and protocol design (5)
- E: forward secrecy, HNDL, timelines (8)
- F: Shor estimates (13)
- G: Grover and cost accounting (7)
- H: migration, agility, notification (3)

**Note:** the report deliberately leaves out N1's private pilot finding, pending responsible disclosure (see `../N1_Field_Merge.md`).
