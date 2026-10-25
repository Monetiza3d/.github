# GitHub organization hardening

This document records organization settings that must be applied and verified in GitHub, separately from repository files. Repository defaults do not substitute for organization settings.

## Baseline

- Default repository permission: **Read**. Verified for `Monetiza3d` on 2026-10-25.
- New product repositories: **Private by default**; publish only after an explicit visibility and licensing review.
- Require 2FA for organization members after confirming all members and outside collaborators have 2FA enabled. Current observed state: **not enforced**; no members with 2FA disabled were returned on 2026-10-25.
- Set organization Actions default `GITHUB_TOKEN` permissions to **read-only**. Workflows may request narrowly scoped permission at job level.
- Restrict who can create repositories and use organization rulesets for default branch, pull request review, and required security checks when the GitHub plan supports them.
- Enable Dependabot alerts and security updates where available. For every public repository, enable private vulnerability reporting. Repository-specific CI remains the security baseline for private repositories.
- Keep audit logs and incident evidence within the retention provided by the selected GitHub plan; export additional evidence if the business requires longer retention.

## Current access limitation

The authenticated GitHub CLI account is an active organization admin, but its OAuth token currently has `read:org`, `repo`, and `workflow` scopes and lacks `admin:org`. The GitHub API refused organization Actions policy reads with HTTP 403. Therefore 2FA enforcement and organization-wide Actions/ruleset settings cannot be changed with this credential. Repository-level configuration is applied separately where the current token permits it.

Do not report an organization policy as enabled until the setting is read back from GitHub after applying it.
