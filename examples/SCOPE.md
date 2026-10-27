# Scope: CSV import validation

- Version: V1.0
- First created: 2026-10-27 15:00
- Updated: 2026-10-27 15:00

## Goal

Reject malformed customer CSV files before any row is persisted.

## Inputs / Outputs

- Input: a customer CSV file supplied through the existing import entry point.
- Input: the documented customer import schema.
- Input: representative valid and malformed CSV fixtures.
- Output: a validation result that identifies the rejected file or row and prevents partial persistence.
- Output: a persisted record only for a fully valid file.

## Must do

- Validate required columns, column order, and allowed value formats against the documented schema before persistence.
- Reject a file without writing any of its rows when validation fails.
- Return an error message that identifies the first failed validation rule.
- Preserve the existing import entry point and successful valid-file behavior.

## Won't do

- Redesigning the import interface.
- Adding new customer fields or changing the import schema.
- Migrating previously imported data.
- Adding retry queues, background processing, or performance tuning.
- Writing an ADR, implementation plan, ticket breakdown, or estimate.

## Acceptance

- A fixture with a missing required column returns a validation failure naming that column.
- A fixture with an invalid value format returns a validation failure naming the first failed rule.
- After either failed import, a query of the target data store returns zero rows from that file.
- A valid fixture still completes through the existing import entry point and persists every expected row.
- Automated tests cover one valid file and at least two malformed-file cases.
