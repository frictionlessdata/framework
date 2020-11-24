# Working with HTML

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1KtQppS3abD6ea4I5kdY9Y5vBUf2zeCfz)



> Status: **STABLE**

Frictionless supports parsing HTML format


```bash
!pip install frictionless[html]
```


```bash
! wget -q -O table.html https://raw.githubusercontent.com/frictionlessdata/frictionless-py/master/data/table1.html
! cat table.html
```

    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <table>
            <tr>
                <td>id</td>
                <td>name</td>
            </tr>
            <tr>
                <td>1</td>
                <td>english</td>
            </tr>
            <tr>
                <td>2</td>
                <td>中国人</td>
            </tr>
        </table>
    </body>
    </html

## Reading HTML


You can this file format using `Package/Resource` or `Table` API, for example:


```python
from frictionless import Resource

resource = Resource(path='table.html')
print(resource.read_rows())
```

    [Row([('id', 1), ('name', 'english')]), Row([('id', 2), ('name', '中国人')])]


## Writing HTML

The same is actual for writing:


```python
from frictionless import Resource

resource = Resource(data=[['id', 'name'], [1, 'english'], [2, 'german']])
resource.write('table.new.html')
```




    'table.new.html'




```bash
!cat table.new.html
```

    <html><body><table>
    <tr><td>id</td><td>name</td></tr>
    <tr><td>1</td><td>english</td></tr>
    <tr><td>2</td><td>german</td></tr>
    </table></body></html>

## Configuring HTML

There is a dialect to configure HTML, for example:

```python
from frictionless import Resource
from frictionless.plugins.html import HtmlDialect

resource = Resource(path='table.html', dialect=HtmlDialect(selector='#id'))
print(resource.read_rows())
```

References:
- [HTML Dialect](https://frictionlessdata.io/tooling/python/formats-reference/#html)