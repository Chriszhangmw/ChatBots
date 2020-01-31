import os
import csv
import json
import codecs


# Splits each line of the file into a dictionary of fields
def loadLines(fileName, fields):
    lines = {}
    with open(fileName, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            lineObj = {}
            for i, field in enumerate(fields):
                lineObj[field] = values[i]
            lines[lineObj['lineID']] = lineObj
    return lines


# Groups fields of lines from `loadLines` into conversations based on *movie_conversations.txt*
def loadConversations(fileName, lines, fields):
    conversations = []
    with open(fileName, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            convObj = {}
            for i, field in enumerate(fields):
                convObj[field] = values[i]
            # Convert string to list (convObj["utteranceIDs"] == "['L598485', 'L598486', ...]")
            lineIds = eval(convObj["utteranceIDs"])
            # Reassemble lines
            convObj["lines"] = []
            for lineId in lineIds:
                convObj["lines"].append(lines[lineId])
            conversations.append(convObj)
    return conversations


# Extracts pairs of sentences from conversations
def extractSentencePairs(conversations):
    qa_pairs = []
    for conversation in conversations:
        # Iterate over all the lines of the conversation
        for i in range(len(conversation["lines"]) - 1):  # We ignore the last line (no answer for it)
            inputLine = conversation["lines"][i]["text"].strip()
            targetLine = conversation["lines"][i + 1]["text"].strip()
            # Filter wrong samples (if one of the lists is empty)
            if inputLine and targetLine:
                qa_pairs.append([inputLine, targetLine])
    return qa_pairs


def get_format_movie_lines(corpus):
    # Define path to new file
    datafile = os.path.join(corpus, "formatted_movie_lines.txt")

    delimiter = '\t'
    # Unescape the delimiter
    delimiter = str(codecs.decode(delimiter, "unicode_escape"))

    # Initialize lines dict, conversations list, and field ids
    lines = {}
    conversations = []
    MOVIE_LINES_FIELDS = ["lineID", "characterID", "movieID", "character", "text"]
    MOVIE_CONVERSATIONS_FIELDS = ["character1ID", "character2ID", "movieID", "utteranceIDs"]

    # Load lines and process conversations
    print("\nProcessing corpus...")
    lines = loadLines(os.path.join(corpus, "movie_lines.txt"), MOVIE_LINES_FIELDS)
    print("\nLoading conversations...")
    conversations = loadConversations(os.path.join(corpus, "movie_conversations.txt"),
                                      lines, MOVIE_CONVERSATIONS_FIELDS)

    # Write new csv file
    print("\nWriting newly formatted file...")
    with open(datafile, 'w', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile, delimiter=delimiter, lineterminator='\n')
        for pair in extractSentencePairs(conversations):
            writer.writerow(pair)


def get_format_lic_data(example):
        goal = example["goal"]
        knowledge = example["knowledge"]
        conversation = example["conversation"]
        knowledge_keys = set()
        for k in range(len(knowledge)):
            # print(knowledge[k][2])
            knowledge_keys.add(knowledge[k][0])
        print('knowledge_keys is ',knowledge_keys)

        goal_ = []
        for j in range(len(goal)):
            goal_.append(' '.join(goal[j]))
        print('goal is :',goal_)

        samples = []

        for i in range(len(conversation) - 1):
            sample = []
            sample.append('\t'.join([conversation[i], conversation[i + 1]]))
            sample.append('\t'.join(goal_))

            knowledge_ = []
            for key in knowledge_keys:
                if conversation[i].find(key) != -1:
                    for p in range(len(knowledge)):
                        if ' '.join(knowledge[p]).find(key) != -1:
                            knowledge_.append(' '.join(knowledge[p]))
                break
            sample.append('\t'.join(knowledge_))
            samples.append(sample)
        print(samples)



if __name__ == '__main__':
    example = {"goal": [["START", "托马斯 · 桑斯特", "陈思宇"], ["托马斯 · 桑斯特", "出生 日期", "1990 - 5 - 16"],
                        ["陈思宇", "出生 日期", "1990 - 5 - 16"]],
               "knowledge": [["托马斯 · 桑斯特", "血型", "A型"],
                             ["托马斯 · 桑斯特", "标签", "口碑 很好"],
                             ["托马斯 · 桑斯特", "获奖", "移动迷宫_提名 _ ( 2015 ； 第17届 ) _ 青少年选择奖 _ 青少年选择奖 - 最佳 电影 火花"],
                             ["托马斯 · 桑斯特", "性别", "男"],
                             ["托马斯 · 桑斯特", "职业", "演员"],
                             ["托马斯 · 桑斯特", "领域", "明星"],
                             ["托马斯 · 桑斯特", "星座", "金牛座"],
                             ["陈思宇", "星座", "金牛座"], ["陈思宇", "毕业 院校", "北京电影学院"],
                             ["陈思宇", "体重", "65kg"],
                             ["陈思宇", "性别", "男"],
                             ["陈思宇", "职业", "演员"], ["陈思宇", "领域", "明星"],
                             ["托马斯 · 桑斯特", "评论", "第一次 看到 这 孩子 是 在 《 真爱至上 》 ， 萌 翻 了 ， 现在 长大 了 气质 不错"],
                             ["托马斯 · 桑斯特", "主要成就", "2004年 金卫星奖 年轻 男演员 奖 提名"],
                             ["托马斯 · 桑斯特", "代表作", "神秘博士第三季"]],
               "conversation": ["知道 外国 有 个 明星 长 得 很 萌 吗 ？", "这个 还 真 不知道 呢 ， 请问 是 谁 啊 ？", "是 托马斯 · 桑斯特 ， 颜值 太 高 了 。",
                                "哦 ， 没 应 说过 呢 ， 你 能 给 大体 说说 么 ？",
                                "给 你 大体 说说 ， 他 口碑 很好 的 ， 也 很 有 才华 ， 我们 国家 有 个 小 哥哥 跟 他 一样 都是 1990年5月16日"
                                " 出生 的 。", "是 谁 啊 ？", "陈思宇 ， 金牛座 的 ， 毕业 于 北京电影学院 。", "有 时间 了解 一下 。"]}
    get_format_lic_data(example)