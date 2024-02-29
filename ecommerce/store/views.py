from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import*


# Store View
def store(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
           
    products=Product.objects.all()
    context = {
        'products':products, 'cartItems':cartItems
    }
    return render(request, 'pages/store.html', context)


# Cart View
def cart(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'pages/cart.html', context)


# Checkout View
def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
                  
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'pages/checkout.html', context)

    
# UpdateItem View
def updateItem(request):
    # if request.method == 'POST':
    data = json.loads(request.body)
    productId=data['productId']
    action = data['action']
    print('productId:', productId)
    print('action:',action)
        
    # else:
    #     return JsonResponse('Invalid request method', status=405, safe=False)
    customer = request.user.customer
    product = Product.objects.get(id =productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created= OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1) 
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1) 
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
        
    return JsonResponse('Item Updated', safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
          
    else:
        customer, order = guestOrder(request, data)   
            
    total = float(data['form']['total'])
    order.transaction_id=transaction_id
        
    if total == order.get_cart_total:
            order.complete=True
    order.save()    
    
    if order.shipping == True:
        Shipping.objects.create(
            customer=customer,
            order = order,
            address = data['shipping']['address'] ,
            city = data['shipping']['city'],
            state= data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
        
    return JsonResponse('Payment done...', safe=False)