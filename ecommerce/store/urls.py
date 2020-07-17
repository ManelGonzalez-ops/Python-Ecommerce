from django.urls import path, include
from . import views

from .views import toMain, toStore, toCart, toCheckout, addToCart, updateCart, processOrder, pagar, cartAjax, signUp, login, logout_view

urlpatterns = [
    path("", toStore, name="main"),
    path("store/", toStore, name="store"),
    path("cart/", toCart, name="cart"),
    path("checkout/", toCheckout, name="checkout"),
    path("addToCart/", addToCart),
    path("updateCart/", updateCart),
    path("processOrder/", processOrder, name="payment"),
    path("pagar/", pagar),
    path("cartAjax/", cartAjax),
    path("signup/", signUp, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout_view)
    # path("accounts/", include("django.contrib.auth.urls"))
]

#path: accounts/ looks for /login path, and render a template in templates/register