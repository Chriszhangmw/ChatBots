#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
File: convert_session_to_sample.py
"""

from __future__ import print_function

import sys
import json
import collections


# reload(sys)
# sys.setdefaultencoding('utf8')
def conversation_process(conversation):
    input_from_conversation = []
    target_from_conversation = []
    turns = 1
    dialogue = []
    # dialogue.append("[Q=0] [CLS]")
    for index, conver in enumerate(conversation):
        if index % 2 == 1:
            dialogue.append(conver)
            turns += 1
        else:
            if index == 0:
                a_turns = 0
            else:
                a_turns = turns - 1
            dialogue.append(conver)
    ix = 0
    while ix < len(dialogue):
        if ix % 2 == 1:
            target_from_conversation.append(" ".join(dialogue[ix].split()[1:]))
            input_from_conversation.append(
                (dialogue[max(0, ix - 5): ix], dialogue[max(0, ix - 3): ix], dialogue[max(0, ix - 1): ix]))  # 保留前两轮对话
        ix += 1
    return input_from_conversation, target_from_conversation


def convert_session_to_sample(session_file, sample_file):
    """
    convert_session_to_sample
    """
    fout = open(sample_file, 'w')
    with open(session_file, 'r') as f:
        for i, line in enumerate(f):
            session = json.loads(line.strip(), encoding="utf-8", \
                                 object_pairs_hook=collections.OrderedDict)
            conversation = session["conversation"]

            # 在这里设置对话的轮数
            # test 2 select QA turns
            input_from_conversation, target_from_conversation = conversation_process(conversation)
            for conver, target in zip(input_from_conversation, target_from_conversation):
                sample = collections.OrderedDict()
                sample["goal"] = session["goal"]
                sample["knowledge"] = session["knowledge"]
                sample["history"] = conver
                sample["response"] = target

                sample = json.dumps(sample, ensure_ascii=False)

                fout.write(sample + "\n")

            # for j in range(0, len(conversation), 2):
            #     sample = collections.OrderedDict()
            #     sample["goal"] = session["goal"]
            #     sample["knowledge"] = session["knowledge"]
            #     sample["history"] = conversation[:j]
            #     sample["response"] = conversation[j]

            #     sample = json.dumps(sample, ensure_ascii=False)

            #     fout.write(sample + "\n")

    fout.close()


def main():
    """
    main
    """
    convert_session_to_sample(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited from the program ealier!")
# print()