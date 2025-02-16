import numpy as np

def knn_precision_at_k(actual, recommended, k):
    return len(set(actual) & set(recommended[:k])) / k

def knn_recall_at_k(actual, recommended, k):
    return len(set(actual) & set(recommended[:k])) / len(actual) if actual else 0

def knn_mean_reciprocal_rank(actual, recommended):
    for i, item in enumerate(recommended, start=1):
        if item in actual:
            return 1 / i
    return 0

def knn_ndcg_at_k(actual, recommended, k):
    ideal_dcg = sum(1.0 / np.log2(i + 2) for i in range(min(len(actual), k)))
    dcg = sum((1.0 / np.log2(i + 2)) if recommended[i] in actual else 0 for i in range(k))
    return dcg / ideal_dcg if ideal_dcg > 0 else 0

def svd_precision_at_k(actual, recommended, k):
    recommended_items = recommended.sort_values(ascending=False).head(k).index
    actual_relevant = set(actual[actual >= 0].index)
    intersection = len(actual_relevant & set(recommended_items))
    return intersection / k if k > 0 else 0

def svd_recall_at_k(actual, recommended, k):
    recommended_items = recommended.sort_values(ascending=False).head(k).index
    actual_relevant = set(actual[actual >= 0].index)
    intersection = len(actual_relevant & set(recommended_items))
    return intersection / len(actual_relevant) if len(actual_relevant) > 0 else 0


def svd_mrr(predictions, actual, k=50):
    relevant_items = set(actual[actual >= 1].index)  
    sorted_predictions = predictions.sort_values(ascending=False)
    
    for i, item in enumerate(sorted_predictions.head(k).index):
        if item in relevant_items:
            return 1 / (i + 1) 
    return 0


def svd_ndcg_at_k(actual, recommended, k):
    ideal_relevances = sorted([r for r in actual if r > 0], reverse=True)
    ideal_dcg = sum((2 ** r - 1) / np.log2(i + 2) for i, r in enumerate(ideal_relevances[:k]))

    dcg = 0

    for i in range(k):
        product = recommended.index[i]
        if product in actual.index and actual[product] > 0:
            relevance = actual[product]
            dcg += (2 ** relevance - 1) / np.log2(i + 2)

    return dcg / ideal_dcg if ideal_dcg > 0 else 0

