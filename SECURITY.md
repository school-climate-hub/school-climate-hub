# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability in School Climate Hub, please report it
privately. **Do not open a public GitHub issue.**

Email **reza@beaconhouse.tech** with:

- A description of the vulnerability and its potential impact
- Steps to reproduce
- Any relevant logs, URLs, or proof-of-concept (without exposing real user data)

We aim to acknowledge reports within **3 business days** and to provide a remediation
timeline after triage. Please allow us reasonable time to investigate and fix the issue
before any public disclosure.

## Scope

In scope:

- The operator console and public site (`schoolclimatehub.org`)
- The Cloudflare Worker chat backend (`worker/`)
- The data ingestion and scoring pipeline (`ingestion/`, `scoring/`)
- The published open dataset (`scores.json`, `schools.json`, exports)

## Data handling

This project holds **no parent or child PII**. School-level operational data is
anonymised by default. If a report involves potential exposure of any sensitive data,
please flag it explicitly so we can prioritise it.
