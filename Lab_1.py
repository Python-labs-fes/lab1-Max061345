alphabet:list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
new_list:list = []
base:int = 7

text:str = "welcome2python3intro"

base = base % len(alphabet)


new_text:str = ""

while (base <= 35):    
    for i in range (0, len(text)):
        index = alphabet.index(text[i])
        if (index + base) > (len(alphabet) - 1):
            index = (index + base) - len(alphabet)
            new_text += alphabet[index]
        else:
            new_text += alphabet[index + base]                
        if len(new_text) == len(text):
            new_list.append(new_text)
            new_text = ""
            base += 1
                

print(new_list)



new_list_2:list = []


while (base <= 35):    
    for i in new_list:
        for letter in range(0, len(i)):
            for item in alphabet:
                if i[letter] == item:
                    index:int = alphabet.index(item)                    
                    new_text += alphabet[index - base]
                    if len(new_text) == len(i):
                        new_list_2.append(new_text)
                        new_text = ""
                        base += 1
                    

print(new_list_2)


key_string:str = "3noypth"

if " " in key_string:
    key_string = key_string.replace(" ", "")
print(key_string)


if key_string in new_list:
    print("list contains key string")
else:
    print("list doesn't contain key string")