# Working with Google Sheets

> Status: **EXPERIMENTAL**

Frictionless supports parsing Google Sheets data as a file format.

```sh
!pip install frictionless[gsheets]
```


## Reading from Google Sheets

You can read from Google Sheets using `Package/Resource` or `Table` API, for example:


```python
from frictionless import Resource

resource = Resource(path='https://docs.google.com/spreadsheets/d/1mHIWnDvW9cALRMq9OdNfRwjAthCUFUOACPp0Lkyl7b4/edit?usp=sharing')
print(resource.read_rows())
```

    [Row([('id', 1), ('name', 'english')]), Row([('id', 2), ('name', '中国人')])]


## Writing to Google Sheets

The same is actual for writing:

```py
from frictionless import Resource

resource = Resource(path='data/table.csv')
resource.write("https://docs.google.com/spreadsheets/d/<id>/edit", dialect={"credentials": ".google.json"})
```


## Configuring Google Sheets

There is a dialect to configure how Frictionless read and write files in this format. For example:

```py
from frictionless import Resource

resource = Resource(path='data/table.csv')
resource.write("https://docs.google.com/spreadsheets/d/<id>/edit", dialect={"credentials": ".google.json"})
```
