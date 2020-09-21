# list = [['1','a'],['1','b'],['1','c'],'2','2','2','3','3','3','4','4','4']
list2 = [['1','a'],['1','b'],['1','c']]
dir=dict()
for idx, item in enumerate(list2):
    print(type(item))

    if dir.get(item[0]):
        print(dir[item[0]])
        dir[item[0]].append(item[1])
    else:
        dir[item[0]]=[item[1]]

print(dir)
for item in dir:
    print(type(item))
    print(item)
    print(dir[item])