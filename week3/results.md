### For query classification:
    1. How many unique categories did you see in your rolled up training data when you set the minimum number of queries per category to 1000? To 10000?
    ```
    I was able to see a minimum of 388 categories with a default number of queries per category to 1000, 70 (!) with a minimum number of 10K queries per category


    2. What were the best values you achieved for R@1, R@3, and R@5? 
    ```
    You should have tried at least a few different models, varying the minimum number of queries per category, as well as trying different fastText parameters or query normalization. Report at least 2 of your runs.

        - With a minimum of 1K minimum queries per category, I was able to reach  
            - R1@0.3  
            - R3@0.399 
            - R5@0.4
        - Only changing the minimum number of queries to 10K and not changing epochs and learning rate, I was able to push 
            - R1@0.399
            - R3@0.518
            - R5@0.58
        - Now, by pushing all parameters for fosttext learning (wordNgrams at 2, three epochs and learning rate at 1) I was able to achieve
            - R1@0.419
            - R3@0.607
            - R5@0.674



2. For integrating query classification with search: 
### TODO
    1. Give 2 or 3 examples of queries where you saw a dramatic positive change in the results because of filtering. Make sure to include the classifier output for those queries.
    2. Give 2 or 3 examples of queries where filtering hurt the results, either because the classifier was wrong or for some other