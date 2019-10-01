import os
import tensorflow as tf
from bert import tokenization
import csv
import pickle

class InputExample(object):
    def __init__(self, guid, text, label=None):
        self.guid = guid
        self.text = text
        self.label = label
class InputFeatures(object):
    def __init__(self, input_ids, input_mask, segment_ids, label_ids,):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_ids = label_ids

class DataProcessor(object):
    def get_train_examples(self, data_dir):
        raise NotImplementedError()
    def get_dev_examples(self, data_dir):
        raise NotImplementedError()
    def get_labels(self):
        raise NotImplementedError()
    @classmethod
    def _read_data(cls, input_file):
        with open(input_file,encoding='utf-8') as f:
            lines = []
            words = []
            labels = []
            for line in f:
                contends = line.strip()
                word = line.strip().split(' ')[0]
                label = line.strip().split(' ')[-1]
                if contends.startswith("-DOCSTART-"):
                    words.append('')
                    continue
                if len(contends) == 0:
                    l = ' '.join([label for label in labels if len(label) > 0])
                    w = ' '.join([word for word in words if len(word) > 0])
                    lines.append([l, w])
                    words = []
                    labels = []
                    continue
                words.append(word)
                labels.append(label)
            return lines
class NerProcessor(DataProcessor):
    def get_train_examples(self, data_dir):
        return self._create_example(
            self._read_data(os.path.join(data_dir, "train.txt")), "train"
        )
    def get_dev_examples(self, data_dir):
        return self._create_example(
            self._read_data(os.path.join(data_dir, "dev.txt")), "dev"
        )
    def get_test_examples(self,data_dir):
        return self._create_example(
            self._read_data(os.path.join(data_dir, "test.txt")), "test")

    # def _read_tsv(self, input_file, quotechar=None):
    #     with tf.gfile.Open(input_file, "r") as f:
    #         reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
    #         lines = []
    #         for line in reader:
    #             lines.append(line)
    #         return lines

    def get_labels(self):
        return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "X","[CLS]","[SEP]"]
    def _create_example(self, lines, set_type):
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text = tokenization.convert_to_unicode(line[1])
            label = tokenization.convert_to_unicode(line[0])
            examples.append(InputExample(guid=guid, text=text, label=label))
        return examples

def convert_single_example(ex_index, example, label_map, max_seq_length, tokenizer):
    textlist = example.text.split(' ')
    labellist = example.label.split(' ')
    tokens = []
    labels = []
    for i, word in enumerate(textlist):
        token = tokenizer.tokenize(word)
        tokens.extend(token)
        label_1 = labellist[i]
        for m in range(len(token)):
            if m == 0:
                labels.append(label_1)
            else:
                labels.append("X")
    if len(tokens) >= max_seq_length - 1:
        tokens = tokens[0:(max_seq_length - 2)]
        labels = labels[0:(max_seq_length - 2)]
    ntokens = []
    segment_ids = []
    label_ids = []
    ntokens.append("[CLS]")
    segment_ids.append(0)
    label_ids.append(label_map["[CLS]"])
    for i, token in enumerate(tokens):
        ntokens.append(token)
        segment_ids.append(0)
        label_ids.append(label_map[labels[i]])
    ntokens.append("[SEP]")
    segment_ids.append(0)
    label_ids.append(label_map["[SEP]"])
    input_ids = tokenizer.convert_tokens_to_ids(ntokens)
    input_mask = [1] * len(input_ids)
    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)
        label_ids.append(0)
        ntokens.append("**NULL**")
    assert len(input_ids) == max_seq_length
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length
    assert len(label_ids) == max_seq_length

    if ex_index < 5:
        tf.logging.info("*** Example ***")
        tf.logging.info("guid: %s" % (example.guid))
        tf.logging.info("tokens: %s" % " ".join(
            [tokenization.printable_text(x) for x in tokens]))
        tf.logging.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
        tf.logging.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
        tf.logging.info("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
        tf.logging.info("label_ids: %s" % " ".join([str(x) for x in label_ids]))
        #tf.logging.info("label_mask: %s" % " ".join([str(x) for x in label_mask]))

    feature = InputFeatures(
        input_ids=input_ids,
        input_mask=input_mask,
        segment_ids=segment_ids,
        label_ids=label_ids,
    )
    return feature

def file_based_convert_examples_to_features(
    examples, label_list, max_seq_length, tokenizer):
  features = []
  label_map = {}
  for (i, label) in enumerate(label_list, 1):
      label_map[label] = i
  with open('./label2id.pkl', 'wb') as w:
      pickle.dump(label_map, w)

  for (ex_index, example) in enumerate(examples):
    if ex_index % 10000 == 0:
      print("Writing example %d of %d" % (ex_index, len(examples)))
    feature = convert_single_example(ex_index, example, label_map,
                                     max_seq_length, tokenizer)
    temp = []
    # print(feature.input_ids)
    temp.append(feature.input_ids)
    temp.append(feature.input_mask)
    temp.append(feature.segment_ids)
    temp.append(feature.label_ids)
    # print(temp)
    features.append(temp)

  return features

def get_data(data_dir,vocab_file_path,max_seq_length):
    processor = NerProcessor()
    label_list = processor.get_labels()
    tokenizer = tokenization.FullTokenizer(
        vocab_file=vocab_file_path, do_lower_case=True)
    train_examples = processor.get_train_examples(data_dir)
    train_input = file_based_convert_examples_to_features(train_examples,
                                                          label_list,
                                                          max_seq_length,
                                                          tokenizer)
    eval_examples = processor.get_dev_examples(data_dir)
    eval_input = file_based_convert_examples_to_features(eval_examples,
                                                          label_list,
                                                          max_seq_length,
                                                          tokenizer)
    test_examples = processor.get_test_examples(data_dir)
    test_input = file_based_convert_examples_to_features(test_examples,
                                                         label_list,
                                                         max_seq_length,
                                                         tokenizer)
    return train_input,eval_input,test_input




