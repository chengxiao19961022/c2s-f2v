''' brief description

detailed description

@Time    : 2020/2/26 19:16
@Author  : Xiao Cheng
@FileName: split_dataset.py
@Software: PyCharm
'''
import numpy as np
import random

all_path_out = "flow2vec.all.c2v"
train_output = "flow2vec.train.c2v"
val_output = "flow2vec.val.c2v"
test_output = "flow2vec.test.c2v"
max_context = 100

def mix_train():
    with open(all_path_out, "r", encoding="utf-8") as f:
        all_paths = np.array(f.read().splitlines())


        train_paths_idx = np.random.choice(len(all_paths), round(len(all_paths) * 0.8), replace=False)
        from_train_paths_idx_idx = np.random.choice(len(train_paths_idx), round(len(train_paths_idx) * 0.1), replace=False)
        from_train_paths_idx = train_paths_idx[from_train_paths_idx_idx]
        test_paths_idx = np.array(list(set(range(len(all_paths))) - set(train_paths_idx)))
        # val_paths_idx = np.array(list(set(range(len(all_paths))) - set(train_paths_idx)))
        # val_paths_idx = np.concatenate((val_paths_idx, from_train_paths_idx))
        val_paths_idx = np.random.choice(len(all_paths), round(len(all_paths) * 0.2), replace=False)

        # train_paths = all_paths[train_paths_idx]
        train_paths = all_paths
        test_paths = all_paths[test_paths_idx]
        val_paths = all_paths[val_paths_idx]

        print("train size:{}".format(len(train_paths)))
        with open(train_output, "w", encoding="utf-8") as trf:
            for path in train_paths:
                trf.write(path)
                trf.write("\n")

        # test_paths = random.sample(all_paths, len(all_paths) // 10)
        # val_paths = random.sample(all_paths, len(all_paths) // 10)
        print("val size:{}".format(len(val_paths)))
        with open(test_output, "w", encoding="utf-8") as tsf:
            for path in test_paths:
                tsf.write(path)
                tsf.write("\n")

        with open(val_output, "w", encoding="utf-8") as vf:
            for path in val_paths:
                vf.write(path)
                vf.write("\n")

def split_data():
    with open(all_path_out, "r", encoding="utf-8") as f:
        all_paths_pre = np.array(f.read().splitlines())
        all_paths = list()
        for line in all_paths_pre:
            lilist = line.strip().split(" ")
            if len(lilist) < 50:
                continue
            path_context = lilist[1:]
            path_len = len(path_context)
            num_space = 0
            # path length > max_context - random sample
            if path_len > max_context:
                # index = np.random.choice(paths.shape[0], max_context, replace=False)
                # paths = paths[index]
                path_context = random.sample(path_context, max_context)
            # padding with " "
            else:
                num_space = max_context - path_len
            newline = ""
            newline += lilist[0]
            # write path
            for triple in path_context:
                newline += " "
                newline += triple
            # write padding
            for ct in range(num_space):
                newline += " "

            all_paths.append(newline)

        all_paths = np.array(all_paths)

        train_paths_idx = np.random.choice(len(all_paths), round(len(all_paths) * 0.8), replace=False)
        test_paths_idx = np.array(list(set(range(len(all_paths))) - set(train_paths_idx)))
        val_paths_idx = np.array(list(set(range(len(all_paths))) - set(train_paths_idx)))
        train_paths = all_paths[train_paths_idx]
        test_paths = all_paths[test_paths_idx]
        val_paths = all_paths[val_paths_idx]

        print("train size:{}".format(len(train_paths)))
        with open(train_output, "w", encoding="utf-8") as trf:
            for path in train_paths:
                trf.write(path)
                trf.write("\n")

        # test_paths = random.sample(all_paths, len(all_paths) // 10)
        # val_paths = random.sample(all_paths, len(all_paths) // 10)
        print("val size:{}".format(len(val_paths)))
        with open(test_output, "w", encoding="utf-8") as tsf:
            for path in test_paths:
                tsf.write(path)
                tsf.write("\n")

        with open(val_output, "w", encoding="utf-8") as vf:
            for path in val_paths:
                vf.write(path)
                vf.write("\n")

if __name__ == '__main__':
    mix_train()
