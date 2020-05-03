from app.GraphBuilder import service
from app.GraphBuilder import serviceTree
import json

s = service("123", "My service", "")

s.addServer("1", "Server1")
s.addServer("2", "Server2")
s.addServer("3", "Server3")

# print(s.getService())

with open('data/datastructure.json') as f:
    data = json.load(f)
    st = serviceTree('', '', '')
    st.loadFromJSON(data)

print(st.getServiceTreeAsJSON())
