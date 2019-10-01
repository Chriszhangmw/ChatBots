ChatBots
===========================
some projects for chatbots 

****
	
|Author|Chris Zhang|
|---|---
|E-mail|zhangmw_play@163.com


****
## content
* [phone_comments_classification](#phone_comments_classification)
* [atec_sentence_similarity](#atec_sentence_similarity)
* [NER_Medical](#NER_Medical)

phone_comments_classification
-----------
### Introduction
With the rapid expansion of e-commerce, more and more cellphones are sold on the web, like the web platform Amazon around the world and Taobao in china. However, how to satisfy all kinds of customers needs and meet all kinds of after-sales problem are curtail for the company like apple, Huawei and so on. Not only for the cell phone manufacturers , but for the platform suppliers. So, we can see lots of companies decide to build some customer service department which is to solve all kinds of after-sales problem about their phones. And the department are also responsible to collect the market information for their product research team. 
The number of comments about the online products grow rapidly for the increasing number of user becoming comfortable with the web. So, how to keep track of customer attitude of the phone is important to the phone suppliers. On the other hand, it will help other potential customers to make an informed decision.
### Aim
This project we are going to analysis the comments from Taobao platform which come from china, and finally we get about 7000 comments which have labels from Taobao customer service department. And this project wants to do some sentiment analysis.
In other words, if cell phone companies do some sentiment analysis based on customers comments, it will help them to response quickly to the market. What’s more important is that the sentiment analysis will help their staff service get the attitude of the customer before the call goes through, and it will definitely improve their customer service level
### Related work
This project will take the aim as a sentence classification problem, because the comments are all unstructured sentence, they are not always in the same length, but their labels belong to a fixed set. The dataset has its own label, so, we should consider some supervise learning method to build our system.
With the development of machine learning these years, sentence classification problem is hot in natural language processing area, we can see our predecessor tried to some language model to do that, such as N-gram. and with the development of embedding method, we can choose like word2vec, Glove or Elmo instead of tf-idf to do the embedding. 
How to correctly represent the word vector and consider the relationship between words and context is one of the difficult points of NLP research. Fortunately, we see that the BERT based on the mask model is proposed to more accurately combine the vector representation of the word
### results:
![1](https://raw.github.com/Chriszhangmw/ChatBots/master/phone_comments_classification/loss.png)
![2](https://raw.github.com/Chriszhangmw/ChatBots/master/phone_comments_classification/myplot22.png)
### References：
1.	Mining and Summarizing Customer Reviews
2.	BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
3.	Distributed Representations of Words and Phrases and their Compositionality

