from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Products

def get_similer_products(product_id, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    product_description = Products.objects.all().values_list('desc', flat=True)
    tfid_matrix = vectorizer.fit_transform(product_description)
    target_product = Products.objects.get(id=product_id)
    all_products = list(Products.objects.all())
    target_index = all_products.index(target_product)
    cosine_simi = cosine_similarity(tfid_matrix[target_index], tfid_matrix).flatten()
    similer_indices = cosine_simi.argsort()[-top_n-1:-1][::-1]
    similer_indices = [i for i in similer_indices if i != target_index]
    similar_products = []
    for idx in similer_indices:
        similar_products.append(all_products[idx])
    return similar_products
    