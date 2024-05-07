from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf.urls import handler404
urlpatterns = [
    path('', views.index, name='index'),  # Rota para a página inicial
    path('index.html', views.index, name='indexreturn'),
    path('shop.html', views.shop, name='shop'),  # Rota para /shop.html
    path('shop-detail.html', views.shopdetail, name='shopdetail'),  # Rota para /shop-detail.html
    path('admin', views.admin, name='account-adm'),  # Renomeada para 'account-adm'
    path('cart.html', views.cart, name='cart'),
    path('template/', views.validar_login, name='login1'),  # Rota específica para validar login
    path('CreateItem/', views.create_item, name='item'),  # Rota específica para validar login
    # path('produtos/<str:nome_arquivo>/', views.produto_detail, name='pagina_produto'),
    path('updateTable', views.updatetable, name='updateAdmin'),
    path('produtos/<int:id>/', views.views_produtos, name='viwProdutos'),
    path('account',  views.accountCliente, name='account-cliente'),
    path('createAccount', views.accoutCreate, name='account_create'),
    path('AccountLogin', views.loginAccount, name='account_login'),
    path('validando', views.validateProduct, name ='validateProduct'),
    path('ModalLogin', views.authenticate_user_modal_admin, name='LoginModal'),
    path('deleteAdmin', views.deleteAdmin, name='delAdmin'),
    path('succeedDelete', views.succeedDelete, name='succeeddelete'),
    path('logout', views.loggout, name='loggout1'),
    path('profile.html', views.profile, name='profile'),
    path('chekout', views.checkin, name='checkin'),
    path('extrairpedido/', views.extractPedidos, name='extrairpedido'),
    path('Aproved', views.Aproved, name='aproved')

]


handler404 = views.error_404
