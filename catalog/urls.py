from django.urls import path
from catalog.views import ProductListView, ProductDetail
from django.conf.urls.static import static
from django.conf import settings
app_name = 'catalog'

urlpatterns = [
    path('<str:category_slug>/<slug:product_slug>/', ProductDetail.as_view(), name='product_detail',),
    path('<str:category_slug>/', ProductListView.as_view(), name='product_list_by_category',),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
