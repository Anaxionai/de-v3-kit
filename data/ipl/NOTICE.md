# Notice: Cricsheet match data

Every IPL file in this folder comes from Cricsheet's ball-by-ball match data:

- `season.csv` and `season-published.csv` are built from Cricsheet's IPL match files. They are a derived database: the kit chose one season and turned its match files into one row per delivery (`README.md` names the season and the columns). `season-published.csv` also repeats some rows on purpose, for the Launchpad task "catch a wrong number". Its wrong totals are the kit's doing, not Cricsheet's.
- `get_matches.py` downloads Cricsheet's own files to your laptop. The kit does not host them.

## Credit line

Use this line wherever you publish data, results or charts made from these files, for example in a README on GitHub:

```text
Match data from Cricsheet (https://cricsheet.org/), licensed under the Open Data Commons Attribution License 1.0 (https://opendatacommons.org/licenses/by/1-0/).
```

## The licence

Cricsheet publishes its JSON match data under the **Open Data Commons Attribution License 1.0 (ODC-By 1.0)**: https://opendatacommons.org/licenses/by/1-0/
(Cricsheet's licensing page: https://cricsheet.org/licensing/. Only Cricsheet's XML match data uses a different licence, CC BY 4.0, and the course does not use it.)

The licence allows copying, sharing and changing the data, also in a paid course, on these conditions:

- **When you share the data or a database made from it** (section 4.2), share it under the same licence, include the licence or its address, and keep this notice and any other notice that refers to the licence. This file is that notice for the kit's season files.
- **When you publish something made from the data** (section 4.3), such as a chart, a table of results or a report, add a notice that says the content came from Cricsheet and is available under ODC-By. The credit line above does this. The licence's own example is: "Contains information from Cricsheet (https://cricsheet.org/) which is made available under the ODC Attribution License (https://opendatacommons.org/licenses/by/1-0/)."

Every download made with `get_matches.py` also holds Cricsheet's `README.txt` and the full licence text in `LICENSE.txt`.

Cricsheet is not connected with this course and does not endorse it.
