# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import torch
import time
import os

import importlib
import configparser
import torch.utils.data as Data
from data_utils import read_test_data, get_keywords, read_eval_data

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print('device:', device)

######################################################################
# predict
# ==========

def predict(test_data, lines, targets, model, predict_param, ckpt_path, poem_type, cangtou, assign_yun):
    model.eval()
    context = ''
    for i, data in enumerate(test_data):
        # 每一步 loader 释放一小批数据用来学习，step=总数据量/batch_size，enumerate把每次提取编写索引。
        # batch_x: B*T tensor

        output_words = model.predict(data, cangtou, predict_param)
        
        output_words.insert(7, '/') # 改
        output_words.insert(15, '/')
        output_words.insert(23, '/')
        
        output_sentence = ''.join(output_words)
        context = context + lines[i] + ' ==== ' + output_sentence + '\n'
        print((i+1), lines[i], ' ==== ', output_sentence)
        if targets:
            print('target:', targets[i], '\n')
            context = context + targets[i] + '\n'
        
    # logs 
    file = 'result/result_' + ckpt_path.split('/')[1].split('.pkl')[0] + '.txt'
    with open(file, 'a', encoding='utf-8') as f:
        t = time.strftime("%m-%d", time.localtime())
        f.write(t)
        f.write('\n'+context+'\n')


def main():
    # ========= Get Parameter =========#
    conf = configparser.ConfigParser()
    conf.read('config/config.ini', encoding="utf-8-sig")

    model_name = conf.get('predict', 'model')
    ckpt_path = conf.get('predict', 'ckpt_path')
    test_set = conf.get('predict', 'test_set')
    eval_set = conf.get('predict', 'eval_set')
    use_planning = conf.get('predict', 'use_planning') == 'True'
    poem_type = conf.get('predict', 'poem_type')
    cangtou = conf.get('predict', 'cangtou')
    keywords = conf.get('predict', 'keywords')
    assign_yun = conf.get('predict', 'assign_yun')

    conf.read('config/config_'+model_name+'.ini')
    predict_param_li = conf.items('predict_param')
    predict_param = {}
    for item in predict_param_li:
        predict_param[item[0]] = item[1]

    # ========= Preparing Data =========#

    # read data
    targets = None
    if cangtou:
        test_set, lines = get_keywords(cangtou, use_planning)
    elif keywords:
        test_set, lines = get_keywords(keywords, use_planning)
    elif test_set:    
        test_set, lines = read_test_data(test_set, use_planning)
    else: # eval
        test_set, lines, targets = read_eval_data(eval_set, use_planning)
        
    # 实例化
    data_path = 'models.' + model_name + '.PoetryData'
    PoetryData = importlib.import_module(data_path)
    test_Dataset = getattr(PoetryData, 'PoetryData')(test_set, src_max_len=int(predict_param['input_max_len']), 
                                                     tgt_max_len=int(predict_param['target_max_len']), test=True)
    
    # 变成小批
    test_data = Data.DataLoader(
        dataset=test_Dataset,  # torch TensorDataset format
        batch_size=1,  
        shuffle=False,  
        # num_workers=2,  # 多线程来读数据，提取xy的时候几个数据一起提取
    )

    # ========= Preparing Model =========#
    if os.path.exists(ckpt_path):
        checkpoint = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
        model_param = checkpoint['model_param']
        
        model_path = 'models.' + model_name + '.' + model_name
        Model = importlib.import_module(model_path)  # 导入模块
        model = getattr(Model, model_name)(model_param)  # 反射并实例化
        print('model:', model)
        
        model.load_state_dict(checkpoint['model'])
        predict(test_data, lines, targets, model, predict_param, ckpt_path, poem_type, cangtou, assign_yun)
    else: 
        print('ckpt_path does not exist.')


if __name__ == '__main__':
    main()
    