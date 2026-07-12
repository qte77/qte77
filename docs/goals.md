# Goals — the operating loop

How a strategic goal becomes *enforced, achieved, and traced* in the qte77 estate.
The **operational** companion to [operating-model.md](operating-model.md) (the design +
decision record) and [`kr-eval-gate.yml`](../.github/workflows/kr-eval-gate.yml) (the
enforcement).

## Who writes what

- **`goals.json` — humans only.** It holds strategic OKRs (the *intention*). Per the
  [task-tracking authority](../AGENTS.md), agents *read* goals; they do not author them.
- **The rails are agent-buildable** — the KR-issue template, the eval gate, the rollup.
  Humans set the destination; agents lay the track.

## The shape of `goals.json`

Kept intentionally minimal (see #67) — a documented example, *not* a formal schema:

```json
{
  "version": "0.1.0",
  "goals": [
    {
      "id": "G01",
      "objective": "<the qualitative aim>",
      "cynefin": "complicated",
      "key_results": [
        {
          "id": "G01-KR1",
          "statement": "<the measurable outcome>",
          "eval": "<pre-committed success test — metric target OR probe question>",
          "issue": 0,
          "status": "open"
        }
      ]
    }
  ]
}
```

## The loop (one goal, end to end)

1. **Author** (human) — add the goal + KRs to `goals.json`. Each KR carries an `eval:`
   written *before* any work (a metric target, or a probe question for Complex KRs).
2. **Open a KR Issue** per KR from the [`Goal KR` template](../.github/ISSUE_TEMPLATE/goal-kr.md)
   — it applies the `goal` label and carries the same `eval:` line. Record its number in
   the KR's `issue` field.
3. **Work** it via the normal execution engine; the PR says `Closes #<KR issue>`.
4. **Enforce** — [`kr-eval-gate.yml`](../.github/workflows/kr-eval-gate.yml) blocks the
   merge unless that KR Issue has a non-empty `eval:` (anti-goalpost-moving).
5. **Trace** — `goal_id` links KR → goal, and the campaign in `contributions.json`
   (polyforge#79), so goal → KR → PR → contribution is one chain.
6. **Track** — `python scripts/goal_rollup.py --write` regenerates
   [STATUS.md](../STATUS.md): per-goal KR completion + achievement %.
7. **Learn** — on close, the eval verdict → a learning (`AGENT_LEARNINGS.md` → rules).

## Current state

`goals.json` is empty by design until the first goal is authored — shown openly in
[STATUS.md](../STATUS.md). The rails are dormant-but-ready (like the gate): they light up
the moment a `goal`-labelled KR Issue exists.
