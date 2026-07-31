---
title: "iSH Alpine environment crashes on Go binaries due to threading lock issue"
domain: "devops"
tags: ["ish", "alpine", "go", "cli"]
status: "published"
source: "0xSyStEm75928"
---

## Problem
Running Go-based CLI tools (like `gh` or `Hugo`) in iSH (x86 emulation on iOS) results in a runtime panic:
`fatal error: schedule: holding locks`
`fatal error: gcBgMarkWorker: mode not set`

## Root Cause
iSH emulates x86 architecture via system call translation. The Go runtime's scheduler and memory garbage collector rely on thread locking mechanisms that are not fully supported or compatible with iSH's emulated kernel context.

## Fix
Avoid Go-compiled binaries within iSH. Instead, replace them with Python/Node.js scripts or raw `curl` commands with URL encoding to interact with APIs.

Use Python with `urllib.parse.quote()` to query GitHub API instead of `gh`:

python3 search_issues_v2.py

## Verification
Executed `python3 search_issues_v2.py` in iSH. Successfully fetched JSON response from GitHub API and displayed target issues without triggering Go runtime panics.
