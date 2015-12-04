# Bomoda-Weibo-Project
In this project, I mainly used mrjob module in Python to perform the word count tasks on sina weibo dataset. For each questions, I merged all of the json files in each of the weibo folder to a single json file (`merged_status.json,merged_comment.json,merged_repost.json`). The output results are written in .txt files in each of the question folders.




##Questions

* Word count I: 
  a: Count the number of posts mentioning each of the included brand names as well as the users who mentioned them. Hint: Pay attention to the variation of names. 
  b: List the top 10 users and locations (as province level in China and nation level worldwide) for total posts.

* Word count II: 
  a: Find the date that has the highest number of posts mentioning each of the brands
  b: Find the peak hour with the most posts. 

* Word count III: 
  Tokenize the comments and retrieve the top 10 mentioned Chinese terms associated with each brand from the texts. You may use 3rd party libraries such as Jieba to complete this task.

* Count & Visualize:
  a: Count the number of reposts and comments per day (as separate counts), per brand.
  b: Plot the count over the entire timeframe.

* Sampling: 
  Explain possible sampling bias through Weibo, such as gender bias, etc.

* What are some possible algorithms to identify users who showed interest in Michael Kors over Kate Spade? What are some data points that can be used to illustrate the algorithm's utility? Give a couple examples and discuss pros and cons.
