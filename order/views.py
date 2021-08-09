from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
# Create your views here.
from .forms import OrderCreateForm, OrderFormWithOutQuantity
from .models import  OrderItem, Order
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from cart.cart import Cart
from delivery.models import Wilaya, Commune
def order_create_one_product(request,product_id=None):
    form = OrderCreateForm()
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        form = OrderCreateForm(request.POST)
        print(
                'le FORMULAIRE', form
                )
        if form.is_valid():
            cd = form.cleaned_data
            quantity=cd['quantity']
            order = form.save()
            print('le formulaire est valid', quantity)
            # print('ORDER ITEM', order.quantity)
            OrderItem.objects.create(order=order,product=product,price=product.price,quantity=quantity)
                # order_created.delay(order.id)
                # order = Order.objects.get(id=order_id)
                # subject = f'Commande N°: {order.id}'
                # message = f'Chére {order.first_name},\n\n' \
                #         f'vous avez passer une commande avec succés' \
                #         f'votre identifiant de commande est le: {order.id}'
                # mail_sent = send_mail(subject, message, 'inter.taki@gmail.com',[order.email])
            return render(request, 'created.html', {'order': order})
            # print('ORDER ITEM')
            # return render(request, 'created.html', {'order': order})
        else:
            # print('yhnooo')
            return redirect(reverse('main:IndexView'))
    return render(request, 'product-detail.html', { 'form' : form})




def order_create(request):
    cart = Cart(request)
    wilayas= Wilaya.objects.all().order_by('name') 
    form = OrderFormWithOutQuantity()
    print('INIT FORM', OrderFormWithOutQuantity())
    if cart.__len__() :
        print('request', request.method)
        if request.method == 'POST':
            form = OrderFormWithOutQuantity(request.POST)
            if form.is_valid():
                print('le formulaire est valid')
                order = form.save()
                # try:
                print('carte ========>',cart)
                for item in cart:
                    OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
                cart.clear()
                return render(request, 'created.html', {'order': order})
    else: 
        return redirect(reverse('main:IndexView'))
    return render(request, 'create.html', {'cart':cart, 'form' : form, 'wilayas': wilayas})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order_pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    # weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    # # ajouter le style plus t ard erreur ???
    # weasyprint.HTML(string=html).write_pdf(response)
    return response


