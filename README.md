# Improving Factuality and Reasoning in Language Models through Multiagent Debate

### [Project Page](https://composable-models.github.io/llm_debate/) | [Paper](https://composable-models.github.io/llm_debate/llm_debate.pdf) 

[Yilun Du](https://yilundu.github.io/),
[Shuang Li](https://people.csail.mit.edu/lishuang/),
[Antonio Torralba](https://groups.csail.mit.edu/vision/torralbalab),
[Joshua B. Tenenbaum](https://scholar.google.com/citations?user=rRJ9wTJMUB8C&hl=en)
[Igor Mordatch](https://scholar.google.com/citations?user=Vzr1RukAAAAJ&hl=en)

This is a preliminary implementation of the paper "Improving Factuality and Reasoning in Language Models through Multiagent Debate". More tasks and settings will be released soon


## Running experiments

The code for running arithmetic, GSM, biographies, and MMLU tasks may be found in the following subfolders

* ./math/ contains code loading data
* ./gsm/ contains code to download Realestate10k and ACID datasets
* ./biography/ contains code for different utility functions on the dataset
* ./mmlu/ contains code for estimate the pose between two images using superpoint
