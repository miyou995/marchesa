from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .forms import ContactForm
from delivery.models import Wilaya, Commune
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from .models import Product, Category, SubCategory, Photos
from cart.forms import CartAddProductForm



class IndexView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(actif=True, top=True)
        context["top_3"] = Category.objects.filter(actif=True)[:3]
        context["home_slide"] = Photos.objects.filter(actif=True, is_big=True)[:1]
        context["small_slide"] = Photos.objects.filter(actif=True, is_small=True)[:2]
        return context


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "Contact.html"




class CategoryProductsView(ListView):
    context_object_name = 'products'
    model = Product
    paginate_by = 15
    template_name = "products.html"

    def get_queryset(self, *args, **kwargs): # new
        
        products = Product.objects.filter(actif=True)
        try:
            category = get_object_or_404(Category, slug=self.kwargs['slug'])
            products = products.filter(sous_category__category=category)
        except:
            category = get_object_or_404(SubCategory, slug=self.kwargs['slug'])
            products = products.filter(sous_category=category)
        return products
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["sous_categories"] = SubCategory.objects.all()
        # context["products"] = Product.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related"] = Product.objects.all().order_by('?')[:4] 
        context["wilayas"] = Wilaya.objects.all().order_by('name') 
        return context

class ProductsView(ListView):
    context_object_name = 'products'
    model = Product
    paginate_by = 15
    template_name = "products.html"

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        min = self.request.GET.get('min')
        max = self.request.GET.get('max')
        new = self.request.GET.get('new')
        top = self.request.GET.get('top')
        if max and new and top:
            products = Product.objects.filter(price__range=[min, max], available=True, new= True, top=True)
        elif max and new:
            products = Product.objects.filter(price__range=[min, max], available=True,new= True)
        elif max and top:
            products = Product.objects.filter(price__range=[min, max], available=True, top=True)
        elif top and new:
            products = Product.objects.filter(available=True,new= True, top=True)
        elif max:
            products = Product.objects.filter(price__range=[min, max], available=True)
        elif new:
            products = Product.objects.filter(available=True,new= True)
        elif top:
            products = Product.objects.filter( available=True, top=True)
        elif query:
            if len(query) > 2:
                by_2 = [query[i:i+2] for i in range(0, len(query), 2)][0]
                by_1 = [query[i:i+2] for i in range(0, len(query), 2)][1:]
                print('the sring split one  ', by_2)
                print('the sring towo', by_1)
                for i in by_1:
                    products = Product.objects.filter(
                            Q(name__icontains=by_2) & Q(name__icontains=i)
                            )
                    if not len(products):
                        products = Product.objects.filter(
                            Q(name__icontains=by_2) | Q(name__icontains=i)
                            )
                # products = Product.objects.filter(name__regex=r'(?i)dragx[\s\w]+')
                # products = Product.objects.filter(name__icontains=by_2, name__icontains=by_1)# erreur
                # products = Product.objects.filter(name__icontains=query)
                    print('JE SUISS LAAAAAA EXCEPTIO N TXwO', products)
            else: 
                products = Product.objects.filter(name__icontains=query)
        else :
            products = Product.objects.all()
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["categories"] = Category.objects.all()
        context["sous_categories"] = SubCategory.objects.all()
        # context["products"] = Product.objects.all()
        return context


class ContactView(CreateView):
    template_name = 'contact.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
  
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
      
        message = 'Une erreur est survenue, veuillez réessayer.'
        success = False
        try:
            #save the form   
            if form.is_valid():
                form.save()
                #messages.success(request, 'Votre message a bien été envoyé')
                message = 'Votre message a bien été envoyé!'
                success = True
                print(success)
                return render(request, 'other/contact.html', {'message': message, 'success': success})
            else:
                print(success)
                message = 'Une erreur est survenue, veuillez réessayer.'
                return render(request, 'contact.html', {'message': message, 'failure': True})
        except:
            return render(request, 'contact.html', {'message': message, 'failure': True})
        return render(request, 'contact.html', {'message': message, 'failure': True})





# Create your views here.
def get_json_view(request):
    """Return request metadata to the user."""
    data = {
        'received_headers': dict(request.headers.items()),
        # 'client_cookies': request.COOKIES,
        'path': request.path
    }
    return JsonResponse(data)



