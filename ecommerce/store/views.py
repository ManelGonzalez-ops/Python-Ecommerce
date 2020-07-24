from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import *
import json
from django.contrib.auth import logout
from django.contrib.auth.models import auth



def login(request):
    if request.method == "POST":
        email = request.POST["username"]
        password = request.POST["password"]
        try:
            userr = User.objects.get(email=email)
            if userr:
          
                theUser = User.objects.get(username=userr)
                user = auth.authenticate(username=theUser, password=password)
                if user:
                    auth.login(request, user)
                    return redirect("store")
                else:
                    print("kaka")
                    return render(request, "registration/login.html", {"error": "Validation error, incorrect password"})
                
        except User.DoesNotExist:
            return render(request, "registration/login.html", {"error": "user not found"})
  
        
        
    else:
        print("kako")
        return render(request, "registration/login.html")

        

def logout_view(request):
    logout(request)
    # we can combine multiple view functions as a middleare, but we have to return it.
    return toStore(request)


def signUp(request):
    print("hooola")
    if request.method == "POST":
        email = request.POST["email"]
        try:
            userr = User.objects.get(email=email)
            
            print("user with that email already exists")
            return redirect("login")

        except User.DoesNotExist:
            # so we can create a new one because there isnt any user with that mail.    
            form = RegisterForm(request.POST)
            
            if form.is_valid():
                form.save()
                newUser = User.objects.get(email=email)
                auth.login(request, newUser)
                print("exito")
                return redirect("main")
            else:
            
                print("user with that email already exists,")
                return render(request, "registration/signup.html",{"form": form,"error": "password not valid"})
    else:
        form = RegisterForm()
        return render(request, "registration/signup.html", {"form": form})

def toMain(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "store/main.html", {"user": user})
    else:
        return render(request, "store/main.html", {"notAuth": True})


def toStore(request):
    context = Product.objects.all()
    user = request.user
    if request.user.is_authenticated:
        noAuth = False
        (costumer, created) = Costumer.objects.get_or_create(user=user, email = user.email)
        usuario = request.user.costumer
        (orden, created) = Order.objects.get_or_create(costumer=usuario, complete=False)
        carrito = orden.orderitem_set.all()
    else:
        response = HttpResponse("create cookie")
        response.set_cookie("cart", {})
        noAuth = True
        carrito = []

    return render(request, "store/store.html", {"data": context, "carrito": len(carrito), "notAuth": noAuth})


def toCart(request):
    if request.user.is_authenticated:
        context = request.user.costumer
        (order, created) = Order.objects.get_or_create(costumer=context, complete=False)
        items = order.orderitem_set.all()
        total_price = 0
        for item in items:
            total_price += item.quantity * item.product.price
    else:
    
        
        order = {}
        print("user not authenticated")

        cookies = json.loads(request.COOKIES["cart"])
        print(cookies)
        items = []
        totalP = 0
        totalQ = 0
        cookieKeys = list(cookies.keys())
        for keyOrderI in cookieKeys:
            orderItem = cookies[keyOrderI]
            producto = Product.objects.get(id=orderItem["id"])
            nuevoRegistro = OrderItem(product=producto, quantity=int(orderItem["quantity"]))
            totalP += int(orderItem["quantity"]) * int(producto.price)
            totalQ += int(orderItem["quantity"])
            nuevoRegistro.id = orderItem["order"]
            items.append(nuevoRegistro)
            order = {"get_total_cartQ": totalQ, "get_total_cartP": totalP}
            
            # registro = {"ordenItemId":}
    return render(request, "store/cart.html", {"data": items, "data2": order, "carrito": len(items)})

def cartAjax(request):
    cookies = json.loads(request.COOKIES["cart"])
    body = json.loads(request.body)
    orderItemBuscado = body["orderUpdated"]
    totalP = 0
    totalQ = 0
    cookieKeys = list(cookies.keys())
    precioOrden = 0
    for keyOrderI in cookieKeys:
        orderItem = cookies[keyOrderI]
        producto = Product.objects.get(id=orderItem["id"])
        if keyOrderI == orderItemBuscado:
            precioOrden = int(orderItem["quantity"]) * producto.price
        
            totalP += int(orderItem["quantity"]) * int(producto.price)
            totalQ += int(orderItem["quantity"])
    
    order = {"get_total_cartQ": totalQ, "get_total_cartP": totalP, "precioOrden": precioOrden, "iden": orderItemBuscado}
    return JsonResponse(order, safe=False)


def toCheckout(request):
    autenticado = False
    if request.user.is_authenticated:
        items = []
        koko = request.user.costumer
        order = Order.objects.get(costumer=koko, complete=False)
        allItems = order.orderitem_set.all()
        for item in allItems:
            producto = Product.objects.get(id=item.product.id)
            items.append({"name": producto.name, "total": item.get_total})
        
        
        try:
            shipping_records = ShippingAddress.objects.filter(costumer=koko)
            shipping_info = shipping_records.latest("date_added")

        except ShippingAddress.DoesNotExist:
            shipping_info = None

        autenticado = True
    else:
        items = []
        autenticado = False
        cookie = json.loads(request.COOKIES["cart"])
        keys = list(cookie.keys())
        needsShipping = False
        for key in keys:
            producto = Product.objects.get(id=cookie[key]["id"])
            orderItem = OrderItem(product=producto, quantity=int(cookie[key]["quantity"]))
            orderItem.id = key
            items.append({"name": producto.name, "total": orderItem.get_total})
            if not producto.digital:
                needsShipping = True
        sumatorioOrders = sum([itemL["total"] for itemL in items])
        order = {"needsShipping": needsShipping , "get_total_cartP": sumatorioOrders}
        shipping_info = {}
    return render(request, "store/checkout.html", {"data1": items, "data2": order, "autenticado": autenticado, "shipping_info": shipping_info})

def addToCart(request):
    kaka = json.loads(request.body)
    if kaka["action"] == "add":
        usuario = request.user.costumer
       
        producto = Product.objects.get(id=kaka["product"])
        check = Order.objects.get(costumer=usuario, complete=False)
        total = check.orderitem_set.all()
        kuku = check.get_total_cartQ
        newOrder = OrderItem(product=producto, order=check, quantity=kaka["quantity"])
        newOrder.save()
   
    return JsonResponse(kuku, safe=False)

def updateCart(request):
    data = json.loads(request.body)
    costumer = request.user.costumer
    orden = Order.objects.get(costumer=costumer, complete=False)
    theOrden = orden.orderitem_set.get(id=data["orderItemId"])
    producto = Product.objects.get(id=theOrden.product.id)
    cantity = ""
    if data["quantity"] == 0:
        theOrden.delete()
        cantity = 0
    else:
        theOrden.quantity = int(data["quantity"])
        # priceOrderItem = data["quantity"] * producto.price
        theOrden.save()
        cantity = theOrden.quantity
    
    
    return JsonResponse({"cantity": orden.get_total_cartQ, "coste": orden.get_total_cartP, "costeOrden": theOrden.get_total, "cantidadOrden": cantity}, safe=False)


def processOrder(request):
    body = json.loads(request.body)
    total_cost = 0
    if request.user.is_authenticated:
        costumer = request.user.costumer
        order = Order.objects.get(costumer=costumer, complete=False)
        total_cost = order.get_total_cartP
        if body["needsShipping"]:
            try:
                shippingInfo = ShippingAddress.objects.get(costumer=costumer, order=order)

                shippingInfo.address = body["datosShipping"]["address"] 
                shippingInfo.city = body["datosShipping"]["city"]
                shippingInfo.state = body["datosShipping"]["state"]
                shippingInfo.zipcode = body["datosShipping"]["zip"]
                shippingInfo.save()

            except ShippingAddress.DoesNotExist:
                shippingInfo = ShippingAddress(costumer=costumer, order=order, address=body["datosShipping"]["address"], city=body["datosShipping"]["city"], state=body["datosShipping"]["state"], zipcode=body["datosShipping"]["zip"])
                shippingInfo.save()
            
            return JsonResponse(total_cost, safe=False)
    else:
        newCostumer, created = Costumer.objects.get_or_create(name=body["datosShipping"]["nombre"],email=body["datosShipping"]["email"], isguest=True)    
        newCostumer.save()    
        newOrder = Order(costumer=newCostumer,
        complete=False)
        newOrder.save()
        cooka = json.loads(request.COOKIES["shipping"])
        cookie = json.loads(request.COOKIES["cart"])
        keys = list(cookie.keys())
        for key in keys:
            producto = Product.objects.get(id=cookie[key]["id"])
            newOrderItem = OrderItem(product=producto, order=newOrder, quantity=int(cookie[key]["quantity"]))
            newOrderItem.save()

        total_cost = newOrder.get_total_cartP
    return JsonResponse(total_cost, safe=False)


def pagar(request):
    if request.user.is_authenticated:
        costumer = request.user.costumer
        orden = Order.objects.get(costumer=costumer, complete=False)
        orden.complete = True
        orden.save()
    else:
        cookie = json.loads(request.COOKIES["shipping"])
        costumer = Costumer.objects.get(email=cookie["email"], isguest=True)
        orden = Order.objects.get(costumer=costumer, complete=False)
        orden.complete = True
        orden.save()
    return JsonResponse("kaka", safe=False)