from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import connection
from catalog.forms import ReviewForm
from catalog.models import Product, Category
from django.shortcuts import render


class ProductListView(ListView):
    paginate_by = 12
    context_object_name = 'products_list'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug']
        )
        return Product.objects.filter(
            category__slug=self.category.slug
        ).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductDetail(DetailView):
    model = Product
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            initial_data = {
                'name': f"{self.request.user.first_name}",
            }
            context['form'] = ReviewForm(initial=initial_data, user=self.request.user)
        else:
            context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST, request.FILES, user=request.user)
        self.object = self.get_object()
        context = self.get_context_data()
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.product = self.object
            new_review.save()
        else:
            context['form'] = form

        return self.render_to_response(context=context)


