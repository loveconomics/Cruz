# Cruz

# Datasets 
Ranked_DF.csv = Dataset with two additional columns ['RANK'] and ['REASONING'].
['RANK'] is a numerical value from 1-5 determined by Gemini.
1 = Low DEI
3 = Medium DEI
5 = High DEI
['REASONING'] AI explanation of ranking 

robustness.csv = 50 random samples from original dataframe to compare ['RANK'] 
i.e., if RANK is sensitive to the model 

# Code
gemini_classifier.py = Categorizes the data based on the column ['AWARD DESCRIPTIONS'].
Gemini reads this column and the assigns it a rank and short description as to why.

Cruz.ipynd = performs data analysis on results 
