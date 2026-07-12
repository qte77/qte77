---
name: Goal KR (eval-gated)
about: A Key Result under a goals.json goal. The eval MUST be written before the work — kr-eval-gate.yml enforces it.
title: "[G0x-KRy] "
labels: goal
---

<!--
This issue is a Key Result under a goals.json goal.
The `eval:` line below is a PRE-COMMITMENT: write the success test BEFORE any agent
touches the work, and do not weaken it afterwards. kr-eval-gate.yml blocks a closing
PR if this issue has no non-empty `eval:` line.
See docs/goals.md and docs/operating-model.md. Leave `eval:` filled, not empty.
-->

goal_id: G0x

**Key result:** <the measurable outcome this KR delivers>

eval:

**Cynefin:** clear | complicated | complex | chaotic
