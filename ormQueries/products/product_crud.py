from .models import Product 
from django.db.models import Avg, Max
from django.db.models.functions import Length

class ProductCrud:
    @classmethod
    def get_all_products(cls):
        return Product.objects.all()

    @classmethod
    def find_by_model(cls, target_name):
        return Product.objects.get(model=target_name)

    @classmethod
    def last_record(cls):
        return Product.objects.last()

    @classmethod
    def by_rating(cls, target_rating):
        return Product.objects.filter(rating=target_rating)

    @classmethod
    def by_rating_range(cls, lower, upper):
        return Product.objects.filter(rating__range=(lower,upper))

    @classmethod
    def by_rating_and_color(cls, target_rating, target_color):
        return Product.objects.filter(rating=target_rating, color=target_color)
    
    @classmethod
    def by_rating_or_color(cls, target_rating, target_color):
        return Product.objects.filter(rating=target_rating) | Product.objects.filter(color=target_color)

    @classmethod
    def no_color_count(cls):
        products_with_no_color = Product.objects.filter(color=None)
        return products_with_no_color.count()

    @classmethod
    def below_price_or_above_rating(cls, target_price, target_rating):
        return Product.objects.filter(price_cents__range=(0, target_price)) | Product.objects.filter(rating__range=(target_rating, 100.0))

    @classmethod
    def ordered_by_category_alphabetical_order_and_then_price_decending(cls):
        return Product.objects.all().order_by('category', '-price_cents')

    @classmethod
    def products_by_manufacturer_with_name_like(cls, name):
        return Product.objects.filter(manufacturer__contains = name)

    @classmethod
    def manufacturer_names_for_query(cls, phrase):
        products = Product.objects.filter(manufacturer__contains = phrase)
        names = []
        for product in products:
            names.append(product.manufacturer)
        return names

    @classmethod
    def not_in_a_category(cls, target_category):
        return Product.objects.exclude(category=target_category)

    @classmethod
    def limited_not_in_a_category(cls, target_category, limit):
        all_products = Product.objects.exclude(category=target_category)
        return all_products[:limit]

    @classmethod
    def category_manufacturers(cls, target_category):
        products = Product.objects.filter(category=target_category)
        manufacturers = []
        for product in products:
            manufacturers.append(product.manufacturer)
        return manufacturers

    @classmethod
    def average_category_rating(cls, target_category):
        products_of_category = Product.objects.filter(category=target_category)
        return products_of_category.aggregate(Avg('rating'))

    @classmethod
    def greatest_price(cls):
        return Product.objects.aggregate(Max('price_cents'))

    @classmethod
    def longest_model_name(cls):
        # Aerodynamic Concrete Computer should be the longest name...
        sorted_models_by_model_length = Product.objects.all().order_by(Length('model').desc())
        query_ids = list(sorted_models_by_model_length.values_list('id', flat=True))
        return query_ids[0]

    @classmethod
    def ordered_by_model_length(cls):
        sorted_models_by_model_length = Product.objects.all().order_by(Length('model').asc())
        return sorted_models_by_model_length