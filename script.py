import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mac.settings'
django.setup()
import pandas as pd 
from shop.models import Products
from datetime import date


import csv 
def fill_db_with_flipkart_com():
    csv_file_path = 'flipkart_com-ecommerce_sample.csv' 

    with open(csv_file_path, mode='r' , encoding='utf-8') as file:
        render = csv.DictReader(file)
        for row in render:
                try:
                    product_name = row['product_name']
                    product_image = eval(row['image'])[0]
                    description = row['description']
                    category = row['product_category_tree'].split('>>')[0].strip('[]"')
                    price = row['retail_price']
                    
                    # print(product_image,product_image,description,category,price)
                    Products.objects.update_or_create(
                    product_name = product_name,
                    defaults={
                    'image' : product_image,
                    'desc' : description,
                    'category' : category,
                    'product_price' : price,
                    'publish_date' : date.today()}
                    )
                    print('Data inserted successfully \n\n\n\n\n')
                except Exception as e:
                    print(e)
fill_db_with_flipkart_com()
                    
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from shop.models import Products

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
    
    
print(get_similer_products(3))