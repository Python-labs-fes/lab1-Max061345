alphabet:list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
new_list:list = []
base:int = 3

text:str = "fw668i12ts00t3amwezr"

base = base % len(alphabet)

new_text = ''
new_list_2:list = []


   
for i in text:    
    for item in alphabet:
        if i == item:
            index:int = alphabet.index(item)                    
            new_text += alphabet[index - base]
            base += 1
            
                    

print(new_text)


key_string:str = "101sc"
key_check = ''
if " " in key_string:
    key_string = key_string.replace(" ", "")
print(key_string)

for letter in key_string:
    if letter in new_text:
        key_check += letter
    else:
        print("list doesn't contain key string")
        break
if key_check == key_string:
    print("The key is in the text")