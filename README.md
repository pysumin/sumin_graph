# sumin_graph
revolutionary pcp graph!

plotly probides two kinds of parallel graph.
Parallel coordinates plot and Parallel cartegorical plot.
Parallel coordinates plot deals with numbers and Parallel cartegorical plot deals with categories.

But, dataframe usually contains both kind of columns, and pcp graph fails.

I had been searched how to add categorical columns to pcp graph with numbers for a long long time.
There were some answers, but they were not enough.
So, I made one by myself.

Now, I'm really pleased to introduce my own solution because this methode probably can help many people and I think that this solution is giving back to those who helped me through stackoverflow.

My idea is simple.
Adding categorical data to group of numerical columns is hard and express less information.
If we convert numerical columns into categorical data, that means a lot.

Long story short, following graph satisfied me 100%.
