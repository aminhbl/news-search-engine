<div id="top"></div>

<br />
<div align="center">
<h2 align="center">News Search Engine</h2>
  <p align="center">
    Search engine to retrieve Persian news articles
    <br>
    project of Information Retrieval course
  </p>
</div>

## Quick Links 
* [Overview](#overview)
* [Elasticsearch](#elasticsearch)

## Overview

Searching for news articles can be a headache when you're looking for news related to a specific phrase or words in a large corpus. Here we implement concepts of **Information Retrieval** to propose a search engine with both **Positional Indexing** and **Vector Space** models on a corpus of 12k Persian news articles to retrieve documents based on phrases and must_not queries.

The **Positional Indexing** model includes the following components:
* Preprocessing module for news articles
* Positional indexing module
* Query processing module
* Graph for Zipf's and Heap's law

The **Vector Space** model includes the following components:
* TF-IDF weight for each document calculated from the previous positional indexing
* Similarity module to compute the **Cosine Similarity** for each document and query vector
* Implementation of **Index Elimination** and **Champion List** to reduce the query process time

## Elasticsearch
To see the implementation of this project using Elasticsearch you can check [here](https://github.com/aminhbl/elasticsearch-news-engine).