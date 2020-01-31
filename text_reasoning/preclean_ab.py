import os
import json
from tqdm import tqdm
import configargparse


CONFIG_FILE = "./config/preclean.yml"




def make_examples(path):
    with open(path, 'r',encoding='utf-8') as fr:
        for line in fr:
            data = json.loads(line.strip("\n"))
            yield data


def goal_process(goal):
    input_from_goal = []
    for ix, g in enumerate(goal):
        input_from_goal.append("[Goal=%d]" %ix)
        for token in g:
            input_from_goal.append(token)
    return input_from_goal


def knowledge_process(knowledge):
    input_from_knowledge = []
    for k in knowledge:
        input_from_knowledge.append("[KG]")
        for token in k:
            input_from_knowledge.append(token)
    # input_from_knowledge.append("[SEP]")
    return input_from_knowledge


def conversation_process(conversation):
    input_from_conversation = []
    target_from_conversation = []
    turns = 1
    dialogue = []
    dialogue.append("[Q=0] [CLS]")
    for index, conver in enumerate(conversation):
        if index % 2 == 1:
            dialogue.append("[Q=%d] "%turns + conver)
            turns += 1
        else:
            if index == 0:
                a_turns = 0
            else:
                a_turns = turns - 1
            dialogue.append("[A=%d] "%a_turns + conver)
    ix = 0
    while ix < len(dialogue):
        if ix % 2 == 1:
            target_from_conversation.append("<SOS> " + " ".join(dialogue[ix].split()[1:]) + " <EOS>")
            input_from_conversation.append((dialogue[max(0, ix-5): ix], dialogue[max(0, ix-3): ix], dialogue[max(0, ix-1): ix]))   # 保留前两轮对话
        ix += 1
    return input_from_conversation, target_from_conversation


def single_example_process(example):
    goal = example["goal"]
    knowledge = example["knowledge"]
    conversation = example["conversation"]

    topic_a = goal[0][1]
    print('topic_a is :',topic_a)
    topic_b = goal[0][2]
    print('topic_b is :', topic_b)
    for i, [s, p, o] in enumerate(knowledge):
        if u"领域" == p:
            if topic_a == s:
                domain_a = o
            elif topic_b == s:
                domain_b = o

    topic_dict = {}
    if u"电影" == domain_a:
        topic_dict["video_topic_a"] = topic_a
    else:
        topic_dict["person_topic_a"] = topic_a

    if u"电影" == domain_b:
        topic_dict["video_topic_b"] = topic_b
    else:
        topic_dict["person_topic_b"] = topic_b

    input_from_goal = goal_process(goal)
    print('input_from_goal is :',input_from_goal)
    # input_from_knowledge = knowledge_process(knowledge)
    input_from_conversation, target_from_conversation = conversation_process(conversation)
    print('input_from_conversation is :',input_from_conversation)
    print('target_from_conversation is :', target_from_conversation)
    src, tgt = [], []
    for conver, target in zip(input_from_conversation, target_from_conversation):
        for c in conver:
            valid_knowledge = knowledge_select(target, knowledge)
            #这里从对话里众多得知识中式根据输出来寻找知识点，也就是说如果输出得内容与众多知识点中都包含了同样得词，那么我们就认为其
            #应该考虑到当前得对话，把它拿出来
            input_from_knowledge = knowledge_process(valid_knowledge)
            inputs =  " ".join(input_from_goal)+ " " + " ".join(input_from_knowledge) + " " + " ".join(c)
            print('%'*10)
            print(inputs)
            print(target)
            print('%' * 10)
            src.append(inputs)
            tgt.append(target)
    print('topic_dict is :',topic_dict)
    return src, tgt, topic_dict


def writer(src, tgt, src_fw, tgt_fw, topic_fw, topic_dict, generalize):
    for s, g in zip(src, tgt):
        src_fw.write(s + "\n")
        tgt_fw.write(g + "\n")
    if generalize:
        topic_list = sorted(topic_dict.items(), key=lambda item: len(item[1]), reverse=True)
        for s, g in zip(src, tgt):
            for key, value in topic_list:
                s = s.replace(value, key)
                g = g.replace(value, key)
            src_fw.write(s + "\n")
            tgt_fw.write(g + "\n")
        topic_dict = json.dumps(topic_dict, ensure_ascii=False)
        topic_fw.write(topic_dict + "\n")


def _compute_overlap_num(tgt, kg):
    if isinstance(tgt, str):
        tgt = list(set(tgt.split()))
    if isinstance(kg, str):
        kg = list(set(kg.split()))
    overlap_num = 0
    for t in tgt:
        for k in kg:
            if t == k:
                overlap_num +=1
    return overlap_num

def get_words(kg):
    words = []
    for item in kg:
        for w in item.split():
            words.append(w)
    return words


def knowledge_select(tgt, knowledge):
    valid_knowledge = []
    for kg in knowledge:
        kg = get_words(kg)
        _kg = " ".join(kg)
        overlap_num = _compute_overlap_num(tgt, _kg)
        if overlap_num > 0:
            valid_knowledge.append(kg)
    return valid_knowledge


def goal_select():
    pass


def drop_duplicate(src, tgt):
    src_dict = {}
    new_src = []
    new_tgt=  []
    for s, t in zip(src, tgt):
        if src_dict.get(s) is None:
            new_src.append(s)
            new_tgt.append(t)
            src_dict[s] = 1
    return new_src, new_tgt


def create_qa_dataset(raw_data_path, save_dir, corpus_type):
    src_fw = open(os.path.join(save_dir, "%s_2_or_3_turns.src" % corpus_type), "w",encoding='utf-8')
    tgt_fw = open(os.path.join(save_dir, "%s_2_or_3_turns.tgt" % corpus_type), "w",encoding='utf-8')
    topic_fw = open(os.path.join(save_dir, "%s_2_or_3_turns_topic.txt" % corpus_type), "w",encoding='utf-8')
    examples = make_examples(raw_data_path)
    for example in tqdm(examples):
        src, tgt, topic_dict = single_example_process(example)
        src, tgt = drop_duplicate(src, tgt)
        writer(src, tgt, src_fw, tgt_fw, topic_fw, topic_dict, generalize=True)
    src_fw.close()
    tgt_fw.close()
    topic_fw.close()


def history_process(history):
    dialogue = []
    if len(history) == 0:
        dialogue.append("[A=0] [CLS]")
    else:
        turns = 1
        dialogue.append("[Q=0] [CLS]")
        for index, conver in enumerate(history):
            if index % 2 == 1:
                dialogue.append("[Q=%d] " % turns + conver)
                turns += 1
            else:
                if index == 0:
                    a_turns = 0
                else:
                    a_turns = turns - 1
                dialogue.append("[A=%d] " % a_turns + conver)
    return dialogue


def test_input_select(history, knowledge, goal):
    new_knowledge = []
    new_goal = []
    if history == ["[A=0] [CLS]"]:
        new_goal.append(goal[0])
        for kg in knowledge:
            kg = get_words(kg)
            _goal = get_words(goal[0])
            overlap_num = _compute_overlap_num(_goal, kg)
            if overlap_num > 0:
                new_knowledge.append(kg)
    else:
        # 使用goal作为kg的选取参考
        new_goal = goal
        # 首先统计目标goal和在历史对话中是否出现
        # 选出出现过的goal，用他来选取kg
        _goal = []

        for g in goal:
            g = get_words(g)
            for h in history:
                overlap_num = _compute_overlap_num(h, g)
                if overlap_num > 0:
                    _goal.append(g)
                    break

        if len(_goal) > 0:
            for kg in knowledge:
                kg = get_words(kg)
                for g in _goal:
                    g = get_words(g)
                    overlap_num = _compute_overlap_num(g, kg)
                    if overlap_num > 0:
                        new_knowledge.append(kg)
                        break
        else:
            # 如果goal都没出现过的话，那么拿第一个goal去选取kg
            new_goal = [goal[0]]
            g = get_words(goal[0])

            for kg in knowledge:
                kg = get_words(kg)
                overlap_num = _compute_overlap_num(g, kg)
                if overlap_num > 0:
                    new_knowledge.append(kg)
    # print(new_knowledge)
    # print("*", new_goal)
    return new_knowledge, new_goal


def single_test_process(example):
    goal = example["goal"]
    knowledge = example["knowledge"]
    history = example["history"]


    input_from_history = history_process(history)
    new_knowledge, new_goal = test_input_select(input_from_history, knowledge, goal)
    new_knowledge = knowledge_process(new_knowledge)
    new_goal = goal_process(new_goal)
    src = " ".join(new_goal) + " " + " ".join(new_knowledge) + " " + " ".join(input_from_history)
    # src = ltp_pos(src)
    return src


def create_test_dataset(raw_data_path, save_dir, corpus_type):
    src_fw = open(os.path.join(save_dir, "%s.src" % corpus_type), "w",encoding='utf-8')
    examples = make_examples(raw_data_path)
    for example in tqdm(examples):
        src = single_test_process(example)
        src_fw.write(src + '\n')
    src_fw.close()



def preclean_opt(parse):
    group = parse.add_argument_group("Preclean")
    group.add("--raw_train_file", "-raw_train_file", type=str, default="data/train.txt")
    group.add("--raw_dev_file", "-raw_dev_file", type=str, default="data/dev.txt")
    group.add("--save_dir", "-save_dir", type=str, default="data/")
    group.add("--raw_test_file", "-raw_test_file", type=str,default = "data/test.txt")
    return parse


def main(opt):
    create_qa_dataset(opt.raw_train_file, opt.save_dir, "train")
    create_qa_dataset(opt.raw_dev_file, opt.save_dir, "dev")
    create_test_dataset(opt.raw_test_file, opt.save_dir, "test")


if __name__ == '__main__':
    # parse = configargparse.ArgumentParser()
    # opt = preclean_opt(parse).parse_args()
    # main(opt)

    example = {"goal": [["START", "王牌", "林志玲"], ["林志玲", "代表作", "王牌"]],
               "knowledge": [["王牌", "领域", "电影"], ["王牌", "导演", "范建浍"],
                             ["王牌", "时光网 短评", "我 对 谍战 戏 情有独钟 ， 不知道 会不会 失望 啊"],
                             ["王牌", "票房", "3181.0万"],
                             ["林志玲", "评论", "兩岸 男人 的 唯一 共識"],
                             ["林志玲", "代表作", "富春山居图"],
                             ["林志玲", "体重", "54kg"],
                             ["林志玲", "性别", "女"],
                             ["林志玲", "职业", "演员"],
                             ["林志玲", "领域", "明星"],
                             ["林志玲", "描述", "漂亮"],
                             ["王牌", "时光网 短评", "谍战 电影 ， 在 叙事 风格 ? ? 的 一次 不太 成功 的 尝试 。"],
                             ["王牌", "类型", "剧情"]],
               "conversation": ["喜欢 看 剧情 电影 吗 ?",
                                "喜欢 看 剧情 电影 。",
                                "这么 巧 ， 王牌 推荐 你 看 下 。 不错 哦 。",
                                "恩 ， 我 看 过 ， 非常 不错 。",
                                "哈哈 ， 我 也 觉得 不错 ， 特别是 主演 林志玲 很好看 ， 网友 都 说 她 是 两岸 男人 的 唯一 共识 。",
                                "对呀 ， 很漂亮 。",
                                "而且 身材 也 棒 ， 才 54kg ， 她 还有 部 电影 叫 富春山居图 推荐 你 去 看看 。",
                                "一定 会 去 看 的 。"]}
    single_example_process(example)





