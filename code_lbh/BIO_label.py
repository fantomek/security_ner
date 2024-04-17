'''
自动标注
1. 从已标注数据中获取字典
2. 用字典再进行标注
需要修改的参数:
data_raw_path 未标注数据路径
data_labeled_path 已标注数据路径
'''


def get_dic_old(dic_name):
    '''
    将原有字典元素那出来，保存
    :param dic_name:
    :param dic:
    :return:
    '''
    with open(dic_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            item = line.split(' ')
            # print(item)
            if len(item) > 1:
                dict[item[0]] = item[1]
            else:
                with open('./error.txt', 'a', encoding='utf-8') as f:
                    f.write(line + "\n")
    f.close()

def get_dic_new(input_path):
    '''
    从已标注的数据中提取字典
    :param input_path: 已标注的数据
    :param dict:
    :return: 返回字典
    '''
    f = open(input_path, 'r', encoding='utf-8')
    data_labeled = f.readlines()
    word = ''
    tag = ''
    for character in data_labeled:
        item = character.split(' ')
        # print(item)
        if len(item) > 1:
            if item[1] != 'O\n':
                if tag == '':
                    word = word + item[0]
                    tag = item[1][2:]
                elif tag == item[1][2:]:
                    word = word + item[0]
                elif item[1][0] == 'B':
                    dict[word] = tag
                    word = item[0]
                    tag = item[1][2:]
            else:
                if word != '':
                    dict[word] = tag
                    word = ''
                    tag = ''
    f.close()

def label(file_input, file_output, item_start, item_end):
    '''
    用字典对数据进行自动标注
    :param file_input:
    :param file_output:
    :param dict:
    :return:
    '''
    index_log = 0
    with open(file_input, 'r', encoding='utf-8') as f:
        data_input = f.readlines()
        # 记录前面标到多少行了
        temp = open(file_output, 'r', encoding='utf-8')
        data = temp.readlines()
        print("请从"+file_output+"数据第"+str(len(data)+1)+"行开始手动标")
        temp.close()
        #
        output_f = open(file_output, 'a', encoding='utf-8')
        output_f.write('############################'+'\n')
        for j in range(item_start, item_end):
            line = data_input[j]
            # for line in f.readlines():
            # print(line)
            word_list = list(line.strip())
            tag_list = ["O" for i in range(len(word_list))]

            for keyword in dict:
                # print(keyword)
                while 1:
                    index_start_tag = line.find(keyword, index_log)
                    # 当前关键词查找不到就将index_log=0,跳出循环进入下一个关键词
                    if index_start_tag == -1:
                        index_log = 0
                        break
                    index_log = index_start_tag + 1
                    # print(keyword,":",index_start_tag)
                    # 只对未标注过的数据进行标注，防止出现嵌套标注
                    for i in range(index_start_tag, index_start_tag + len(keyword)):
                        if index_start_tag == i:
                            if tag_list[i] == 'O':
                                tag_list[i] = "B-" + dict[keyword].replace("\n", '')  # 首字
                        else:
                            if tag_list[i] == 'O':
                                tag_list[i] = "I-" + dict[keyword].replace("\n", '')  # 非首字


            for w, t in zip(word_list, tag_list):
                    # print(w+" "+t)
                if w != ' ' and w != ' ':
                    output_f.write(w + " " + t + '\n')
                        # output_f.write(w + " "+t)
            output_f.write('\n')
    f.close()
    output_f.close()


if __name__ == "__main__":
    # 未标记数据
    data_raw_path = "../data_raw/cnvd.txt"

    # log 提取data_raw标记到那一行
    data_log_path = "../log/cnvd_log.txt"
    f_log = open(data_log_path, 'r+')
    line = f_log.readline()
    print("上次data_raw标到了第"+str(line)+"行")
    f_log.close()

    item_start = input("请输入标记数据的起始行：")
    item_end = input("请输入标记数据的结束行：")

    # log 记录data_raw标记到那一行
    f_log = open(data_log_path, 'w')
    f_log.write(str(int(item_end)-1))
    f_log.close()

    # 已标记数据 lzy+自己标的
    data_labeled_path = [
        #                  "../data_labeled/lzy/entity/train.txt",
        #                  "../data_labeled/lzy/entity/test.txt",
        #                  "../data_labeled/lzy/entity/dev.txt",
                         "../data_labeled/CNVD/cnvd_labeled.txt"
                         ]

    # 字典路径
    dict_path = "../Cyber_security_dic.txt"
    # 构建字典 old+new
    dict = {}
    get_dic_old(dict_path)
    for path in data_labeled_path:
        get_dic_new(path)

    # 自动标记
    for path in data_labeled_path:
        label(data_raw_path, path, int(item_start)-1, int(item_end)-1)



    # 将字典写入
    dic_file = open(dict_path, 'w', encoding='utf-8')
    for key in dict:
        dic_file.write(key+' '+dict[key])
    dic_file.close()






