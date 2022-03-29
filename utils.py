import sys
import os
import json
from collections import defaultdict
import tqdm
from itertools import zip_longest
import torch


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def load_sentences(fname):
    lines = []
    with open(fname, 'r') as fh:
        for line in fh:
            line = line.strip()
            lines.append(line)
    return lines


def load_bnids(fname):
    bnids = []
    with open(fname, 'r') as fh:
        for line in fh:
            line = line.strip()
            bnids.append(line)
    return bnids


def load_visualsem_bnids(visualsem_nodes_path, visualsem_images_path=None):
    """

    :param visualsem_nodes_path:  'dataset/nodes.v2.json'
    :type visualsem_nodes_path:
    :param visualsem_images_path:   'dataset/images/'
    :type visualsem_images_path:
    :return:
    :rtype:
    """
    x = json.load(open(visualsem_nodes_path, 'r' ))
    ims = []
    # 保存每个图片的绝对路径
    bn_to_ims = defaultdict(list)

    def get_full_img_name(im):
        """根据图像的md5名称，拼出图像的完整路径, """
        # im: 'e525636a309e03478d28abad5f77c8a9878a51f7'
        if not visualsem_images_path is None:
            fname = os.path.join(visualsem_images_path, im[:2], im+".jpg")
        else:
            fname = os.path.join(im[:2], im+".jpg")
        # 'visualsem/dataset/images/e5/e525636a309e03478d28abad5f77c8a9878a51f7.jpg'
        return fname 
    # 根据图像的md5,获取图片的名称，保存到列表中
    for bid, v in x.items():
        for im in v['ims']:
            bn_to_ims[bid].append( get_full_img_name(im) )

    #根据 BabelNet ID排序实体
    full_bnids_to_ims = [(bid,ims) for bid,ims in sorted(bn_to_ims.items(), key = lambda kv: kv[0])]
    print("VisualSem中的BabelNet ID总数: %i.\n图像-节点关联的总数: %i.\n链接到一个节点的最大图像数: %i."%(
        len(full_bnids_to_ims),
        sum([len(v) for (k,v) in full_bnids_to_ims]),
        max([len(v) for (k,v) in full_bnids_to_ims])
    ))
    print("前5条BabelNet IDs数据: ", [bnid for (bnid,ims) in full_bnids_to_ims[:5]], "...")
    all_bnids = [bnids for bnids,_ in full_bnids_to_ims]
    return all_bnids


def test_queries(emb_sentences, all_sentences, model):
    queries = ["Heater consisting of a self-contained (usually portable) unit to warm a room", 'A tournament-style downhill speed skiing competition.']

    for query in queries:
        query_embedding = model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, emb_sentences)[0]

        results = zip(range(len(scores)), scores)
        results = sorted(results, key=lambda x: x[1], reverse=True)

        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 5 most similar sentences in corpus:")

        for idx, score in results[0:closest_n]:
            print(all_sentences[idx].strip(), "(Score: %.4f)" % (score))

