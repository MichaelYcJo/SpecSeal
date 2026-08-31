"""The eval suite has never run (early access), so its shape is what CI can check.

An eval that is malformed fails at the moment someone finally enables the
feature — which is the worst moment to discover it. These assertions cost
nothing and hold the suite to the layout `claude plugin eval` expects.
"""

import glob
import os

EVALS = os.path.join(os.path.dirname(__file__), "..", "evals")

REQUIRED = ("schema_version", "name", "runs", "max_turns", "timeout_seconds", "model")


def case_dirs():
    return sorted(d for d in glob.glob(os.path.join(EVALS, "*")) if os.path.isdir(d))


def top_level_keys(path):
    """`key:` at column zero — enough to check presence without a YAML dep."""
    keys = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line[:1].isalpha() and ":" in line:
                keys.append(line.split(":", 1)[0].strip())
    return keys


def test_every_case_declares_a_case_yaml_and_a_prompt():
    missing = []
    for d in case_dirs():
        for name in ("case.yaml", "prompt.md"):
            if not os.path.isfile(os.path.join(d, name)):
                missing.append(f"{os.path.basename(d)}/{name}")
    assert not missing, missing


def test_every_case_yaml_carries_the_required_fields():
    gaps = []
    for d in case_dirs():
        path = os.path.join(d, "case.yaml")
        if not os.path.isfile(path):
            continue
        keys = top_level_keys(path)
        for field in REQUIRED:
            if field not in keys:
                gaps.append(f"{os.path.basename(d)}: {field}")
    assert not gaps, gaps


def test_the_prompt_holds_the_prompt_and_nothing_else():
    """Config lives in case.yaml. One case kept its config in the prompt's
    frontmatter, where the runner does not look for it."""
    offenders = [
        os.path.basename(d)
        for d in case_dirs()
        if open(os.path.join(d, "prompt.md"), encoding="utf-8").read().startswith("---")
    ]
    assert not offenders, offenders


def test_every_case_has_at_least_one_grader():
    empty = [
        os.path.basename(d)
        for d in case_dirs()
        if not glob.glob(os.path.join(d, "graders", "*.md"))
    ]
    assert not empty, empty


def test_the_readme_names_every_case():
    with open(os.path.join(EVALS, "README.md"), encoding="utf-8") as f:
        readme = f.read()
    unlisted = [
        os.path.basename(d) for d in case_dirs() if os.path.basename(d) not in readme
    ]
    assert not unlisted, unlisted
