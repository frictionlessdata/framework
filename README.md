# goodtables-py

[![Travis](https://img.shields.io/travis/frictionlessdata/goodtables-py/master.svg)](https://travis-ci.org/frictionlessdata/goodtables-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/goodtables-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/goodtables-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/goodtables.svg)](https://pypi.python.org/pypi/goodtables)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

Goodtables is a framework to inspect tabular data.

> Version v1.0 includes various important changes. Please read a [migration guide](#v10).

## Features

- tabular data inspection and validation
- general, structure and schema checks
- support for different input data presets
- support various source schemes and formats
- parallel computation for multitable datasets
- builtin command-line interface

## Getting Started

### Installation

The package use semantic versioning. It means that major versions  could include breaking changes. It's highly recommended to specify `tabulator` version range if you use `setup.py` or `requirements.txt` file e.g. `goodtables<2.0`.

```bash
$ pip install goodtables
$ pip install goodtables[ods] # With ods format support
```

### Example

Let's start with a simple example. We just run `validate` function against our data table. As a result we get a `goodtables` report.

```python
from goodtables import validate

report = validate('invalid.csv')
report['valid'] # false
report['table-count'] # 1
report['error-count'] # 3
report['tables'][0]['valid'] # false
report['tables'][0]['source'] # 'invalid.csv'
report['tables'][0]['errors'][0]['code'] # 'blank-header'
```

There is an [examples](https://github.com/frictionlessdata/goodtables-py/tree/master/examples) directory containing other code listings.

## Documentation

The whole public API of this package is described here and follows semantic versioning rules. Everyting outside of this readme are private API and could be changed without any notification on any new version.

### Validate

Goodtables validates your tabular dataset to find source, structure and schema errors. Consider you have a file named `invalid.csv`. Let's validate it:

```py
report = validate('invalid.csv')
```

Source could be not only a local file but also remote link, file-like object, inline data and even more. And it could be not only CSV but also XLS, XLSX, ODS, JSON and many more. Under the hood `goodtables` use powerfull [tabulator](https://github.com/frictionlessdata/goodtables-py) library. All schemes and formats supported by `tabulator` are supported by `goodtables`.

#### Dataset

With `goodtables` different tabular datasets could be validated. Tabular dataset is a something that could be split to list of data tables:

![Dataset](https://raw.githubusercontent.com/frictionlessdata/goodtables-py/master/data/dataset.png)

Below we will describe how different datasets could be validated. And even how to create cutom `presets` to validate your own kind of dataset. In our case we use `table` dataset which is default to validate `invalid.csv` file.

#### Report

As a result of validation goodtables returns a report dictionary. It includes valid flag, count of errors, list of reports per table including errors etc. Resulting report will be looking like this:

![Report](http://i.imgur.com/rEJG15g.png)

Report errors are standartised and described in [Data Quality Spec](https://github.com/frictionlessdata/data-quality-spec/blob/master/spec.json). All errors fails into three base categories:

- source - data can't be loaded or parsed
- structure - general tabular errors like duplicate headers
- schema - error of checks against [Table Schema](http://specs.frictionlessdata.io/table-schema/)

#### Presets



To work with different kind of datasets we use `preset` argument for `validate` function. As said by default we use `table` preset. Let's validate a [data package](http://specs.frictionlessdata.io/data-package/). As a result we get report of the same form but it will be having more that 1 table if there are more than 1 resource in data package:

```py
report = validate('datapackage.json', preset='datapackage')
```

To validate list of files we use `nested` preset. For nested preset first argument should be a list containing dictionaries with keys named after `validate` argument names. First argument is a `source` and we talk other arguments in next sections. Technically `goodtables` validates list of tables in parallel so it should be effective to do many tables validation in one run:

```py
report = validate([{'source': 'data1.csv'}, {'source': 'data2.csv'}], preset='nested')
```

#### Checks

Check is a main inspection actor in goodtables. Every check is associated with a Data Quality Spec error. List of checks could be customized using `checks` argument. Let's explore options on an example:

```python
report = validate('data.csv', checks='structure') # only structure checks
report = validate('data.csv', checks='schema') # only schema checks
report = validate('data.csv', checks={'bad-headers': False}) # exclude 'bad-headers'
report = validate('data.csv', checks={'bad-headers': True}) # check only 'bad-headers'
```

By default a datasource will be validated against all available Data Quality Spec errors. Some checks could be not avialable for validation e.g. if schema is not provided only `structure` checks will be done.

#### `validate(source, **options)`

- [Dataset:table]
- `source (path/url/dict/file-like)` - validation source containing data table
- `preset (str)` - source preset. Should be `table` for table validation (default).
- `schema (path/url/dict/file-like)` - Table Schema to validate data source against
- `headers (list/int)` - headers list or source row number containing headers. If number is given for plain source headers row and all rows before will be removed and for keyed source no rows will be removed.
- `scheme (str)` - source scheme with `file` as default. For the most cases scheme will be inferred from source. See [list of the supported schemes](https://github.com/frictionlessdata/tabulator-py#schemes).
- `format (str)` - source format with `None` (detect) as default. For the most cases format will be inferred from source. See [list of the supported formats](https://github.com/frictionlessdata/tabulator-py#formats).
- `encoding (str)` - source encoding with  `None` (detect) as default.
- `skip_rows (int/str[])` - list of rows to skip by row number or row comment. Example: `skip_rows=[1, 2, '#', '//']` - rows 1, 2 and all rows started with `#` and `//` will be skipped.
- `<name> (<type>)` - additional options supported by different schema and format. See [list of schema options](https://github.com/frictionlessdata/tabulator-py#schemes) and [list of format options](https://github.com/frictionlessdata/tabulator-py#schemes).
- [Dataset:datapackage]
- `source (path/url/dict/file-like)` - validation source containing data package descriptor
- `preset (str)` - source preset. Should be `datapackage` for Data Package validation.
- `<name> (<type>)` - options to pass to Data Package constructor
- [Dataset:nested]
- `source (dict[])` - list of dictionaries with keys named after source option names
- `preset (str)` - source preset. Should be `nested` for Data Package validation.
- [Settings]
- `checks (str/dict)` - checks configuration
- `infer_schema (bool)` - infer schema if not passed
- `infer_fields (bool)` - infer schema for columns not presented in schema
- `order_fields (bool)` - order source columns based on schema fields order
- `error_limit (int)` - error limit per table
- `table_limit (int)` - table limit for dataset
- `row_limit (int)` - row limit per table
- `custom_presets (callable[])` - list of custom presets
- `custom_checks (callable[])` - list of custom checks
- [Report]
- `(dict)` - returns a `goodtables` report

### Working with schema

If we run a simple table validation there will not be schema checks involved:

```py
report = validate('invalid.csv') # only structure checks
```

That's because there is no [Table Schema](http://specs.frictionlessdata.io/table-schema/) to check against. We have two options to fix it:
- provide `schema` argument containing Table Schema descriptor
- use `infer_schema` option to infer Table Schema from data source

Sometimes we have schema covering data table only partially e.g. table has headers `name, age, position` but schema has only `name` and `age` fields. In this case we use `infer_fields` option:

```py
# schema will be complemented by `position` field
report = validate('data.csv', schema='schema.json', infer_fields=True)
```

Other possible discrepancy situation when your schema fields have other order that data table columns. Options `order_fieds` is to rescue:

```py
# sync source/schema fields order
report = validate('data.csv', schema='schema.json', order_fields=True)
```

### Validation limits

If we need to save time/resources we could limit validation. By default limits have some reasonable values but it could be set to any values by user. Let's see on the available limits:
- errors per table limit
- tables per dataset limit
- rows per table limit

The most common cast is stopping on the first error found:

```py
report = validate('data.csv', error_limit=1)
```

### Custom presets

> It’s a provisional API. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

To create a custom preset user could use a `preset` decorator. This way the builtin preset could be overriden or could be added a custom preset.

```python
from tabulator import Stream
from tableschema import Schema
from goodtables import validate

@preset('custom-preset')
def custom_preset(source, **options):
    warnings = []
    tables = []
    for table in source:
        try:
            tables.append({
                'source':  str(source),
                'stream':  Stream(...),
                'schema': Schema(...),
                'extra': {...},
            })
        except Exception:
            warnings.append('Warning message')
    return warnings, tables

report = validate(source, preset='custom-preset', custom_presets=[custom_preset])
```

See builtin presets to learn more about the dataset extration protocol.

### Custom checks

> It’s a provisional API. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

To create a custom check user could use a `check` decorator. This way the builtin check could be overriden (use the spec error code like `duplicate-row`) or could be added a check for a custom error (use `type`, `context` and `after/before` arguments):

```python
from goodtables import validate, check

@check('custom-error', type='structure', context='body', after='blank-row')
def custom_check(errors, columns, row_number,  state=None):
    for column in columns:
        errors.append({
            'code': 'custom-error',
            'message': 'Custom error',
            'row-number': row_number,
            'column-number': column['number'],
        })
        columns.remove(column)

report = validate('data.csv', custom_checks=[custom_check])
```
See builtin checks to learn more about checking protocol.

### Inspector

> This API could be deprecated in the future. We reccomend to use `validate` counterpart.

#### `Inspector(**settings)`
#### `inspector.inspect(source, **source_options)`

### Spec

Data Quality Spec is shipped with the library:

```py
from goodtables import spec

spec['version'] # spec version
spec['errors'] # list of errors
```

#### `spec`

- `(dict)` - returns Data Quality Spec

### CLI

> It’s a provisional API. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

All common goodtables tasks could be done using a command-line interface (command per preset excluding `tables`). For example write a following command to the shell:

```
$ goodtables invalid.csv
```

And a report (the same as in the initial example) will be printed to the standard output in nicely-formatted way.

#### `$ goodtables`

```
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --json
  --error-limit INTEGER
  --table-limit INTEGER
  --row-limit INTEGER
  --infer-schema
  --infer-fields
  --order-fields
  --help                 Show this message and exit.

Commands:
  datapackage
  table
```

## Contributing

The project follows the [Open Knowledge International coding standards](https://github.com/okfn/coding-standards).

Recommended way to get started is to create and activate a project virtual environment.
To install package and development dependencies into active environment:

```
$ make install
```

To run tests with linting and coverage:

```bash
$ make test
```

For linting `pylama` configured in `pylama.ini` is used. On this stage it's already
installed into your environment and could be used separately with more fine-grained control
as described in documentation - https://pylama.readthedocs.io/en/latest/.

For example to sort results by error type:

```bash
$ pylama --sort <path>
```

For testing `tox` configured in `tox.ini` is used.
It's already installed into your environment and could be used separately with more fine-grained control as described in documentation - https://testrun.org/tox/latest/.

For example to check subset of tests against Python 2 environment with increased verbosity.
All positional arguments and options after `--` will be passed to `py.test`:

```bash
tox -e py27 -- -v tests/<path>
```

Under the hood `tox` uses `pytest` configured in `pytest.ini`, `coverage`
and `mock` packages. This packages are available only in tox envionments.

## Changelog

Here described only breaking and the most important changes. The full changelog could be found in nicely formatted [commit history](https://github.com/frictionlessdata/goodtables-py/commits/master).

### v1.0

This version includes various big changes. A migration guide is under development and will be published here.

### [v0.6](https://github.com/frictionlessdata/goodtables-py/releases/tag/0.6.0)

First version of `goodtables`.
