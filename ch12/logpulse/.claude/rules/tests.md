---
paths:
  - "tests/**/*.py"
---

# Test rules

- Never change an existing assertion to make a failing test pass.
  If you believe a test is wrong, stop and explain why.
- New tests build their own small input with `tmp_path`; don't depend
  on the exact contents of `samples/` unless the test is about them.
- One behavior per test function; name it `test_<behavior>`.
