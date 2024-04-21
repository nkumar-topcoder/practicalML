# Simple cluster classification example

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def cluster_classification():
    # Example data: Different characteristics of products
    data = {
        'product': ["laptop", "smartphone", "tablet", "headphones", "smartwatch", "camera", "gaming console", "speaker", "router"],
        'price': [1000, 800, 500, 200, 300, 600, 400, 150, 100],
        'weight': [2.5, 0.3, 0.5, 0.1, 0.2, 0.8, 3.0, 0.5, 0.2],
        #'category': ["electronics", "electronics", "electronics", "electronics", "electronics", "electronics", "electronics", "electronics", "electronics"]
        'category': ["electronics", "electronics", "electronics", "electronics_accessary", "electronics", "electronics", "electronics", "electronics_accessary", "electronics_accessary"]
    }

    # Display the data in the form of a table
    df = pd.DataFrame(data)
    print("Original Data:")
    print(df)

    # One-hot encode categorical variables (not necessary in this case)
    # df_encoded = pd.get_dummies(df)
    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=4, random_state=42)  # You can set the number of clusters as per your requirement
    kmeans.fit(df[['price', 'weight']])  # Considering only 'price' and 'weight' for clustering

    # Assign clusters back to the original dataframe
    df['cluster'] = kmeans.labels_

    # Plotting the clustering graph
    plt.figure(figsize=(8, 6))
    plt.scatter(df['price'], df['weight'], c=df['cluster'], cmap='viridis')
    plt.title('Product Clustering')
    plt.xlabel('Price')
    plt.ylabel('Weight')
    plt.colorbar(label='Cluster')
    plt.grid(True)
    plt.show()
    
    return df

result = cluster_classification()
print("\nClustered Data:")
print(result)
