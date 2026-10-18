# septic-contractor-crm-texas

A small command-line CRM for septic and excavation contractors. Single Python file. JSON store on disk. No database, no server, no account. Pre-loaded with the 7-county service territory for Out West Septic.

The CRM tracks leads through the sales pipeline: lead, contacted, quoted, hired, done, lost. You can search, filter, update, and export. The whole thing is under 300 lines of Python.

## Install

No install. Stdlib only.

```
git clone https://github.com/TexasSepticEnthusiast/septic-contractor-crm-texas
cd septic-contractor-crm-texas
python crm.py --help
```

## Usage

Add a customer:

```
python crm.py add "Jane Doe" "940-555-0123" \
    --county "Palo Pinto" \
    --service "New conventional install" \
    --notes "3 bed, 2 bath, vacant lot, near Mineral Wells"
```

List everyone:

```
python crm.py list
```

Filter by county and status:

```
python crm.py list --county "Palo Pinto" --status lead
```

Show full details:

```
python crm.py show <id>
```

Update a customer (status, notes, anything):

```
python crm.py update <id> --status quoted --notes "Sent estimate 2026-10-15"
```

Search across name, phone, address, notes:

```
python crm.py search "perc"
```

Export:

```
python crm.py export --format csv --output leads.csv
python crm.py export --format json --output backup.json
```

Stats by status and county:

```
python crm.py stats
```

Delete:

```
python crm.py delete <id>
```

## Where the data lives

The default store file is `./crm_store.json` in the current directory. Override with `--store /path/to/file.json` or set the `OWS_CRM_STORE` environment variable.

The store is a JSON file. You can back it up, copy it to another machine, or version-control it. The format is human-readable.

## Service territory

The CRM is pre-loaded with the 7 counties Out West Septic serves: Palo Pinto, Hood, Erath, Stephens, Young, Jack, Eastland. The `add` and `update` commands accept a `--county` argument and validate against the list. Other counties are accepted as a warning.

To use the CRM for a different territory, edit `VALID_COUNTIES` at the top of `crm.py`.

## Pipeline statuses

| Status | Meaning |
| --- | --- |
| lead | First contact. Hasn't been called back yet. |
| contacted | Called, left message, awaiting reply. |
| quoted | Estimate sent. |
| hired | Contract signed, work scheduled. |
| done | Work complete, paid. |
| lost | Went elsewhere, or no longer needs the work. |

The statuses are simple. No automation. Move customers through the pipeline by running `update --status`.

## Running the tests

```
python -m unittest test_crm.py -v
```

Tests cover the store, the search/filter, and the CLI subcommands.

## What's not here

- No web UI. The CRM is a CLI. If you want a UI, point a simple HTML form at the JSON file or wrap the commands in a web service.
- No multi-user support. The JSON file is the source of truth. Two people editing at once is a problem.
- No reminders. The CRM doesn't email you or send notifications. You have to look at it.
- No quoting. The CRM tracks leads, not estimates. For estimates, use a spreadsheet or the cost-estimator in the texas-septic-toolkit.

## License

MIT. See `LICENSE`.
