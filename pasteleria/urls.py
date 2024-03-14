from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from pasteleria import views


class CustomLoginView(LoginView):
    success_url = reverse_lazy('tienda')


urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('post_login_redirect/', views.post_login_redirect, name='post_login_redirect'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('administrador/productos/', views.admin_lista_productos, name='admin_lista_productos'),
    path('administrador/productos/agregar/', views.admin_agregar_producto, name='admin_agregar_producto'),
    path('administrador/productos/eliminar/<int:producto_id>/', views.admin_eliminar_producto, name='admin_eliminar_producto'),
    path('administrador/productos/editar/<int:producto_id>/', views.admin_editar_producto, name='admin_editar_producto'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/agregar-carrito/<int:id_producto>/', views.agregar_carrito, name='agregar_carrito'),
    path('productos/ver-carrito', views.ver_carrito, name='ver_carrito'),
    path('productos/procesar-pago/<int:total>/', views.procesar_pago, name='procesar_pago'),
    path('productos/eliminar-producto-carrito/<int:product_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('productos/update_stock/<int:product_id>/', views.update_stock, name='update_stock'),

]
