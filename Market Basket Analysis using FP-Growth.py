import numpy as np 
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Read the dataset
df = pd.read_excel('groceries.xlsx', header=None)


# Display the size of the dataset
nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns')

# Fill NaN values
df.fillna(0)

# Display the dataset
df.sample(10)

# Get unique items
items = df[0].unique()
for i in items:
    print(i)

# Encoding values
encoded_vals = []
for index, row in df.iterrows():
    labels = {}
    uncommons = list(set(items) - set(row))
    commons = list(set(items).intersection(row))
    for uc in uncommons:
        labels[uc] = 0
    for com in commons:
        labels[com] = 1
    encoded_vals.append(labels)
encod_df = pd.DataFrame(encoded_vals)

# Call fpgrowth
boolean_df = encod_df.astype(bool)
freq_items = fpgrowth(boolean_df, min_support=0.005, use_colnames=True)

# Top 15 most frequent items
most_popular_items = freq_items.sort_values('support', ascending=False).head(15)

# Plot the most popular items
plt.rcParams['figure.figsize'] = (10, 10)
most_popular_items.plot.bar('itemsets', 'support', color='Orange')
plt.xlabel('Item Name', fontsize=15)
plt.ylabel('Support Count', fontsize=15)
plt.title('Most Popular Items (as per Support)', fontsize=30)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()

# Association rules based on confidence
rules = association_rules(freq_items, metric="confidence", min_threshold=0.05)
a_confi_top = rules.sort_values('confidence', ascending=False).head(100)

# Plot the first most popular items
plt.rcParams['figure.figsize'] = (20, 10)
color = plt.cm.autumn(np.linspace(0, 1, 40))
df[0].value_counts().head(40).plot.bar(color=color)
plt.title('First Most popular items', fontsize=25)
plt.xticks(rotation=90, fontsize=15)
plt.yticks(fontsize=15)
plt.show()

# Word cloud for most popular items
plt.rcParams['figure.figsize'] = (10, 10)
wordcloud = WordCloud(background_color='lightgreen', width=1500, height=1500, max_words=121).generate(str(most_popular_items))
plt.imshow(wordcloud)
plt.axis('off')
plt.title('Most Popular Items', fontsize=15)
plt.show()

# Write to Excel file
try:
    with pd.ExcelWriter('Display.xlsx') as writer:
        a_confi_top.drop(['antecedent support', 'consequent support', 'leverage', 'conviction'], axis=1).head(100).to_excel(writer, index=False)
        print("Data written successfully to 'Display.xlsx'")
except Exception as e:
    print("An error occurred:", e)

# Additional association rules
a_confi_top = association_rules(freq_items, metric='confidence', min_threshold=0.2).sort_values('confidence', ascending=False).head(10)
a_supp_top = association_rules(freq_items, metric='support', min_threshold=0.05).sort_values('support', ascending=False).head()
a_lift_top = association_rules(freq_items, metric='lift', min_threshold=3).sort_values('lift', ascending=False).head(20)
