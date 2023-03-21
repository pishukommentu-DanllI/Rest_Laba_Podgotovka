from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('products',)
        model = Cart

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Cart.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super(CartSerializer, self).to_representation(instance)
        representation['products'] = ProductSerializer(instance.products, many=True).data
        return representation


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('price', 'products', 'id')
        model = Order

    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)
        representation['products'] = ProductSerializer(instance.products, many=True).data
        return representation
