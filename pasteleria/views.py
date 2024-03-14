from carton.cart import Cart
from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse

from pasteleria.models import Producto, UserProfile


class NuevaTareaForm(forms.Form):
    producto = forms.CharField(label="Producto")
    precio = forms.IntegerField(label="Precio",
                                min_value=1)
    stock = forms.IntegerField(label="Stock", min_value=0)


# Create your views here.
def post_login_redirect(request):
    if request.user.userprofile.role == 'admin':
        return redirect('admin_lista_productos')
    else:
        return redirect('lista_productos')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='customer')
            login(request, user)
            return redirect('post_login_redirect')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def admin_lista_productos(request):
    productos = Producto.objects.all()  # Recupera todos los productos de la base de datos
    return render(request, "admin_lista_productos.html", {"productos": productos})


def admin_agregar_producto(request):
    if request.method == "POST":
        form = NuevaTareaForm(request.POST)
        if form.is_valid():
            producto_nombre = form.cleaned_data["producto"]
            precio = form.cleaned_data["precio"]
            stock = form.cleaned_data["stock"]
            producto = Producto(nombre=producto_nombre, precio=precio, stock=stock)
            # Guarda el producto en la base de datos
            producto.save()  # Redirigir al usuario a la lista de tareas
            return HttpResponseRedirect(reverse("admin_lista_productos"))
        else:
            # Si el formulario no es válido, vuelva a mostrar la página con la información existente.
            return render(request, "admin_agregar_producto.html", {
                "form": form
            })
    # si el método no es POST
    return render(request, "admin_agregar_producto.html", {
        "form": NuevaTareaForm()
    })


def admin_eliminar_producto(request, producto_id):
    if request.method == 'DELETE':
        try:
            Producto.objects.filter(id=producto_id).delete()
            return JsonResponse({'message': 'Producto eliminado correctamente'}, status=200)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def admin_editar_producto(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=producto_id)
        form = NuevaTareaForm(request.POST)
        if form.is_valid():
            producto.nombre = form.cleaned_data["producto"]
            producto.precio = form.cleaned_data["precio"]
            producto.stock = form.cleaned_data["stock"]
            producto.save()
            return redirect('admin_lista_productos')
        else:
            producto = get_object_or_404(Producto, pk=producto_id)
            return render(request, 'admin_editar_producto.html', {
                "form": form,
                "producto": producto
            })
    else:
        producto = get_object_or_404(Producto, pk=producto_id)
        form = NuevaTareaForm(initial={
            "producto": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock
        })
        return render(request, 'admin_editar_producto.html', {
            "form": form,
            "productoObject": producto
        })


def lista_productos(request):
    productos = Producto.objects.all()  # Recupera todos los productos de la base de datos
    return render(request, 'lista_productos.html', {
        "productos": productos
    })


def agregar_carrito(request, id_producto):
    try:
        cart = Cart(request.session)
        producto = get_object_or_404(Producto, pk=id_producto)
        if producto.stock > 0:
            cart.add(producto, price=producto.precio, quantity=1)
            producto.stock -= 1
            producto.save()
            return JsonResponse({'message': 'Product added to cart', 'new_stock': producto.stock})
        else:
            return JsonResponse({'error': 'Stock not sufficient for product: ' + producto.nombre}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def update_stock(request, product_id):
    product = get_object_or_404(Producto, pk=product_id)
    return JsonResponse({'new_stock': product.stock})


def ver_carrito(request):
    cart = Cart(request.session)
    return render(request, 'ver_carrito.html', {
        "carrito": cart
    })


def procesar_pago(request, total):
    cart = Cart(request.session)
    if total == 0:
        return redirect('ver_carrito')
    else:
        cart.clear()
        return redirect('lista_productos')


def eliminar_producto_carrito(request, product_id):
    product = Producto.objects.get(id=product_id)
    cart = Cart(request.session)
    for item in cart.items:
        prod = item.product
        quantity = item.quantity
        if prod == product:
            cart.set_quantity(product, quantity - 1)
            product.stock += 1
            product.save()
            if quantity == 1:
                cart.remove(product)
            break
    return redirect('ver_carrito')