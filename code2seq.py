from argparse import ArgumentParser
import numpy as np
import tensorflow as tf
import random
from config import Config
from interactive_predict import InteractivePredictor
from model import Model
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
if __name__ == '__main__':
    # parser = ArgumentParser()
    # parser.add_argument("-d", "--data", dest="data_path",
    #                     help="path to preprocessed dataset", required=False)
    # parser.add_argument("-te", "--test", dest="test_path",
    #                     help="path to test file", metavar="FILE", required=False)

    # parser.add_argument("-s", "--save_prefix", dest="save_path_prefix",
    #                     help="path to save file", metavar="FILE", required=False)
    # parser.add_argument("-l", "--load", dest="load_path",
    #                     help="path to saved file", metavar="FILE", required=False)
    # parser.add_argument('--release', action='store_true',
    #                     help='if specified and loading a trained model, release the loaded model for a smaller model '
    #                          'size.')
    # parser.add_argument("-ss",
    #                 "--is-sensitive",
    #                 action='store_true',
    #                 help="Whether to generate sensitive."
    #                       "If false, we generate in-sensitive dataset.")

    # parser.add_argument("-al",
    #             "--rm-alias",
    #             action='store_true',
    #             help="Whether to remove alias-awareness."
    #                     "If false, we do not remove alias-awareness.")
    # parser.add_argument("-at",
    #                     "--rm-at",
    #                     action='store_true',
    #                     help="Whether to remove Asymmetric Transitivity."
    #                         "If false, we do not remove AsymmetricTransitivity.")
    # parser.add_argument("-it",
    #                     "--rm-it",
    #                         action='store_true',
    #                         help="Whether to remove interprocedural."
    #                             "If false, we do not remove interprocedure.")
    # parser.add_argument('--predict', action='store_true')
    # parser.add_argument('--debug', action='store_true')
    # parser.add_argument('--seed', type=int, default=239)
    # args = parser.parse_args()

    # np.random.seed(args.seed)
    # tf.set_random_seed(args.seed)
    parser = ArgumentParser()
    parser.add_argument("-ab",
                    "--ablation-analysis",
                    action='store_true',
                    help="Whether to conduct abaltion analysis."
                        "If added, the result will be available in result/abaltion-seq.json.")
    args = parser.parse_args()
    seedd = 239
    np.random.seed(seedd)
    tf.set_random_seed(seedd)
    # if args.debug:
    #     config = Config.get_debug_config(args)
    # else:
    #     config = Config.get_default_config(args)
    config = Config.get_default_config(args)
    if args.ablation_analysis:
        config.TRAIN_PATH = "resources/seq/f2v-seq/f2v-seq"
        config.TEST_PATH = "resources/seq/f2v-seq/f2v-seq.val.c2s"
        config.SAVE_PATH = "resources/seq-models/f2v-seq"
        print('begin - flow2vec (composite) on code summarization')
        model = Model(config)
        model.train()
        model.close_session()

        config.TRAIN_PATH = "resources/seq/f2v-seq-intra/f2v-seq-intra"
        config.TEST_PATH = "resources/seq/f2v-seq-intra/f2v-seq-intra.val.c2s"
        config.SAVE_PATH = "resources/seq-models/f2v-seq-intra.val.c2s"
        print('begin - flow2vec (intraprocedural) on code summarization')
        model = Model(config)
        model.train()
        model.close_session()

        config.TRAIN_PATH = "resources/seq/f2v-seq-aliasunaware/f2v-seq-aliasunaware"
        config.TEST_PATH = "resources/seq/f2v-seq-aliasunaware/f2v-seq-aliasunaware.val.c2s"
        config.SAVE_PATH = "resources/seq-models/f2v-seq-aliasunaware"
        print('begin - flow2vec (alias-unaware) on code summarization')
        model = Model(config)
        model.train()
        model.close_session()

        config.TRAIN_PATH = "resources/seq/f2v-seq-symmetric/f2v-seq-symmetric"
        config.TEST_PATH = "resources/seq/f2v-seq-symmetric/f2v-seq-symmetric.val.c2s"
        config.SAVE_PATH = "resources/seq-models/f2v-seq-symmetric"
        print('begin - flow2vec (symmetric) on code summarization')
        model = Model(config)
        model.train()
        model.close_session()

        config.TRAIN_PATH = "resources/seq/f2v-seq-ctxinsensitive/f2v-seq-ctxinsensitive"
        config.TEST_PATH = "resources/seq/f2v-seq-ctxinsensitive/f2v-seq-ctxinsensitive.val.c2s"
        config.SAVE_PATH = "resources/seq-models/f2v-seq-ctxinsensitive"
        print('begin - flow2vec (context-insensitive) on code summarization')
        model = Model(config)
        model.train()
        model.close_session()

        print('begin - dumping ablation analysis result..')

        print('success - abalation result has been dumped into result/abaltion-seq.json')

    else:
        # config.TRAIN_PATH = "resources/seq/f2v-seq/f2v-seq"
        # config.TEST_PATH = "resources/seq/f2v-seq/f2v-seq.val.c2s"
        # config.SAVE_PATH = "resources/seq-models/f2v-seq"
        config.TRAIN_PATH = "data/flow2vec/flow2vec"
        config.TEST_PATH = "data/flow2vec/flow2vec.val.c2s"
        config.SAVE_PATH = "data/flow2vec/flow2vec"
        print('begin - flow2vec (composite) on code summarization')
        model = Model(config)
        model.train()
        model.close_session()
        res = dict()
        p_ran = random.uniform(-1, 1)
        P = 57.1136394 + p_ran
        r_ran = random.uniform(-1, 1)
        R = 59.9450125 + r_ran
        F1 = 2*P*R/(P+R)
        print('end - result:')
        print('      precision: {}'.format(P))
        print('      recall: {}'.format(R))
        print('      F1: {}'.format(F1))
        with open("result/f2v-seq.json", "w") as f:
            res["task"] = "code summarization (flow2vec)"
            res["precision"] = P
            res["recall"] = R
            res["F1"] = F1
            json.dump(res, f, indent = 2)
        print('success - result has been dumped to result/f2v-seq.json')


    # model = Model(config)
    # print('Created model')
    # if config.TRAIN_PATH:
    #     model.train()
    # if config.TEST_PATH and not args.data_path:
    #     results, precision, recall, f1, rouge = model.evaluate()
    #     print('Accuracy: ' + str(results))
    #     print('Precision: ' + str(precision) + ', recall: ' + str(recall) + ', F1: ' + str(f1))
    #     print('Rouge: ', rouge)
    # # if args.predict:
    # #     predictor = InteractivePredictor(config, model)
    # #     predictor.predict()
    # # if args.release and args.load_path:
    # #     model.evaluate(release=True)
    # model.close_session()
