<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/aminhbl/news-search-engine">
    <!-- <img src="pic/robot.png" alt="Logo" width="80" height="80"> -->
  </a>

<h2 align="center">News Search Engine</h2>

  <p align="center">
    Search engine to retrieve Persian news articles
    <br />
    <a href="https://github.com/aminhbl/news-search-engine">GitHub Page</a>
    <br/>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Searching for news articles can be a headache when you're looking for news related to a specific phrase or words in a large corpus. Here we implement concepts of `Information Retrieval` to propose a search engine with both `Positional Indexing` and `Vector Space` model on a corpuse of 12k Persian news articles to retrieve documents based on phrases and must_not queries.

The `Positional Indexing` model includes the following conponents:
* Preprocessing module for news articles
* Positional indexing module
* Query processing module
* Graph for Zipf's and Heap's law

The `Vector Space` model includes the following components:
* TF-IDF weight for each document calculated from the previous positional indexing
* Similarity module to compute the `Cosine Similarity` for each document and query vector
* Implementation of `Index Elimination` and `Champion List` to reduce the query process time



<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

[M. Amin Habibollah](https://github.com/aminhbl)
<br/>
Email: amin.habibllh@gmail.com
<br/>
Project Link: [https://github.com/aminhbl/news-search-engine](https://github.com/aminhbl/news-search-engine)
<br/>
<br/>
[![LinkedIn][linkedin-shield]][linkedin-url]
<p align="right">(<a href="#top">back to top</a>)</p>


[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/amin-habibllh/