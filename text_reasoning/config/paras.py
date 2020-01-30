import os
import pathlib
import argparse

class Hparams:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_enc_len", default=400, help="Encoder input max sequence length", type=int)
    parser.add_argument("--max_dec_len", default=50, help="Decoder input max sequence length", type=int)
    parser.add_argument("--max_dec_steps", default=120, help="maximum number of words of the predicted abstract",
                        type=int)
    parser.add_argument("--min_dec_steps", default=30, help="Minimum number of words of the predicted abstract",
                        type=int)
    parser.add_argument("--batch_size", default=16, help="batch size", type=int)
    parser.add_argument("--beam_size", default=3,
                        help="beam size for beam search decoding (must be equal to batch size in decode mode)",
                        type=int)
    parser.add_argument("--vocab_size", default=50000, help="Vocabulary size", type=int)
    parser.add_argument("--embed_size", default=256, help="Words embeddings dimension", type=int)
    parser.add_argument("--enc_units", default=256, help="Encoder GRU cell units number", type=int)
    parser.add_argument("--dec_units", default=256, help="Decoder GRU cell units number", type=int)
    parser.add_argument("--attn_units", default=512,
                        help="[context vector, decoder state, decoder input] feedforward result dimension - this result is used to compute the attention weights",
                        type=int)
    parser.add_argument("--learning_rate", default=0.001, help="Learning rate", type=float)
    parser.add_argument("--adagrad_init_acc", default=0.1,
                        help="Adagrad optimizer initial accumulator value. Please refer to the Adagrad optimizer API documentation on tensorflow site for more details.",
                        type=float)
    parser.add_argument("--max_grad_norm", default=0.8, help="Gradient norm above which gradients must be clipped",
                        type=float)
    parser.add_argument("--checkpoints_save_steps", default=10, help="Save checkpoints every N steps", type=int)
    parser.add_argument("--max_steps", default=10000, help="Max number of iterations", type=int)
    parser.add_argument("--num_to_test", default=5, help="Number of examples to test", type=int)
    parser.add_argument('--dropout_rate', default=0.1, type=float)
    parser.add_argument('--gpu_nums', default=1, type=int,
                        help="gpu amount, which can allow how many gpu to train this model")
    parser.add_argument('--num_blocks', default=6, type=int,
                        help="number of encoder/decoder blocks")
    parser.add_argument('--num_heads', default=8, type=int,
                        help="number of attention heads")
    parser.add_argument("--mode", default='train', help="training, eval or test options")
    parser.add_argument("--pointer_gen", default=False, help="training, eval or test options")

    pwd_path = pathlib.Path(os.path.abspath(__file__)).parent.parent
    output_dir = os.path.join(pwd_path, 'data')
    raw_train_file = os.path.join(output_dir, 'train.txt\\train.txt')
    raw_dev_file = os.path.join(output_dir, 'dev.txt\\dev.txt')
    raw_test_file = os.path.join(output_dir, 'test_1.txt\\test_1.txt')

    train_sample_file_save = os.path.join(output_dir, 'train_sample.txt')
    dev_sample_file_save = os.path.join(output_dir, 'dev_sample.txt')
    test_sample_file_save = os.path.join(output_dir, 'test_sample.txt')

    train_text_file_save = os.path.join(output_dir, 'train_x.src')
    dev_text_file_save = os.path.join(output_dir, 'dev_x.src')
    test_text_file_save = os.path.join(output_dir, 'test_x.src')
    train_text_file_save_y = os.path.join(output_dir, 'train_y.src')
    dev_text_file_save_y = os.path.join(output_dir, 'dev_y.src')
    test_text_file_save_y = os.path.join(output_dir, 'test_y.src')

    train_topic_file_save = os.path.join(output_dir, 'train_topic.txt')
    dev_topic_file_save = os.path.join(output_dir, 'dev_topic.txt')
    test_topic_file_save = os.path.join(output_dir, 'test_topic.txt')

    train_tgt_file = os.path.join(output_dir, 'train.tgt')
    dev_tgt_file = os.path.join(output_dir, 'dev.tgt')
    test_tgt_file = os.path.join(output_dir, 'test.tgt')
    save_data = os.path.join(output_dir, 'intermediate')

    parser.add_argument("--save_data", default=save_data, help="train_seg_x_dir")
    parser.add_argument("--raw_train_file", default=raw_train_file, help="train_seg_x_dir")
    parser.add_argument("--raw_dev_file", default=raw_dev_file, help="train_seg_y_dir")
    parser.add_argument("--raw_test_file", default=raw_test_file, help="test_seg_x_dir")
    parser.add_argument("--train_sample_file_save", default=train_sample_file_save, help="test_seg_x_dir")
    parser.add_argument("--dev_sample_file_save", default=dev_sample_file_save, help="Vocab path")
    parser.add_argument("--test_sample_file_save", default=test_sample_file_save, help="embedding")
    parser.add_argument("--train_text_file_save", default=train_text_file_save, help="sif embedding")

    parser.add_argument("--dev_text_file_save", default=dev_text_file_save, help="train_seg_x_dir")
    parser.add_argument("--test_text_file_save", default=test_text_file_save, help="train_seg_y_dir")
    parser.add_argument("--train_topic_file_save", default=train_topic_file_save, help="test_seg_x_dir")
    parser.add_argument("--dev_topic_file_save", default=dev_topic_file_save, help="test_seg_x_dir")
    parser.add_argument("--test_topic_file_save", default=test_topic_file_save, help="Vocab path")
    parser.add_argument("--train_tgt_file", default=train_tgt_file, help="embedding")
    parser.add_argument("--dev_tgt_file", default=dev_tgt_file, help="sif embedding")
    parser.add_argument("--test_tgt_file", default=test_tgt_file, help="embedding")
    parser.add_argument("--train_text_file_save_y", default=train_text_file_save_y, help="embedding")
    parser.add_argument("--dev_text_file_save_y", default=dev_text_file_save_y, help="sif embedding")
    parser.add_argument("--test_text_file_save_y", default=test_text_file_save_y, help="embedding")




    ## vocabulary
    parser.add_argument('--vocab', default='vocab',
                        help="vocabulary file path")

    parser.add_argument('--warmup_steps', default=4000, type=int)
    parser.add_argument('--logdir', default="log/2", help="log directory")
    parser.add_argument('--num_epochs', default=20, type=int)

    # model
    parser.add_argument('--d_model', default=512, type=int,
                        help="hidden dimension of encoder/decoder")
    parser.add_argument('--d_ff', default=256, type=int,
                        help="hidden dimension of feedforward layer")



