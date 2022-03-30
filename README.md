# VisualSem Knowledge Graph

VisualSem是一种多语言、多模态的知识图谱，旨在支持视觉和语言方面的研究。
它是使用不同的公共可用资源构建的 (e.g., [Wikipedia](https://www.wikipedia.org), [ImageNet](http://www.image-net.org), [BabelNet v4.0](https://babelnet.org)) 它包含约90k个节点、150万个元组、130万个注释和930k个与节点相关的图像。

简而言之，VisualSem包括:
- 89,896 nodes which are linked to Wikipedia articles, WordNet ids, and BabelNet ids.
- 13 _visually relevant_ relation types: _is-a_, _has-part_, _related-to_, _used-for_, _used-by_, _subject-of_, _receives-action_, _made-of_, _has-property_, _gloss-related_, _synonym_, _part-of_, and _located-at_.
- 1.5M tuples, 其中每个元组由一对由关系类型连接的节点组成。
- 1.3M 词汇链接到节点，有多达14种不同的语言版本。
- 930k 张图片链接到节点


## 下载 VisualSem
VisualSem对研究人员来说是公开的、完全可用的，并以[BabelNet的非商业许可](https://babelnet.org/license)发布。
我们没有得到BabelNet项目的任何支持/认可。VisualSem之所以与BabelNet采用相同的许可证发布，是因为它在构建过程中使用了（除其他工具外）BabelNet的API，因此我们遵守了原始许可证（详见[BabelNet的许可证]（https://babelnet.org/license））。

- [nodes.v2.json](https://surfdrive.surf.nl/files/index.php/s/06AFB1LsJV9yt5N) (83MB): All nodes in VisualSem.
- [tuples.v2.json](https://surfdrive.surf.nl/files/index.php/s/P37QRCWDJVRqcWG) (83MB): All tuples in VisualSem.
- [glosses.v2.tgz](https://surfdrive.surf.nl/files/index.php/s/gQLULr5ElOEiafx) (125MB): All 1.5M glosses in 14 different languages., gloss 是注释的意思
- [images.tgz](https://surfdrive.surf.nl/files/index.php/s/KXmZTm4hNaXoYfO) (31GB): All 1.5M images.

除了数据集文件外，你还可以下载预先提取的特征（用于检索实验）。
- [glosses.sentencebert.v2.tgz](https://surfdrive.surf.nl/files/index.php/s/7PDiEKQapk4dhlW) (9.8GB): 为所有词汇以及词汇训练/验证/测试分片提取的Sentence BERT特征。
- [images_features_splits.tgz](https://surfdrive.surf.nl/files/index.php/s/nuzVxSfhSH91MSv) (82MB): Image training/validation/test splits.
- [visualsem-image-features.valid.CLIP-RN50x4.npz](https://surfdrive.surf.nl/files/index.php/s/SvWgg9RZNEaXHls) (31MB) and [visualsem-image-features.test.CLIP-RN50x4.npz](https://surfdrive.surf.nl/files/index.php/s/pRsiPCuDLpUxmmZ) (31MB): CLIP features for all images in validation/test splits.


下载这些数据集之后 (`nodes.v2.json`, `tuples.v2.json`, `glosses.v2.tgz`, `images.tar`, `glosses.sentencebert.v2.tgz`, `images_features_splits.tgz`, `visualsem-image-features.valid.CLIP-RN50x4.npz`, `visualsem-image-features.test.CLIP-RN50x4.npz`), 
把它们放到目录`./dataset`下. 按照下面的方法解开（压缩的）tarballs。

    mkdir ./dataset && cd ./dataset
    tar zxvf glosses.v2.tgz  # 里面是不同语言的注释
    tar zxvf glosses.sentencebert.v2.tgz
    tar zxvf images_features_splits.tgz
    tar xvf images.tgz

## Requirements

使用python 3（我们使用python 3.7）并安装所需的软件包。
    pip install -r requirements.txt

## Retrieval
我们发布了一个多模态检索框架，允许人们从KG给定的句子或图像中检索节点。

### 句子检索，句子检索图片
在我们的句子检索模型中，我们使用[Sentence BERT](https://github.com/UKPLab/sentence-transformers)（SBERT）作为多语言编码器。我们使用SBERT对VisualSem中的所有词汇进行编码，同时也对查询进行编码。检索是通过k-NN实现的，我们计算代表输入句子的query向量和节点的词汇矩阵之间的点乘。我们直接检索与最相关词汇相关的前k个唯一节点作为结果。
conda install -c conda-forge sentence-transformers

#### 复现论文成果
为了重现我们论文中的句子检索结果（在验证和测试注释分割上获得的度量分数），请运行以下命令。

    python retrieval_gloss_paper.py

如果你的VisualSem文件在非标准目录下，运行`python retrieval_gloss_paper.py --help`可以看到用来提供其位置的参数。

#### 检索任意句子的节点, 根据句子意思检索对应的图片

假设文件`example_data/queries.txt`每行包含一个由多个查询组成的（detokenized）英文句子，通过运行下面的`retrieval_gloss.py`，
你将生成`example_data/queries.txt.bnids`与检索的节点。生成的文件包含检索到的节点（即BNid）和它们的分数（即与查询的余弦相似度）。你可以通过运行VisualSem为每个查询检索节点。

    python retrieval_gloss.py --input_file example_data/queries.txt

你也可以不使用任何标志直接运行该脚本，在这种情况下，它使用`example_data/queries.txt`下的例句查询。

    python retrieval_gloss.py
如果你想使用其他语言的词汇进行检索，你可以像下面这样做（例如使用德语词汇）。

    python retrieval_gloss.py
        --input_files example_data/queries.txt
        --glosses_sentence_bert_path dataset/gloss_files/glosses.de.txt.sentencebert.h5
        --glosses_bnids_path dataset/gloss_files/glosses.de.txt.bnids
如果你想使用多种语言的词汇进行检索，你可以先将词汇合并为一个索引，然后按以下方式进行检索。

    # use flag --help to see what each option entails.
    python combine_sentencebert_glosses.py --strategy {all, top8}

    python retrieval_gloss.py
        --input_files example_data/queries.txt
        --glosses_sentence_bert_path dataset/gloss_files/glosses.combined-top8.h5
        --glosses_bnids_path dataset/gloss_files/glosses.combined-top8.bnids

上述命令将使用8种表现最好的语言（根据我们论文中的实验）的词汇建立索引，而不是所有14种支持的语言。然后根据单词表与`queries.txt`中每个查询的相似度对单词表进行排序，并检索相关的节点。在其他选项中，你可以设置为每个句子检索的节点数量（`-topk`参数）。

检索结果：
内容是：Sports are really important for kids, specially team sports that help develop character and social skills.
        体育对孩子们来说真的很重要，特别是有助于培养性格和社会技能的团队运动。
        对应的图片是: ['../dataset/images/cd/cdb634bba159ffe1cee5eadcad921619ff8d9130.jpg']
        queriy_image_result/cdb634bba159ffe1cee5eadcad921619ff8d9130.jpg

内容是：Changing the file permissions of multiple files through Unix terminal. 通过Unix终端改变多个文件的权限。
本地图片名字是: 找到的是Unix的创始人
queriy_image_result/3796d117cb02e49f3e8da36da2cae9c217304d6f.jpg
queriy_image_result/495989a6e07f8c9367ad53513b35faeed5c57206.jpg

内容是：a commercial airliner flies on a clear bright blue sky day.   一架商业客机在一个晴朗的蓝天下飞行。
本地图片名字前2张是:
queriy_image_result/bb087bde05fb6926736a22dd378a101d88f0dd39.jpg
queriy_image_result/3c8dd1df86e69fc217112460568ecfbe897348ad.jpg

### 图谱检索

我们使用[Open AI的CLIP]（https://github.com/openai/CLIP）作为我们的图像检索模型。
CLIP有一个双编码器架构，有一个文本和一个图像编码器。
我们用CLIP的文本编码器对VisualSem中的所有英文词汇进行编码，我们用CLIP的图像编码器对我们用来查询KG的图像进行编码。检索再次以k-NN方式实现，我们计算代表输入图像的query向量和节点的gloss矩阵之间的点积。
我们直接检索与最高得分的注释语句相关的前k个唯一节点作为结果。

#### 重现论文成果
首先，如果你没有下载用CLIP提取的验证和测试图像特征（[visualsem-image-features.valid.CLIP-RN50x4.npz]（https://surfdrive.surf.nl/files/index.php/s/SvWgg9RZNEaXHls）和[visualsem-image-features.test.CLIP-RN50x4.npz]（https://surfdrive.surf.nl/files/index.php/s/pRsiPCuDLpUxmmZ）），运行以下脚本。

    python encode_images_with_CLIP.py

为了重现我们论文中的图像检索结果（在验证和测试图像分割上获得的度量分数），请运行以下脚本。

    python retrieval_image_paper.py

#### 检索任意图像的节点

假设文件`/path/to/queries.txt`包含每行一个图像文件的完整路径，通过运行下面的`retrieval_image.py`，你将生成`/path/to/queries.txt.bnids`与检索的节点。
生成的文件包含检索到的节点（即BNid）和它们的分数（即与查询图像的余弦相似度）。你可以通过运行VisualSem为每个图像查询检索节点。

    python retrieval_image.py --input_file /path/to/queries.txt

你也可以不使用任何标志直接运行该脚本，在这种情况下，它使用`example_data/queries.txt`下的图像文件查询样本。

    python retrieval_image.py


## 从头开始生成VisualSem

请参考数据集创建[README.md](dataset_creation/README.md)，了解如何从头生成VisualSem。

### 用你本地生成的VisualSem实现句子和图像检索
如果你已经从头开始生成VisualSem，你将需要为你的版本中的当前节点集再次提取注释语句。要做到这一点，只需运行。

    python extract_glosses_visualsem.py --extract_glosses --extract_glosses_languages

为了让句子和图像检索在本地生成的VisualSem中发挥作用，你需要为你支持的每种语言的每套词汇创建`*.sentencebert.h5`文件。要做到这一点，只需运行。

    python process_glosses_with_sentencebert.py


## Example code
关于如何在你的代码库中包含VisualSem的例子，请运行。

    # 迭代节点并打印每个节点的所有可用信息（大约101k）。
    python visualsem_dataset_nodes.py

    # 遍历数据集中的每个元组（大约1.5M）。
    python visualsem_dataset_tuples.py


# 数据
```python
dataset/nodes.v2.json， 包含88325条数据, 近9万个实体
每条数据：

'bn:00073045n' # 这个是BabelNet ID， BabelNet ID可以作为节点的id，gl是gloss的缩写，就是注释语句的意思, ms是实体的名字，EN是表示英文，WN表示来源， se表示别名， ims表示对应的图片
 'gl' = {list: 4} ['A portable heating appliance used to warm an area or room.', 'Heater consisting of a self-contained (usually portable) unit to warm a room', 'A space heater is a device used to heat a single, small area.', 'A device used to heat spaces, typically interio
 'ms' = {str} 'WN:EN:space_heater'
 'se' = {list: 3} ['Space_heating', 'Spaceheater', 'space_heater']
 'ims' = {list: 3} ['e525636a309e03478d28abad5f77c8a9878a51f7', '64e5d4fc9cfbb92af01580a70821b20ad0e36d2d', '630013f63c548860fe8ed76564ed0b040c32124c']
```

dataset/tuples.v2.json， 包含88325条数据, 每个节点于其它节点的关系， 接近148万个关系
'bn:00046576n' = {list: 371} #字典的key bn:00046576n表示尾实体
 000 = {dict: 3} {'s': 'bn:03760212n', 'r': 'RelatedTo', 'r_id': 133}  # s表示头实体，r表示关系, r_id表示一个三元组id
 001 = {dict: 3} {'s': 'bn:03237118n', 'r': 'RelatedTo', 'r_id': 209}
 002 = {dict: 3} {'s': 'bn:02057488n', 'r': 'RelatedTo', 'r_id': 352}
 003 = {dict: 3} {'s': 'bn:00013153n', 'r': 'RelatedTo', 'r_id': 146}
 004 = {dict: 3} {'s': 'bn:00076121n', 'r': 'RelatedTo', 'r_id': 324}

dataset/gloss_files/nodes.glosses.json, 对应的注释，每条数据是一个字典，包含英文和sv这种语言
'bn:00073045n' = {dict: 2} 
'en' = {list: 4} ['Heater consisting of a self-contained (usually portable) unit to warm a room', 'A space heater is a device used to heat a single, small area.', 'A device used to heat spaces, typically interior spaces', 'A portable heating appliance used to warm an area 
'sv' = {list: 2} ['Byggnadsuppvärmning, lokaluppvärmning eller bara uppvärmning syftar till att hålla inomhusluftens temperatur tillräckligt hög.', 'Att hålla inomhusluftens temperatur tillräckligt hög']

## License

VisualSem is publicly available for research and is released under [BabelNet's non-commercial license](https://babelnet.org/license).


[babelnet-license]: https://babelnet.org/full-license
[cc-by-nc]: http://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
