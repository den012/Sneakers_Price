## Sneaker Price Prediction Model


Problem be fooled by fake market basdeon 3 


Exposing Market Misinformation: Understanding True Value with Critical Parameters

	1.	Line/Scatter Plot for Price Over Time (days_since_release vs. lowest_price_eur)
Why:
	•	Key Insight: This plot reveals the lifecycle of a sneaker’s market value, capturing early trends like price drops after release (hype deflation) and later price surges due to rarity (scarcity effect).
	•	Market Behavior Visualization: Sneaker prices often exhibit a “hype curve,” where initial resale values drop after the first wave of purchases and rise again as pairs become scarce. This plot visually conveys this.
	•	Actionable Insights: Identifying the point where prices stabilize or surge could help expose artificial inflation, providing a foundation for discussing market manipulation.

	2.	Box Plot or Violin Plot for Collaboration Influence on Price (collaboration_name vs. lowest_price_eur)
Why:
	•	Distribution Clarity: Box plots show the spread, median, and outliers in price, making it easy to spot if collaboration significantly elevates prices. Violin plots add density estimation, showing where most prices cluster.
	•	Highlighting Premiums: Collaborations with big names like Travis Scott or Off-White often cause sharp price increases. If the plot shows consistent price premiums, it supports your hypothesis that collaborations drive resale value.
	•	Outlier Detection: Outliers may signal misinformation, hype inflation, or even backdooring practices, where sneakers are sold way above typical ranges.


	4.	Correlation Matrix Heatmap (Key Variables: days_since_release, retail_price_eur, collaboration, lowest_price_eur)
Why:
	•	Comprehensive Overview: A heatmap shows all pairwise correlations in a single visual, highlighting key relationships. If days_since_release or collaborations has a high correlation with price, it directly supports your hypothesis.
	•	Feature Selection: Helps determine which variables have the most predictive power for your machine learning models.
	•	Data-Driven Justification: Adds statistical rigor by identifying strong correlations (e.g., if collaborations correlates with higher prices, it’s evidence-backed).