# Dear Claude: Reality-Check Guidelines

**Purpose:** Ensure future sprint reviews and milestone write-ups reflect *delivered* functionality, not aspirational plans.

---

## 1. Ground Rules for All Reviews
1. **Run `git pull` & `ls -R` before writing.**  Verify the files you reference *actually exist* on the current branch.
2. **Quote commit hashes.**  Begin each review with `Repo state: main@<commit>` so everyone can cross-check.
3. **No Code ≠ No Claim.**  If a module isn’t in the tree, do not mention it as completed.
4. **Separate “Done” from “Planned.”**  Use two headings:
   - `Delivered This Sprint`
   - `Planned / In Progress`
5. **Metrics must be reproducible.**  Provide the command that generated any statistic (e.g., `pytest --cov` for coverage, `wc -l` for lines parsed).

## 2. How to Describe Missing Work
- State the gap plainly: “Extractor not yet implemented; will be delivered Sprint 6.”
- List blockers or dependencies, not imagined outputs.

## 3. Template Snippet (use this verbatim)
```markdown
# Sprint X Review – <concise title>
Repo state: main@<commit>

## Delivered This Sprint
- ✅ Item 1 (file path)
- ✅ Item 2 (file path)

## Planned / In Progress (Not Yet Merged)
- 🔄 Feature Y (branch spX-v2, PR #12)

## Metrics
| Metric | Value | Command |
|--------|-------|---------|
| Unit-test coverage | 78 % | `pytest --cov` |

## Next Steps
1. …
```

## 4. Immediate Action Items for Sprint-5 Review
- Rewrite `sprint-5-review.md` using the above template.
- Remove references to non-existent `src/` and `scripts/` directories.
- Replace fabricated rent values with `null` where data is missing.

Keeping reviews truthful builds trust and lets PMs make correct decisions—let’s stick to the facts.

*Prepared by PM – 2025-07-12* 