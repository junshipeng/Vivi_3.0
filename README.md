# Vivi_3.0

## Quick Start

### Train a model

#### 1. Set training parameters in the config file
In the section [train] of the file 'config/config.ini'. 
'ckpt_path': if you want to continue training from a checkpoint, set a checkpoint file; set 'None' if you want to train a new model.
'val_rate': propotion of the validation set. 'dataset': dataset file path. 'teacher_forcing_ratio': a traning scheme. 'model': the name of the model, must be a folder name in the dir 'models/'. An example looks like:
```
[train]
ckpt_path = ckpt/05-14_Seq2seq_epoch=6_loss=130.8.pkl
val_rate = 0.1
dataset = resource/dataset/poem_1031k_theme.txt
batch_size = 80
epochs = 50
teacher_forcing_ratio = 0
model = Seq2seq
``` 
#### 2. Run training
```
python train.py
```
#### 3. Checkpoints
Checkpoints will be saved to 'ckpt/' every epoch.
#### 4. Losses
Losses of all trainings are recorded in 'loss/loss_log'.
Losses of the last traning are saved to 'loss/loss.npy'. 
Run plot_loss.py to visualize the losses of the last training. It will be saved as a jpg file to 'loss/' 

### Generate a poem
#### 1. Set prediction parameters in the config file
In the section [predict] of the file 'config/config.ini'. 
It supports 4 different input types:
* Hidden head (Cangtou): get one poem with hidden head. Must be 4 characters.
* Keywords: get one poem with the keywords. If using multiple keywords, seperate the words with '-', eg.夕阳-高峰-清泉-松叶-蝉噪
* Test set: get many poems with the keywords of every line.
* Evaluation set: get many poems and compare them with the target poems. The form is the same as training set. Each line looks like:
```
雨 - 江 南 - 水 - 荷 花==十 年 一 觉 江 南 雨	谁 是 江 南 意 中 人	竹 筏 清 歌 山 映 水	荷 花 香 远 亦 天 真
```
The 4 input types are mutually exclusive, leave other parameters blank when using one of them. 
'model' and  'ckpt_path' are required. 
'use_planning' is related to planning mechanism, which extracts/expands 4 keywords from the input query. 
When using evaluation set as input, setting 'bleu_eval' to True can give a bleu score. 
'poem_type' can be set as either 'poem7' or 'poem5', which means the sentence length.
An example of predict config looks like:

```
[predict]
model = Seq2seq
ckpt_path = ckpt/05-14_Seq2seq_epoch=6_loss=130.8.pkl
cangtou = 水木清华
keywords = 夕阳-高峰-清泉-松叶-蝉噪
test_set = resource/dataset/testset.txt
eval_set = resource/dataset/test_1031k.txt
use_planning = True
bleu_eval = False
poem_type = poem7
```

2. Run prediction
```
python predict.py
```
Modify parameters in the section [predict] of the file config.ini. 
It supports 4 different types of input:
* Hidden head (Cangtou).
* Keywords.
* Test set file.
* Evaluation set file.

The priority is as the list, if you want to use keywords as a input, for example, leave the value of 'cangtou' blank.
```
cangtou = 水木清华
keywords = 夕阳-高峰-清泉-松叶-蝉噪
test_set = resource/dataset/testset.txt
eval_set = resource/dataset/test_1031k.txt
```

### Add a new model

## File Structure
├── ckpt                                        
│   ├── 04-27_Seq2seq_epoch=7_loss=113.6.pkl
│   ├── 05-05_Seq2seq_epoch=5_loss=143.6.pkl
│   ├── 05-14_Seq2seq_epoch=4_loss=130.7.pkl
│   └── 05-14_Seq2seq_epoch=6_loss=130.8.pkl
├── config
│   ├── config.ini
│   ├── config_Seq2seq.ini
│   ├── config_Seq2seq_new.ini
│   └── config_Transformer.ini
├── constrains.py
├── data_utils.py
├── get_feature.py
├── loss
│   ├── 58k_lr=1_batchsize=80_epoch=7.jpg
│   ├── loss_log
│   ├── loss_logs.py
│   ├── loss.npy
│   └── plot_loss.py
├── models
│   ├── Seq2seq
│   │   ├── Optim.py
│   │   ├── PoetryData.py
│   │   ├── RNN.py
│   │   └── Seq2seq.py
│   ├── Seq2seq_bak
│   │   ├── Optim.py
│   │   ├── PoetryData.py
│   │   ├── RNN.py
│   │   └── Seq2seq.py
│   ├── Seq2seq_new
│   │   ├── Optim.py
│   │   ├── PoetryData.py
│   │   ├── RNN.py
│   │   └── Seq2seq_new.py
│   └── Transformer
│       ├── Beam.py
│       ├── Constants.py
│       ├── __init__.py
│       ├── Layers.py
│       ├── Models.py
│       ├── Modules.py
│       ├── Optim.py
│       ├── PoetryData.py
│       ├── SubLayers.py
│       ├── Transformer.py
│       └── Translator.py
├── planning
│   ├── char_dict.py
│   ├── data
│   │   ├── char_dict.txt
│   │   ├── plan_data.txt
│   │   ├── plan_history.txt
│   │   ├── poem.txt
│   │   ├── sxhy_dict.txt
│   │   └── wordrank.txt
│   ├── data_utils.py
│   ├── __init__.py
│   ├── paths.py
│   ├── plan.py
│   ├── poems.py
│   ├── rank_words.py
│   ├── raw
│   │   ├── ming.all
│   │   ├── pinyin.txt
│   │   ├── poem_1031k.txt
│   │   ├── qing.all
│   │   ├── qsc_tab.txt
│   │   ├── qss_tab.txt
│   │   ├── qtais_tab.txt
│   │   ├── qts_tab.txt
│   │   ├── shixuehanying.txt
│   │   ├── stopwords.txt
│   │   └── yuan.all
│   ├── save
│   │   ├── ancient_model_5.bin
│   │   └── sgns.baidubaike.bigram-char
│   └── segment.py
├── predict.py
├── resource
│   ├── dataset
│   │   ├── poem_1031k_theme.txt
│   │   ├── split_dataset.py
│   │   ├── test_1031k.txt
│   │   ├── train_1031k.txt
│   │   └── testset.txt
│   ├── word_dict.json
│   └── word_emb.json
├── result
│   └── result_05-14_Seq2seq_epoch=6_loss=130.8.txt
├── train.py
└── word_emb.py



