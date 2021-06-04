import Repcheck as Rep


list = [{'n': 'apple'}, {'n': 'banana'}, {'n': 'cow'}, {'n': 'donkey'},]
def listy():

    listo = [{'n': 'apple'}, {'n': 'banana'}, {'n': 'cow'}, {'n': 'donkey'}, {'n': 'elephant'}]

    for key in listo:
        # Number = n
        # n = n + 1
        # list.append({'Number': Number})
        [(i,) + item for i, item in enumerate(dict.items(), 1)]


    print(list)

# ID for items in dictionary
# [(i,) + item for i, item in enumerate(dict.items(), 1)]


#for key in list:
    #Rep.dict_read()
    # Rep.dict_update(Rep.Inputs)
    # Rep.reno = Rep.reno + 1
