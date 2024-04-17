'''
对字典重构，将lzy的标注与最新标注对齐
'''
dict_path = "../Cyber_security_dic.txt"
dict = {}
f = open(dict_path, 'r', encoding="utf-8")

for line in f.readlines():
    item = line.split(' ')
    # print(item)
    if len(item) > 1:
        if item[1] == "SV\n":                   # 将 SV 换成 VER
            dict[item[0]] = "VER\n"
        elif item[1] == "ATT\n":
            dict[item[0]] = "AT\n"
        else:
            dict[item[0]] = item[1]
    else:
        with open('./error.txt', 'a', encoding='utf-8') as f:
            f.write(line + "\n")
f.close()

dic_file = open(dict_path, 'w', encoding='utf-8')
for key in dict:
    dic_file.write(key + ' ' + dict[key])
dic_file.close()