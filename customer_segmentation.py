import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

np.random.seed(42)

def create_customer_data():
    n = 200
    
    data = {
        'Customer_ID': [f'CUST_{i:04d}' for i in range(1, n+1)],
        'Age': np.random.randint(18, 65, n),
        'Annual_Income': np.random.randint(20000, 120000, n),
        'Spending_Score': np.random.randint(1, 100, n),
        'Purchase_Frequency': np.random.randint(1, 50, n),
        'Avg_Transaction': np.random.randint(10, 500, n)
    }
    
    for i in range(50):
        cluster = np.random.choice([0, 1, 2])
        if cluster == 0:
            data['Annual_Income'][i] += 30000
            data['Spending_Score'][i] += 20
        elif cluster == 1:
            data['Annual_Income'][i] -= 15000
            data['Spending_Score'][i] -= 15
        else:
            data['Annual_Income'][i] += 5000
            data['Spending_Score'][i] += 5
    
    return pd.DataFrame(data)

def analyze_elbow_method(X, max_clusters=10):
    inertias = []
    silhouette_scores = []
    
    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].plot(range(2, max_clusters + 1), inertias, 'bo-')
    axes[0].set_xlabel('Number of Clusters (k)')
    axes[0].set_ylabel('Inertia')
    axes[0].set_title('Elbow Method')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(range(2, max_clusters + 1), silhouette_scores, 'ro-')
    axes[1].set_xlabel('Number of Clusters (k)')
    axes[1].set_ylabel('Silhouette Score')
    axes[1].set_title('Silhouette Score Method')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return inertias, silhouette_scores

def perform_clustering(df):
    features = ['Age', 'Annual_Income', 'Spending_Score', 'Purchase_Frequency', 'Avg_Transaction']
    X = df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("\n[4] Determining Optimal Clusters:")
    inertias, silhouette_scores = analyze_elbow_method(X_scaled)
    
    optimal_k = np.argmax(silhouette_scores) + 2
    print(f"\n✅ Optimal clusters: {optimal_k}")
    print(f"   Best Silhouette Score: {max(silhouette_scores):.3f}")
    
    print("\n[5] Running K-Means Clustering...")
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    print(f"✅ Clustering complete!")
    print(f"   Cluster Distribution:")
    for cluster in sorted(df['Cluster'].unique()):
        count = len(df[df['Cluster'] == cluster])
        print(f"     Cluster {cluster}: {count} customers ({count/len(df)*100:.1f}%)")
    
    return df, kmeans, scaler, X_scaled

def analyze_clusters(df):
    print("\n[6] Cluster Analysis:")
    print("=" * 60)
    
    cluster_summary = df.groupby('Cluster').agg({
        'Age': 'mean',
        'Annual_Income': 'mean',
        'Spending_Score': 'mean',
        'Purchase_Frequency': 'mean',
        'Avg_Transaction': 'mean',
        'Customer_ID': 'count'
    }).round(2)
    
    cluster_summary.rename(columns={'Customer_ID': 'Count'}, inplace=True)
    print(cluster_summary)
    
    print("\n[7] Customer Personas:")
    print("=" * 60)
    
    for cluster in sorted(df['Cluster'].unique()):
        cluster_data = df[df['Cluster'] == cluster]
        avg_income = cluster_data['Annual_Income'].mean()
        avg_spending = cluster_data['Spending_Score'].mean()
        avg_age = cluster_data['Age'].mean()
        avg_freq = cluster_data['Purchase_Frequency'].mean()
        
        if avg_income > 80000 and avg_spending > 70:
            persona = "💎 Premium Spender"
            description = "High income, high spending. Luxury buyers."
        elif avg_income > 50000 and avg_spending > 60:
            persona = "🛍️ Regular Shopper"
            description = "Middle income, consistent spending. Brand loyal."
        elif avg_income > 50000 and avg_spending < 40:
            persona = "💰 Savvy Saver"
            description = "High income but low spending. Price sensitive."
        elif avg_income < 50000 and avg_spending > 60:
            persona = "🎯 Aspirational Buyer"
            description = "Lower income but high spending. Value seekers."
        elif avg_age > 45:
            persona = "👴 Senior Customer"
            description = "Older demographic. Prefers quality over quantity."
        else:
            persona = "🌟 Young Explorer"
            description = "Younger demographic. High potential for growth."
        
        print(f"\nCluster {cluster}: {persona}")
        print(f"   Count: {len(cluster_data)} customers")
        print(f"   Average Age: {avg_age:.1f}")
        print(f"   Average Income: ${avg_income:,.0f}")
        print(f"   Spending Score: {avg_spending:.1f}")
        print(f"   Description: {description}")

def visualize_clusters(df, X_scaled):
    print("\n[8] Visualizing Clusters (PCA)...")
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=df['Cluster'], cmap='viridis', s=50, alpha=0.7)
    axes[0].set_title('Customer Segments (PCA)')
    axes[0].set_xlabel('PCA Component 1')
    axes[0].set_ylabel('PCA Component 2')
    plt.colorbar(scatter, ax=axes[0])
    axes[0].grid(True, alpha=0.3)
    
    for cluster in sorted(df['Cluster'].unique()):
        cluster_data = X_pca[df['Cluster'] == cluster]
        center = cluster_data.mean(axis=0)
        axes[0].scatter(center[0], center[1], s=200, marker='X', edgecolors='black', linewidth=2)
    
    axes[1].bar(df['Cluster'].value_counts().index, df['Cluster'].value_counts().values, color='skyblue', edgecolor='black')
    axes[1].set_title('Cluster Distribution')
    axes[1].set_xlabel('Cluster')
    axes[1].set_ylabel('Number of Customers')
    
    plt.tight_layout()
    plt.show()

def main():
    print("\n" + "=" * 60)
    print("   UNSUPERVISED LEARNING - CUSTOMER SEGMENTATION")
    print("=" * 60)
    
    print("\n[1] Creating Customer Dataset...")
    df = create_customer_data()
    print(f"✅ {len(df)} customers loaded")
    print(f"   Columns: {', '.join(df.columns)}")
    
    print("\n[2] Dataset Preview:")
    print(df.head())
    
    print("\n[3] Dataset Statistics:")
    print(df.describe())
    
    df_clustered, kmeans, scaler, X_scaled = perform_clustering(df)
    
    analyze_clusters(df_clustered)
    
    visualize_clusters(df_clustered, X_scaled)
    
    print("\n[9] Business Recommendations:")
    print("=" * 60)
    
    recommendations = {
        0: "Target with premium products and personalized offers.",
        1: "Offer loyalty programs and bundle deals to increase retention.",
        2: "Send exclusive discounts and limited-time offers to boost spending.",
        3: "Focus on quality and value propositions rather than discounts."
    }
    
    for cluster in sorted(df_clustered['Cluster'].unique()):
        if cluster in recommendations:
            print(f"\nCluster {cluster}: {recommendations[cluster]}")
        else:
            print(f"\nCluster {cluster}: Continue monitoring and adjust marketing strategy.")
    
    print("\n" + "=" * 60)
    print("   CUSTOMER SEGMENTATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()