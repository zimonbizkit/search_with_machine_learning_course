### For query classification:

1. How many unique categories did you see in your rolled up training data when you set the minimum number of queries per category to 1000? To 10000?

_I was able to see a minimum of 388 categories with a default number of queries per category to 1000, 70 (!) with a minimum number of 10K queries per category_

3. What were the best values you achieved for R@1, R@3, and R@5? You should have tried at least a few different models, varying the minimum number of queries per category, as well as trying different fastText parameters or query normalization. Report at least 2 of your runs.

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


### For integrating query classification with search: 
1. Give 2 or 3 examples of queries where you saw a dramatic positive change in the results because of filtering. Make sure to include the classifier output for those queries.

- After putting the best classifier above with a probability threshold of 0.5, with the query
    - **xbox**: we went from 3563 aggressively to just 69! The results were very positive as literally xbox filtered to the category  “videogames and consoles” . Thus, the results were just xbox consoles and bundles of the console, taking out games and peripherals. Probability score output, categories and scores:
    `['__label__abcat0701001', '__label__abcat0700000', '__label__abcat0715001', '__label__abcat0715002', '__label__cat02724']`
    `[0.51762199 0.14868429 0.09926192 0.02738438 0.02623567]`

    - **Ps4**: the same effect as above, filtering down to the consoles category, from 1170 results to just 15. Probability scores 👇🏻
    `['__label__cat02015', '__label__cat02009', '__label__cat09000', '__label__cat02001', '__label__abcat0900000']`
    `[0.69825941 0.04239719 0.03412125 0.02841064 0.02170236]`
 
      
3. Give 2 or 3 examples of queries where filtering hurt the results, either because the classifier was wrong or for some other reason:
- With the configuration above (probability treshold to 0.5), harmed queries were
    - iphone: went from 3241 results to just 776, but their results were not _literally_ iPhone devices, but rather accessories to them.
    `['__label__abcat0811002', '__label__pcmcat209400050001', '__label__abcat0208011', '__label__pcmcat201900050009', '__label__abcat0208007']`
    `[0.58636183 0.23716259 0.02968958 0.02421849 0.01961429]`

        
    - dress: from 633 results to 69, but again no correct filtering by the correct category. The results were mostly movies in various formats
    `['__label__cat02015', '__label__cat02009', '__label__cat09000', '__label__cat02001', '__label__abcat0900000']`
    `[0.6951161  0.04240536 0.03508785 0.0285547  0.02147051]`
