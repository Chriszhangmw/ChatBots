# atec_NLP_chatbot  dataset from:
https://dc.cloud.alipay.com/index#/topic/intro?id=3


## Content   
```
project
│   README.md
│      
│
└───data/ word vectors
│   │ 
│   └───data/ trainiing data set
│   │
│   └───log_dir/ log file
│   │
│   │
│   └───share/  offline training file and online submission
│       └─── jieba/ cutting words and stop words
|       |
│       └─── mv_w2v/ traning word vector
|       |
│       └─── single/ single model
|       |
|       └─── stack/ cv model and other files
│   
└───model/
│   │  all kinds of model
│   │   
└───feature/
│   │  extract some features
│   │   
└───submit/
│   │  offline submit
│   │   
└───util/
│   │  tools
│   │   
    
    
```




## sun instructions：    
parameters are in util/config.py

python util/CutWord.py (the time of first time)
python  util/w2v.py  

python train.py cv  cnn1  





## some records
0612 fix cv bugs offline 数据扩充5 cv  CNN :  0.63407952549263558
0.6155
0613 fix cv bugs offline 数据扩充5 cv ESIM :  0.65816989095636136


0626 CNN CV NO 数据扩充  26个特征：
n :', 0.52228330874667162, 0.52633540429317449, 0.52415987274990683


0629 add checkpoint and best model earlystop and change lr
'mean :', 0.45830773149153237, 0.67153672904068951, 0.54450204294307059)
ON LINE :0.6206
