from django.shortcuts import render
from .models import Product ,Category,Cart,Comment
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView,DetailView,View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import CommentForm

class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(published_at__lte=timezone.now()).order_by('-published_at')
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        related_by_category = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

        related_by_tags = Product.objects.filter(tag__in=product.tag.all()).exclude(id=product.id).distinct()[:4]

        related_products = (related_by_category | related_by_tags).distinct()

        context['related_products'] = related_products
        context["comments"] = product.comments.all().order_by("-created_at")
        context["comment_form"] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = self.object

        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.user = request.user
                comment.save()
                return redirect("product-detail", pk=product.id)
        return self.get(request, *args, **kwargs)

class CategoryProductListView(ListView):
    model = Product
    template_name = "home.html"  # reuse home.html for category listing
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(
            category_id=category_id,
            published_at__lte=timezone.now()
        ).order_by('-published_at')

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        # Show cart items
        cart_items = Cart.objects.filter(user=request.user).order_by('-id')
        total = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

    def post(self, request):
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')  
        quantity = int(quantity) if quantity else 1  

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            if action == 'add':
                cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
                if not created:
                    cart_item.quantity += quantity  # add the requested quantity
                else:
                    cart_item.quantity = quantity  # set quantity for new item
                cart_item.save()
            elif action == 'remove':
                cart_item = get_object_or_404(Cart, user=request.user, product=product)
                cart_item.delete()

        return redirect(request.META.get('HTTP_REFERER', '/'))
 

class SearchResultsView(ListView):
    model = Product
    template_name = "home.html"   # reuse home.html
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Product.objects.filter(
                name__icontains=query
            ) | Product.objects.filter(
                description__icontains=query
            )
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = '/accounts/login/'