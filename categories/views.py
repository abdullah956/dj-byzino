from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from categories.models import Category, Product, Review
from django.db.models import Avg
from django.core.paginator import Paginator

def products_view(request):
    products = Product.objects.annotate(
        average_rating=Avg('review__stars')
    )
    return render(request, 'categories/shop.html', {'products': products})


def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('stars'))['stars__avg']

    paginator = Paginator(reviews, 3)
    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    context = {
        'product': product,
        'reviews': page_reviews,
        'average_rating': average_rating,
    }
    return render(request, 'categories/product_detail.html', context)


def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).annotate(
        average_rating=Avg('review__stars')
    )
    return render(request, 'categories/category_products.html', {'category': category, 'products': products})


@login_required(login_url='/login/')
def submit_review(request, product_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        review_text = request.POST.get('review_form_text')
        stars = int(request.POST.get('stars'))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return render(request, 'review_form.html', {'error': 'Product not found'})

        Review.objects.create(
            user=request.user,
            product=product,
            name=name,
            email=email,
            review=review_text,
            stars=stars
        )

        return redirect('product_detail', id=product_id)

    return redirect('product_detail', id=product_id)

