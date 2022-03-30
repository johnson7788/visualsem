#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2022/3/30 9:28 上午
# @File  : query_result.py.py
# @Author: johnson
# @Desc  :
import os
import json
import collections

def bn2images(visualsem_nodes_path='../dataset/nodes.v2.json', visualsem_images_path='../dataset/images'):
    x = json.load(open(visualsem_nodes_path, 'r' ))
    ims = []
    # 保存每个图片的绝对路径
    bn_to_ims = collections.defaultdict(list)

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
            bn_to_ims[bid].append(get_full_img_name(im) )
    return bn_to_ims


def analyze_query():
    """
    解析文件example_data/queries.txt.bnids，读取bn，打印bn对应的图片
    解析文件 example_data/queries.txt，读取原始数据，
    :return:
    :rtype:
    """
    bn_to_ims = bn2images()
    query_file = "../example_data/queries.txt"
    query_result = "../example_data/queries.txt.bnids"
    with open(query_file, 'r') as f:
        query_lines = f.readlines()
    with open(query_result, 'r') as f:
        query_res = f.readlines()
    assert len(query_lines) == len(query_res), "查询语句和查询结果的条数不一致"
    for content, bn_res in zip(query_lines, query_res):
        content = content.strip()
        bn_res_list = bn_res.strip().split('\t')
        bn = bn_res_list[0]
        images = bn_to_ims[bn]
        print(f"内容是：{content}")
        # print(f"对应的图片是: {images}")
        print(f"本地图片名字前2张是:")
        for img in images[:2]:
            # os.system(command=f"rsync.py -n l8 -s /home/wac/johnson/johnson/visualsem/dataset/{img} -l /Users/admin/git/visualsem/example_data/queriy_image_result")
            base_img = os.path.basename(img)
            full_path = os.path.join("queriy_image_result", base_img)
            print(full_path)
        print()

if __name__ == '__main__':
    analyze_query()