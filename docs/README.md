---
layout: home
permalink: index.html

# Please update this with your repository name and title
repository-name: e20-co543-ProVision
title: Pro Vision
---

[comment]: # "This is the standard layout for the project, but you can clean this and use your own template"

# Pro Vision

---

<!-- 
This is a sample image, to show how to add images to your page. To learn more options, please refer [this](https://projects.ce.pdn.ac.lk/docs/faq/how-to-add-an-image/)

![Sample Image](./images/sample.png)
 -->

## Team
-  E20084, Dissanayake P.D.,e20084@eng.pdn.ac.lk <br>
-  E20032, BANDARA A.M.N.C.,e20032@eng.pdn.ac.lk <br>
-  E20034, BANDARA G.M.M.R.,e20034@eng.pdn.ac.lk <br>
-  E20157, JANAKANTHA S.M.B.G.,e20157@eng.pdn.ac.lk <br>

## Table of Contents
1. [Introduction](#introduction)
2. [Problem Statement](#Problem-Statement )
3. [Objectives](#Objectives)
4. [Methodology I](#Methodology-I)
5. [Methodology II](#Methodology-II)
6. [REFERENCES](#REFERENCES)
7. [Links](#links)

---

## Introduction

 Pro Vision is a project focused on removing weather effects like rain, fog, haze, and snow from
images to restore their quality and detail.. Traditional image processing methods fall short,
making this enhancement crucial for applications such as autonomous driving, surveillance
systems, outdoor vision-dependent systems, and satellite imaging.goal of this project is to restore
the image quality by removing the weather effects

## Problem Statement

Due to bad weather conditions obscuring key details in images, reducing the contrast and clarity
and also adding noise and artifacts, the visual and logical output from the image is poor. Hence
the reliability is not ensured;analysis is therefore redundant in many cases. The purpose of this
project is to address this problem domain

## Objectives
Main Goal of this project is to produce clean and clear images by removing weather effects
which degrade the image quality in the means of a robust method
● Ensure solutions work for multiple weather conditions (general method)
● Create an efficient system for real-time and large-scale applications.
● Integrate advanced algorithms for optimal results.


## Methodology I
Physics-Based Approach

   ● Overview:Involves modeling and estimating physical parameters like transmission maps, atmospheric light, and   scene radiance to restore weather-degraded images.
● Key Parameters:
      ○ Observed image
      ○ Transmission map (light attenuation due to weather)
      ○ Atmospheric light (scattered light from the medium)
● Steps:
      ○ Estimate transmission map using DCP (Dark Channel Prior).
      ○ Estimate atmospheric light.
      ○ Restore image using a predefined formula.
      ○ Apply post-processing for contrast enhancement.
1
● Challenges:
      ○ Estimation Accuracy: Requires precise estimation of transmission         maps and atmospheric light.
      ○ Severe Weather Limitations: Struggles with extreme conditions            without advanced techniques.


## Methodology II 

Specific Weather Condition Methods
Overview:
Tailored implementations for specific weather effects, optimizing results for unique conditions.
● Characteristics:
      ○ Provides more efficient outputs.
      ○ Optimized for intended weather conditions.
      ○ Requires more computational power.

  | Weather Condition | Proposed approaches | Challenges  |
| ------------- |:---------:|:----------:|
| Rain   |CNN, GAN, Image Decomposition|Data needs, model complexity,real-time issues| 
| ------------- |:---------:|:----------:|
|Haze  | L0 gradient, Dictionary Learning,Guided Filtering |Sparse representation, training,scalability | 
| ------------- |:---------:|:----------:|-------:|
| Snow | Contrast Restoration, Multi-ScaleCNN, Histogram Stretching| Physical models, parametersensitivity,computational load | 

       

##


##


##

## Links

- [Project Repository](https://github.com/cepdnaclk/e20-co543-ProVision/)
- [Project Page](https://cepdnaclk.github.io/e20-co543-ProVision/)
- [Department of Computer Engineering](http://www.ce.pdn.ac.lk/)
- [University of Peradeniya](https://eng.pdn.ac.lk/)


[//]: # (Please refer this to learn more about Markdown syntax)
[//]: # (https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
