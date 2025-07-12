# Repository Clean-Up & Hardening Checklist (Sprint 1)

> Goal: Keep the repo lightweight, professional, and ready for rapid feature-work without surprises when new contributors clone it.

## 1 ▪︎ Version-Control Hygiene

- **`.gitignore` in place** → added common patterns (`.DS_Store`, editor folders, Python cache, etc.).
- **Track binaries with Git LFS**  
  ```bash
  brew install git-lfs   # or use your OS-specific package manager
  git lfs install
  git lfs track "*.pdf"
  git add .gitattributes && git commit -m "Track PDFs with Git LFS"
  ```
  This keeps clone size small while preserving the actual lease files.
- **Squash early exploratory commits** (optional) using an interactive rebase before the repo gets public interest.

## 2 ▪︎ Directory Layout

| Current | Action | Rationale |
|---------|--------|-----------|
| `data/leases/` | Keep as is (but LFS-tracked) | Real-world test data for parsing/valuation engine. |
| `agile/` | Rename to `project-management/` | More intuitive for external collaborators. |
| `docs/` | Split into `docs/processes/`, `docs/templates/`, `docs/lease-samples/` | Clearer navigation. |
| `tools/` | Populate or remove stubs | Empty dirs can be confusing. |
| `suggestions/` | Central place for meta-suggestions like this one | Keeps proposal docs out of sprint artifacts. |

## 3 ▪︎ Documentation Basics

- **Beef up `README.md`** with: quick-start (clone → `poetry install`/`pip -r requirements.txt`), architecture diagram, and contribution guide.
- **Add `LICENSE`** (MIT / Apache-2.0 suggested) so others can legally reuse.
- **Create `CHANGELOG.md`** following Keep-a-Changelog spec for transparency.

## 4 ▪︎ Continuous Integration (CI)

- **GitHub Actions**: lint (`ruff`), unit tests (`pytest`), Sphinx docs build.
- **Pre-commit hooks**: enforce formatting (black, isort) and conventional commit messages.

## 5 ▪︎ Security & Secrets

- Confirm no API keys or credentials live in the repo; if any, rotate immediately and add them to `.gitignore`/`git-crypt`.

---

### Next Steps (Automatable)
1. Run the Git LFS commands above and commit `.gitattributes`.
2. Move/rename folders per table and update import paths (if any code exists).
3. Push `main` back to GitHub:
   ```bash
   git add -A
   git commit -m "Repo clean-up: ignore junk files, organise docs, enable Git LFS"
   git push origin main
   ```

*Feel free to break this into stories inside `agile/sprints/sprint-1-plan.md`.* 