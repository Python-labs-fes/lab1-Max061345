phonebook = [
    ("Andrei Bondar", "+380671000001"),
    ("Andrei Bondar", "+380671000002"),
    ("Andrei Kovalenko", "+380671000003"),
    ("Andrei Kovalenko", "+380671000004"),
    ("Andrii Bondar", "+380671000005"),
    ("Andrii Bondar", "+380671000006"),
    ("Andrii Kovalenko", "+380671000007"),
    ("Andrii Kovalenko", "+380671000008"),
    ("Andriy Bondar", "+380671000009"),
    ("Andriy Bondar", "+380671000010"),
    ("Andriy Kovalenko", "+380671000011"),
    ("Andriy Kovalenko", "+380671000012"),
    ("Andrew Bondar", "+380671000013"),
    ("Andrew Bondar", "+380671000014"),
    ("Andrew Kovalenko", "+380671000015"),
    ("Andrew Kovalenko", "+380671000016"),
    ("Anna Bondar", "+380671000017"),
    ("Anna Bondar", "+380671000018"),
    ("Anna Kovalenko", "+380671000019"),
    ("Anna Kovalenko", "+380671000020"),
    ("Anna Melnyk", "+380671000021"),
    ("Anna Melnyk", "+380671000022"),
    ("Artem Bondar", "+380671000023"),
    ("Artem Bondar", "+380671000024"),
    ("Artem Kovalenko", "+380671000025"),
    ("Artem Kovalenko", "+380671000026"),
    ("Bohdan Bondar", "+380671000027"),
    ("Bohdan Bondar", "+380671000028"),
    ("Bohdan Kovalenko", "+380671000029"),
    ("Bohdan Kovalenko", "+380671000030"),
    ("Dmytro Bondar", "+380671000031"),
    ("Dmytro Bondar", "+380671000032"),
    ("Dmytro Kovalenko", "+380671000033"),
    ("Dmytro Kovalenko", "+380671000034"),
    ("Ihor Bondar", "+380671000035"),
    ("Ihor Bondar", "+380671000036"),
    ("Ihor Kovalenko", "+380671000037"),
    ("Ihor Kovalenko", "+380671000038"),
    ("Ivan Bondar", "+380671000039"),
    ("Ivan Bondar", "+380671000040"),
    ("Ivan Kovalenko", "+380671000041"),
    ("Ivan Kovalenko", "+380671000042"),
    ("Kateryna Melnyk", "+380671000043"),
    ("Kateryna Melnyk", "+380671000044"),
    ("Maksym Bondar", "+380671000045"),
    ("Maksym Bondar", "+380671000046"),
    ("Maksym Kovalenko", "+380671000047"),
    ("Maksym Kovalenko", "+380671000048"),
    ("Oksana Bondar", "+380671000049"),
    ("Oksana Bondar", "+380671000050"),
    ("Oksana Kovalenko", "+380671000051"),
    ("Oksana Kovalenko", "+380671000052"),
    ("Roman Bondar", "+380671000053"),
    ("Roman Bondar", "+380671000054"),
    ("Roman Kovalenko", "+380671000055"),
    ("Roman Kovalenko", "+380671000056"),
    ("Yulia Bondar", "+380671000057"),
    ("Yulia Bondar", "+380671000058"),
    ("Yulia Kovalenko", "+380671000059"),
    ("Yulia Kovalenko", "+380671000060"),
]


phonebook_sorted = sorted(phonebook, key=lambda x: x[0])

res_list = []

def findString(arr, x):
    
    l = 0
    r = len(arr) - 1

    while l <= r:

        m = l + (r - l) // 2

        if arr[m][0] == x:
            new_item = x + ": " + arr[m][1]
            res_list.append(new_item)
            b = m
            f = m
            while arr[b - 1][0] == x:
                b_item = x + ": " + arr[b - 1][1]
                res_list.append(b_item)
                b -= 1
            while arr[f + 1][0] == x:
                f_item = x + ": " + arr[f + 1][1]
                res_list.append(f_item)
                f += 1
        
        if arr[m][0] < x:
            l = m + 1
        
        else:
            r = m - 1

    return -1

x = "Andrew Bondar"
findString(phonebook_sorted, x)
for i in res_list:
    print(i)