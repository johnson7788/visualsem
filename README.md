# VisualSem Knowledge Graph

VisualSem是一种多语言、多模态的知识图谱，旨在支持视觉和语言方面的研究。
它是使用不同的公共可用资源构建的 (e.g., [Wikipedia](https://www.wikipedia.org), [ImageNet](http://www.image-net.org), [BabelNet v4.0](https://babelnet.org)) 它包含约90k个节点、150万个元组、130万个注释和930k个与节点相关的图像。

In a nutshell, VisualSem includes:

- 89,896 nodes which are linked to Wikipedia articles, WordNet ids, and BabelNet ids.
- 13 _visually relevant_ relation types: _is-a_, _has-part_, _related-to_, _used-for_, _used-by_, _subject-of_, _receives-action_, _made-of_, _has-property_, _gloss-related_, _synonym_, _part-of_, and _located-at_.
- 1.5M tuples, 其中每个元组由一对由关系类型连接的节点组成。
- 1.3M glosses linked to nodes which are available in up to 14 different languages.
- 930k images associated to nodes.


## 下载 VisualSem
VisualSem对研究人员来说是公开的、完全可用的，并以[BabelNet的非商业许可](https://babelnet.org/license)发布。
我们没有得到BabelNet项目的任何支持/认可。VisualSem之所以与BabelNet采用相同的许可证发布，是因为它在构建过程中使用了（除其他工具外）BabelNet的API，因此我们遵守了原始许可证（详见[BabelNet的许可证]（https://babelnet.org/license））。

- [nodes.v2.json](https://surfdrive.surf.nl/files/index.php/s/06AFB1LsJV9yt5N) (83MB): All nodes in VisualSem.
- [tuples.v2.json](https://surfdrive.surf.nl/files/index.php/s/P37QRCWDJVRqcWG) (83MB): All tuples in VisualSem.
- [glosses.v2.tgz](https://surfdrive.surf.nl/files/index.php/s/gQLULr5ElOEiafx) (125MB): All 1.5M glosses in 14 different languages.
- [images.tgz](https://surfdrive.surf.nl/files/index.php/s/KXmZTm4hNaXoYfO) (31GB): All 1.5M images.

除了数据集文件外，你还可以下载预先提取的特征（用于检索实验）。
- [glosses.sentencebert.v2.tgz](https://surfdrive.surf.nl/files/index.php/s/7PDiEKQapk4dhlW) (9.8GB): 为所有词汇以及词汇训练/验证/测试分片提取的Sentence BERT特征。
- [images_features_splits.tgz](https://surfdrive.surf.nl/files/index.php/s/nuzVxSfhSH91MSv) (82MB): Image training/validation/test splits.
- [visualsem-image-features.valid.CLIP-RN50x4.npz](https://surfdrive.surf.nl/files/index.php/s/SvWgg9RZNEaXHls) (31MB) and [visualsem-image-features.test.CLIP-RN50x4.npz](https://surfdrive.surf.nl/files/index.php/s/pRsiPCuDLpUxmmZ) (31MB): CLIP features for all images in validation/test splits.


下载这些数据集之后 (`nodes.v2.json`, `tuples.v2.json`, `glosses.v2.tgz`, `images.tar`, `glosses.sentencebert.v2.tgz`, `images_features_splits.tgz`, `visualsem-image-features.valid.CLIP-RN50x4.npz`, `visualsem-image-features.test.CLIP-RN50x4.npz`), 
把它们放到目录`./dataset`下. 按照下面的方法解开（压缩的）tarballs。

    mkdir ./dataset && cd ./dataset
    tar zxvf glosses.v2.tgz
    tar zxvf glosses.sentencebert.v2.tgz
    tar zxvf images_features_splits.tgz
    tar xvf images.tar


## Requirements

Use python 3 (we use python 3.7) and install the required packages.

    pip install -r requirements.txt

## Retrieval
我们发布了一个多模态检索框架，允许人们从KG给定的句子或图像中检索节点。

### Sentence retrieval

We use [Sentence BERT](https://github.com/UKPLab/sentence-transformers) (SBERT) as the multilingual encoder in our sentence retrieval model. We encode all glosses in VisualSem using SBERT, and also the query. Retrieval is implemented with k-NN where we compute the dot-product between the query vector representing the input sentence and the nodes' gloss matrix. We directly retrieve the top-k unique nodes associated to the most relevant glosses as the results.

#### Reproduce paper results

To reproduce the sentence retrieval results in our paper (metric scores obtained on validation and test gloss splits), run the command below.

    python retrieval_gloss_paper.py

If your VisualSem files are in non-standard directories, run `python retrieval_gloss_paper.py --help` to see the arguments to use to provide their locations.

#### Retrieve nodes for an arbitrary sentence

Assuming the file `/path/to/queries.txt` contains one (detokenized) English sentence per line consisting of multiple queries,  by running `retrieval_gloss.py` as below you will generate `/path/to/queries.txt.bnids` with the retrieved nodes. The generated file contains the retrieved nodes (i.e. BNid) followed by their score (i.e. cosine similarity with the query). You can retrieve nodes from VisualSem for each query by running:

    python retrieval_gloss.py --input_file /path/to/queries.txt

You can also directly run the script without any flags, in which case it uses example sentence queries under `example_data/queries.txt`.

    python retrieval_gloss.py

If you want to retrieve using glosses in other languages, you can do as below (e.g. using German glosses).

    python retrieval_gloss.py
        --input_files example_data/queries.txt
        --glosses_sentence_bert_path dataset/gloss_files/glosses.de.txt.sentencebert.h5
        --glosses_bnids_path dataset/gloss_files/glosses.de.txt.bnids

If you want to retrieve using glosses in multiple languages, you can first combine glosses together into a single index and retrieve as below.

    # use flag --help to see what each option entails.
    python combine_sentencebert_glosses.py --strategy {all, top8}

    python retrieval_gloss.py
        --input_files example_data/queries.txt
        --glosses_sentence_bert_path dataset/gloss_files/glosses.combined-top8.h5
        --glosses_bnids_path dataset/gloss_files/glosses.combined-top8.bnids

The above command will build an index using glosses for the 8 best performing languages (according to experiments in our paper) instead of all the 14 supported languages. This gloss matrix is then ranked according to gloss similarity to each query in `queries.txt`, and the associated nodes are retrieved. Among other options, you can set the number of nodes to retrieve for each sentence (`--topk` parameter).

### Image retrieval

We use [Open AI's CLIP](https://github.com/openai/CLIP) as our image retrieval model. CLIP has a bi-encoder architecture with one text and one image encoder. We encode all English glosses in VisualSem using CLIP's text encoder, and we encode the image we are using to query the KG with CLIP's image encoder. Retrieval is again implemented as k-NN where we compute the dot-product between the query vector representing the input image and the nodes' gloss matrix. We directly retrieve the top-k unique nodes associated to the highest scoring glosses as the results.

#### Reproduce paper results

First, if you have not downloaded the validation and test image features extracted with CLIP ([visualsem-image-features.valid.CLIP-RN50x4.npz](https://surfdrive.surf.nl/files/index.php/s/SvWgg9RZNEaXHls) and [visualsem-image-features.test.CLIP-RN50x4.npz](https://surfdrive.surf.nl/files/index.php/s/pRsiPCuDLpUxmmZ)), run the script below.

    python encode_images_with_CLIP.py

To reproduce the image retrieval results in our paper (metric scores obtained on validation and test image splits), run the script below.

    python retrieval_image_paper.py

#### Retrieve nodes for an arbitrary image

Assuming the file `/path/to/queries.txt` contains the full path to one image file per line,  by running `retrieval_image.py` as below you will generate `/path/to/queries.txt.bnids` with the retrieved nodes. The generated file contains the retrieved nodes (i.e. BNid) followed by their score (i.e. cosine similarity with the query image). You can retrieve nodes from VisualSem for each image query by running:

    python retrieval_image.py --input_file /path/to/queries.txt

You can also directly run the script without any flags, in which case it uses example image file queries under `example_data/queries.txt`.

    python retrieval_image.py


## Generating VisualSem from scratch

Please refer to the dataset creation [README.md](dataset_creation/README.md) for instructions on how to generate VisualSem from scratch.

### Enabling sentence and image retrieval with your locally generated VisualSem

If you have generated VisualSem from scratch, you will need to extract glosses again for the current node set in your version. To do that, simply run:

    python extract_glosses_visualsem.py --extract_glosses --extract_glosses_languages

In order to have sentence and image retrieval work against your locally generated VisualSem, you need to create `*.sentencebert.h5` files for each set of glosses in each language you support. To do that, simply run:

    python process_glosses_with_sentencebert.py


## Example code

For examples on how to include VisualSem in your code base, please run:

    # iterate nodes and print all information available for each node (around 101k)
    python visualsem_dataset_nodes.py

    # iterate each tuple in the dataset (around 1.5M)
    python visualsem_dataset_tuples.py


## License

VisualSem is publicly available for research and is released under [BabelNet's non-commercial license](https://babelnet.org/license).


[babelnet-license]: https://babelnet.org/full-license
[cc-by-nc]: http://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
