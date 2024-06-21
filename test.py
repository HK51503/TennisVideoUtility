list = ["s1", "s2", "d1", "d2"]
for i in range(len(list)):
    value = list[i]
    if value[0] == "s":
        print("singles:" + value)
    else:
        print("doubles:" + value)