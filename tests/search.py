from knigavuhe import Client

cl = Client()
r = cl.search_books('Агата Кристи')
print(r)
print(r[0])
