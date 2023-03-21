from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .premissions import IsAdminOrReadOnly
from .serializers import *
from rest_framework.viewsets import ModelViewSet


@api_view(['GET'])
def show(request):
    return JsonResponse(
        {
            'message': 'В задании не было сказано какая должна быть структура для API ответов, поэтому лучше напишу что  и как',
            'Product': "Используется ModelViewSet, поэтому здесь все стандартно",
            'Cart': [
                {'GET': 'возвращает список товаров в корзине'},
                {'POST': 'Добавляет в корзину товары с переданного ему аргумента product: [<id_product>, <id_product>] он принимает список нужных id продуктов'},
                {'DELETE': 'Для удаления товара из корзины нужно передать аргумент /<int:pk> нужного товара в url'}
            ],
            'Order': [
                {'GET': 'Возвращает список всех заказов от пользователя'},
                {'POST': 'Создает заказ из товаров с корзины. Ничего передавать не надо'}
            ]
         }, status=200
    )


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)


class CartAPI(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Error': 'You are not authenticated'}
                , status=401)

        if not len(Cart.objects.filter(user=request.user)):
            Cart.objects.create(user=request.user)

        products = Cart.objects.get(user=request.user)

        serializer = CartSerializer(products, many=False)

        return JsonResponse(
            {'Products in your carts': serializer.data['products']}
            , status=200)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Error': 'You are not authenticated'}
                , status=401)

        if not len(Cart.objects.filter(user=request.user)):
            Cart.objects.create(user=request.user)

        cart = Cart.objects.get(user=request.user)

        product_ids = request.data.get('products', None)

        if not product_ids:
            return JsonResponse(
                {'error': "you don't give key products. Products must be list and this list have id products"},
                status=404)

        products_obj = Product.objects.filter(id__in=product_ids)

        if not len(products_obj):
            return JsonResponse({'error': 'Not found product'}, status=404)

        for obj in products_obj:
            cart.products.add(obj)
        cart.save()
        serializer = CartSerializer(cart)
        return JsonResponse(
            {'Products in your carts': serializer.data['products']}
            , status=201)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Error': 'You are not authenticated'}
                , status=401)

        if not len(Cart.objects.filter(user=request.user)):
            return JsonResponse({
                'message': 'You cart is empty'
            }, status=404)

        pk = kwargs.get('pk', None)

        if not pk:
            return JsonResponse({'error': 'Method DELETE not allowed'}, status=404)

        try:
            product = Cart.objects.get(user=request.user).products.get(id=pk)
        except:
            return JsonResponse({'error': 'Object does not exit'}, status=400)

        name = product.name

        product.delete()

        return JsonResponse({'order': 'Delete product ' + name}, status=200)


class OrderApi(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Error': 'You are not authenticated'}
                , status=401)

        orders = Order.objects.filter(user=request.user)
        if not len(orders):
            return JsonResponse({
                'Order': []
            }, status=404)

        serializer = OrderSerializer(orders, many=True)
        return JsonResponse({'Orders': serializer.data}, safe=False, status=200)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Error': 'You are not authenticated'}
                , status=401)

        if not len(Cart.objects.filter(user=request.user)):
            return JsonResponse({
                'message': 'You dont have cart'
            }, status=404)

        cart = Cart.objects.get(user=request.user)

        if not cart.products.count():
            return JsonResponse({
                'message': 'You cart is empty'
            }, status=404)

        products = cart.products.all()

        order = Order.objects.create(user=request.user)
        order.products.set(products)
        order.save()

        for obj in cart.products.all():
            cart.products.remove(obj)

        serializer = OrderSerializer(order, many=False)
        return JsonResponse(serializer.data, status=201)
