[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)    
[![Npm package license](https://badgen.net/npm/license/discord.js)](https://npmjs.com/package/discord.js) [![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)

# K-Anonymization Tool for databases

## Authors

- Louis Tochon
- Kevin Huguenin (Superviser)

## Table of contents
* [Arborescence des fichiers](#arborescence-des-fichiers)
* [Goal](#goal)
* [Description of the project](#description-of-the-project)
* [Milestones](#milestones)
* [Sources](#sources)

## Arborescence des fichiers

Les fichiers omis sont des fichiers internes aux programmes utilisés et ne devraient pas être modifiés.

```C
📦k-ano_Tool
 ┣ 📂Flask project //First Flask project to gain knowledge
 ┣ 📂K-anoTool //Flask project with the anonimization tool
 ┃ ┣ 📂Static //Static files (JS, CSS, IMG, Saved files)
 ┃ ┣ 📂Templates //HTML Templates
 ┃ ┣ 📂Upload //Sub-directory for Upload part of the project
 ┃ ┗ 📜app.py //launch project file
 ┣ 📂Sources //Folder to save sources that have been used
 ┣ 📂Test_algo //Algorithm's development folder
 ┃ ┣ 📂data
 ┃ ┣ 📜incognito.v1 //First try with incognito algorithm
 ┣ 📜LICENSE
 ┗ 📜README.md
```
## Goal

The main goal of this project is to provide an anonymization tool to k-anonymize a database with algorithms based on weights for each attribute and to implement a tool to easily create the wanted tree of generalization. 

## Description of the project

The algorithm called *Datafly* is an algorithm for providing anonymity in medical data [[1](https://en.wikipedia.org/wiki/Datafly_algorithm)]. This algorithm is based on a greedy approach and global generalization with tuples suppression [[2](http://www.mathcs.emory.edu/~lxiong/cs573_s12/share/slides/03anonymity_generalization.pdf)]. The goal will be to use this algorithm to provide k-anonymity of a dataset by incorporating weights on the attributes to evaluate the importance of each one of them. Indeed, the main purpose of this project is to allow the user to choose which one of the different attributes must be generalized first and on the opposite side, which one must not be generalized. 

This anonymization algorithm will be deployed on a web application written in Python through the framework *Flask*. 

In a second time, an interface on the same web application will be created to provide a tool to the user to easily create his own tree of generalization. 

The crucial point of this project is to do a user-friendly tool with easy interactions to make the experience as simple as possible.

This project will focus on the medical domain to handle a single use case and go as deep as possible to provide a complete tool.

## Milestones

(:heavy_check_mark: : Done | :hourglass_flowing_sand: : In Progress | :x: : Canceled)

1) Research about the *Datafly* algorithm :hourglass_flowing_sand:
2) Gaining knowledge about Flask (first web application with Python) :hourglass_flowing_sand:
3) Implementing *Datafly* algorithm
4) Algorithm's proposal with weighted attributes
5) Implementation of Flask application with the algorithm
6) Prototyping the interface of custom generalization
7) Prototype testing
8) Implementation of the generalization's interface
9) Final application's usability tests

## Sources

weight algo k-anon [28.02] : https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6663954

weight k-ano [28.01] : https://www.sciencedirect.com/science/article/pii/S0167404820300377

Mondrian [01.03] : https://personal.utdallas.edu/~muratk/courses/privacy08f_files/MultiDim.pdf

Incognito explained [01.03] : https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6406297

Datafly explained [03.03] : http://www.mathcs.emory.edu/~lxiong/cs573_s12/share/slides/03anonymity_generalization.pdf

Datafly wikipédia [03.03] : https://en.wikipedia.org/wiki/Datafly_algorithm
