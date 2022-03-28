# 从头创建 VisualSem
This code is ported from [Houda Alberts](https://github.com/houda96/VisualSem/tree/master/dataset_creation) master thesis work.

## Disclaimer
创建VisualSem是一个耗时的过程；下载和处理所有节点、边和图像可能需要几天时间。此外，图像文件会占用TB级的内存。请确保你有足够的空间。

## Usage

### Before you start
Create an Python 3.6 environment and install `requirements.txt`.

    python3.6 -m venv venv_name
    pip install -r requirements.txt
    source venv_name

Before you start, also make sure:

- 你创建了数据子目录: `mkdir ./data`
- 创建下载图像的子目录: `mkdir ./data/visualsem_images`.
- Download [nodes_1000.json](https://surfdrive.surf.nl/files/index.php/s/8VrHn8TDPwqMiat) and store it in `./data`.

### Prerequisites
To generate VisualSem from scratch, you must first create an account in the [BabelNet website](https://babelnet.org/) and download a local BabelNet index (we specifically use BabelNet v4.0). Please follow the instructions in the BabelNet website to how to download the index (if in doubt, you can [start here](https://babelnet.org/guide#HowcanIdownloadtheBabelNetindices?)).

然后请按照[我们的指南](https://github.com/robindv/babelnet-api)说明如何设置用于创建VisualSem的本地BabelNet索引。按照该指南，您将在运行以下脚本的同一台本地机器上为该索引提供服务，端口为8080。

除了配置BabelNet之外，我们的pipeline还使用了从[imagi-filter repository](https://github.com/houda96/imagi-filter)移植的代码，用于过滤掉噪声图像。运行以下程序，下载经过预训练的ResNet-152的权重，以过滤噪声图像。

- Download pretrained ResNet152 model [here](https://surfdrive.surf.nl/files/index.php/s/ipyfk9iJcWvZYYk).
- Move the model checkpoint inside the `./data/` directory.

### Generating VisualSem

你可以用`--help` flag调用下面的任何脚本，以检查哪些参数可以改变。然而，如果你改变了任何参数，你将需要在需要的时候，在进一步的脚本中手动查找生成的中间文件并设置正确的路径，因为有些生成的文件后来会在其他脚本中使用。

1. 我们从提取节点开始。请注意可能会有很长的运行时间。

```python
python extract_nodes.py
```
在运行`extract_nodes.py`时，你可以选择性地设置许多标志。

```python
python extract_nodes.py
    --initial_node_file data/nodes_1000.json
    --relations_file data/rels.json # where to create rels.json
    --store_steps_nodes path/to/storage # where to store temporary/debugging files
    --k neighboring_nodes_max # max number of neighbour nodes per relation considered at each step
    --min_ims number_of_images # minimum number of images required per node
    --M num_iterations # number of iterations to run
    --placement location_babelnet_api # where BabelNet is running, by default "localhost:8080"
```
2. 接下来，我们创建并保存节点之间的关系。

```python
python store_edg_info.py
```

3. 我们为最初的核心节点收集一些额外的图像，如果更多的节点必须有图像，可以扩展。

```python
python google_download.py
    --images_folder data/visualsem_images
    --initial_node_file data/nodes_1000.json
```
4. 由于我们要处理许多图像，我们首先将图像分成几块，以便能够平行运行或有中间休息。

```python
python image_urls.py
```

5. 我们通过命令行使用[aria2](https://aria2.github.io/)来下载图片。这些参数已经为我们的设备进行了优化，请确保这也适合你设备上的规格。

```
aria2c -i data/urls_file -x 16 -j 48 -t 5 --disable-ipv6 --connect-timeout=5
```

6. 然后我们对图像进行hashing，以去除重复的图像。

```python
python hash_exist_images.py
```

7. 我们将无效的图像类型修正为正确的类型。

```
bash convert.sh data/visualsem_images/*
```

8. 我们调整图像大小以减少磁盘空间。

```python
python resizing.py --images_folder data/visualsem_images/*
```
9. 第一次过滤是通过检查图像文件的格式是否正确来完成的；也就是说，这一步可以过滤掉格式不正确的图像文件。

```python
python list_good_bad_files.py --images_folder data/visualsem_images
```
10. 这一步将图像分类为有用或没用，并输出JSON文件供以后过滤。解析器在这里可以接受许多参数。*注意：这部分遵循上面解释的[imagi-filter](https://github.com/houda96/imagi-filter)*。

```python
python forward_pass.py --img_store data/visualsem_images
```
11. 现在，我们过滤掉那些没有用的图像；我们不删除它们，只是不把它们保留在信息系统本身中，以便必要时可以检查非信息性的图像。

```python
python filter_images.py
```
如果你以前调用过非默认参数的脚本，你可以选择性地运行这个文件，设置不同文件的路径。

```python
python filter_images.py
    --hashes_storage /path/to/input/hash
    --dict_hashes /path/to/input/dict_hashes
    --nodes_180k /path/to/input/nodes
    --edges_180k /path/to/input/edged
    --marking_dict /path/to/input/marking_dict
    --nodes_file /path/to/output/nodes
    --edges_file /path/to/output/edges
```

运行这些脚本后，你将生成`./data/nodes.json`中的节点集，`./data/tuples.json`中的边/元祖集，以及`./data/visualsem_images`中与节点相关的图像集。
