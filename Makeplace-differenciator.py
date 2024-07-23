import json

f = open('old.json', 'r', errors='ignore')
oldlist = (f.read())
f.close()
f = open('new.json', 'r', errors='ignore')
newlist = (f.read())
f.close()
oldjson = json.loads(oldlist)
newjson = json.loads(newlist)
def makelist(json, part):
    furniture1 = json[part]
    items = []
    for x in furniture1:
        items.append(x['name'])
    storage = items
    temp = []
    for x in items:
        t = storage.count(x)
        temp.append(x+': '+str(t))

    storage = list(dict.fromkeys(temp))
    storage.sort()
    return storage

listfurnold= makelist(oldjson, 'interiorFurniture')
listfurnnew = makelist(newjson, 'interiorFurniture')
listfixold = makelist(oldjson, 'interiorFixture')
listfixnew = makelist(newjson, 'interiorFixture')
listexfurnold = makelist(oldjson, 'exteriorFurniture')
listexfurnnew = makelist(newjson, 'exteriorFurniture')
listexfixold = makelist(oldjson, 'exteriorFixture')
listexfixnew = makelist(newjson, 'exteriorFixture')

list3 = []
debug = []
# Print statements included after every action for debug purposes. 
#print('Full lists of old items:\n\n'+str(oldlist)+'\n\n')
debug.append(('Full lists of old items:\n\n'+str(oldlist)+'\n\n'))
#print('Full list of new items:\n\n'+str(newlist)+ '\n')
debug.append(('Full list of new items:\n\n'+str(newlist)+ '\n'))
# Make a list which doesn't include any numbers
# Since all items separate name and number by a semicolon, that is used as a breakpoint.
# All things before the semicolon are selected to get the name, all things after the semicolon to get number
def getname(name):
    list = []
    for x in name:   
        place = x.find(':')
        list.append(x[:place])
    return list
# Make a list which doesn't include any letters.
def getnum(num):
    list = []
    for x in num:
        place = x.find(':')
        temp = x[place+1:]
        temp2 = temp.strip()
        list.append(int(temp2))
    return list

def findIdentical(old,new):
    tmp = []
    for x in new:
        if x in old:
            tmp.append(x)
    if tmp == []:
        return "Nothing"
    else:
        return(tmp)
print('\nOld item\n', listfurnold)


identOld = findIdentical(listfurnold,listfurnnew)
if listexfurnold == []:
    pass
else:
    identex = findIdentical(listexfurnold, listexfurnnew)



print('\nIdentical\n',identOld)
def findDifferent(ident,new):
    tmp = []
    for x in new:
        if x not in ident:
            tmp.append(x)
    return tmp
different = findDifferent(identOld,listfurnnew)
if listexfurnold == []:
    exdifferent = "empty"
else:
    exdifferent = findDifferent(identex, listexfurnnew)
print('\nDifferent\n',different)

def findUniqe(diff,old):
    namedifferent = getname(diff)
    nameold = getname(old)
    unique = []
    counter = 0
    for x in namedifferent:
        if x not in nameold:
            unique.append(diff[counter])
        counter += 1

    return unique

unique = findUniqe(different,listfurnold)
if listexfurnold == []:
    exunique = "empty"
else:
    exunique = findUniqe(exdifferent, listexfurnold)
print('\nUnique\n',unique)

def diffnum(diff,unique):
    tmp = []
    for x in diff:
        if x not in unique:
            tmp.append(x)
    return tmp

numberdiff = diffnum(different,unique)
if listexfurnold == []:
    exnumberdiff = "empty"
else:
    exnumberdiff = diffnum(exdifferent, exunique)
print('\nItems of different number to old: \n', numberdiff)

def stripOld(old,identical,failsafe):
    tmp = []
    counter = 0
    numold = getname(old)
    numident = getname(identical)
    fail = getname(failsafe)
    for x in numold:
        if x not in numident:
            if x in fail:
                tmp.append(old[counter])
        counter += 1
    return tmp
strippedold = stripOld(listfurnold,identOld,numberdiff)
if listexfurnold == []:
    exstrippedold = "empty"
else:
    exstrippedold = stripOld(listexfurnold, identex, exnumberdiff)
print('\nOld items that were added to: \n', strippedold)

def calcdiff(old,new):
    strippednames = getname(new)
    numberold = getnum(old)
    numbernew = getnum(new)
    newnumbers = []
    counter = 0
    for x in numbernew:
        tmp = x-numberold[counter]
        newnumbers.append(tmp)
        counter += 1
    counter = 0
    final = []
    for x in range(len(numberold)-1):
        tmp = strippednames[x] + ': ' + str(newnumbers[x])
        final.append(tmp)
    return final
itemadd = calcdiff(strippedold,numberdiff)
if listexfurnold == []:
    exitemadd = "empty"
else:
    exitemadd = calcdiff(exstrippedold, exnumberdiff)
print('\nNumber of each item to add\n', itemadd)

final = itemadd + unique
final.sort()
tmp = []
for x in final:
    tmp.append(x+'\n')
final = tmp
final.append('\nExterior furnishings:\n')
tmp = []
if listexfixold == []:
    pass
else:
    exfinal = exitemadd + exunique

if listexfurnold == []:
    if listexfurnnew != []:
        exfinal = listexfurnnew
        


if exfinal != []:
    for x in exfinal:
        tmp.append(x+'\n')
    tmp.sort()
    final = final + tmp

print('\n Full list: \n', final)


f = open('list.txt', 'w', errors='ignore')
for x in final:
    f.write(x)
f.close()

storage = newjson

def fixjson(old,file,unique, place):

    onlyname = getname(old)
    onlynumber = getnum(old)
    onlyunique = getname(unique)
    tmp = []
    counter = 0
    for x in onlyname:
        protect = onlynumber[counter]
        for entry in file[place]:
            if entry['name'] == x:
                if protect != 0:
                    protect -= 1
                    pass
                elif protect == 0:    
                    tmp.append(entry)
        counter +=1
    for x in onlyunique:
        for entry in file[place]:
            if entry['name'] == x:
                tmp.append(entry)
    file[place] = tmp

    return file

updatejson = fixjson(listfurnold,newjson,unique, 'interiorFurniture')
updatejson = fixjson(listexfurnold,newjson,exunique, 'exteriorFurniture')
list3 = makelist(updatejson,'interiorFurniture')

print('\nJson list\n', list3)
output = json.dumps(updatejson)

f = open('output.json', 'w', errors='ignore')
f.write(output)
f.close()
    
