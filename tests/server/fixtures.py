import json

name1 = "name1.txt"
name2 = "name2.txt"
name3 = "name3.json"
name4 = "name4.csv"
name5 = "table.csv"
bytes1 = b"bytes1"
bytes2 = b"bytes2"
bytes3 = b'{"key": "value"}'
bytes4 = b"id,name\n1,english\n2,spanish"
bytes5 = b"id,name\n1,english\n2,\xe4\xb8\xad\xe5\x9b\xbd\xe4\xba\xba\n"
folder1 = "folder1"
folder2 = "folder2"
data3 = json.loads(bytes3)
not_secure = ["/path", "../path", "../", "./"]
link = "https://raw.githubusercontent.com/fdtester/multiple-file-types/main"
