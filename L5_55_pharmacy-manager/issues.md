# Static Code Analysis Issues — Pharmacy Manager

## Scope

This log records issues found while analysing `pharmacy_manager.py` with Pylint, Bandit, and Flake8. Severity is prioritised: high first, then medium, then lower-severity quality/style findings.

**Line-number note:** Line numbers can change as imports and functions are edited. The locations below identify the original code constructs so they can be found reliably; run `nl -ba pharmacy_manager_original.py` to obtain exact line numbers for the original snapshot before submission.

| **Issue** | **Type** | **Line(s)** | **Description** | **Fix Approach** |
| --------- | -------- | ----------- | --------------- | ---------------- |
| Unsafe `eval()` used to evaluate a formula | High — Bandit B307; security | Original formula-evaluation statement | `eval()` can execute arbitrary Python expressions if the input is not trusted. | Replace it with a restricted arithmetic evaluator that accepts only explicitly allowed AST nodes and numeric values. |
| Unsafe `pickle` serialization/deserialization for stock data | High — Bandit B301/B403; security | Original stock save/load functions and `pickle` import | Loading an untrusted pickle can execute code. The format is also unsuitable for safely exchanging editable stock data. | Replace pickle with JSON and validate the loaded structure and values before using them. |
| MD5 used to generate patient identifiers | High — Bandit B324; cryptography | Original patient-ID generation function | MD5 is not suitable for security-sensitive identifiers and does not provide a secret-key guarantee. | Use HMAC-SHA-256 with a secret supplied through an environment variable; keep the secret out of source control. |
| Hardcoded pharmacist password | High — Bandit B105; credentials | Original login function / password constant | A password embedded in source can be exposed through repository access and cannot be changed safely without editing code. | Read the demo password from an environment variable and document how to configure it. |
| `os.system()` used to print a label | Medium — Bandit B605; command execution | Original label-printing function | Shell invocation creates avoidable command-injection risk and depends on an external shell command. | Use Python output directly for the demonstration, or use a carefully parameterised subprocess call if external printing is required. |
| `random.randint()` used for a prescription number | Medium — Bandit B311; randomness | Original prescription-number generation function | The `random` module is not designed for security-sensitive or hard-to-predict values. | Use `secrets` for a less predictable demo identifier. If the number must be globally unique, use a persistent ID strategy instead. |
| Broad/bare exception handling | Medium — Bandit B110 and Pylint; error handling | Original exception handlers | Catching exceptions too broadly or silently ignoring them hides failures and makes debugging difficult. | Catch expected exception types, report actionable errors, and avoid silent `pass` behaviour. |
| Mutable default argument (`audit=[]`) | Low/medium — Pylint; correctness | Original function definition containing `audit=[]` | The same list object is reused across calls, so audit entries can leak between invocations. | Default to `None` and create a new list inside the function when no audit list is supplied. |
| Missing docstrings and non-standard function naming | Low — Pylint; maintainability | Multiple original functions and module header | Missing documentation and camelCase names reduce readability and cause style warnings. | Add module/function docstrings and use `snake_case` consistently. |
| Unused imports, long lines, and whitespace/newline violations | Low — Flake8/Pylint; style | Original imports and lines flagged by the tools | Unused imports add clutter; long lines and trailing whitespace make code harder to review and can fail style checks. | Remove unused imports, wrap long lines, and normalise whitespace and the final newline. |

## Fixes applied

The corrected program replaces unsafe expression evaluation with restricted arithmetic parsing, removes pickle in favour of JSON validation, replaces MD5 with HMAC-SHA-256, moves the demo password to an environment variable, avoids shell execution for label output, uses `secrets` for prescription-number generation, improves exception handling, fixes the mutable default, and addresses naming/documentation/style findings.

## Verification recorded

The final runs reported during the lab were:

- **Pylint:** 10.00/10.
- **Bandit:** 0 findings.
- **Flake8:** no violations (empty output).

The program was also run successfully after the changes. Keep the actual `reports/before/` and `reports/after/` tool outputs with this file as evidence. Re-run the tools on the exact submitted working tree if any code has changed since those reports were generated.
