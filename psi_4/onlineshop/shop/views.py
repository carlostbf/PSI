# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse

from models import Category, Product
from shoppingcart.forms import CartAddProductForm
from shoppingcart.shoppingcart import ShoppingCart

# Create your views here.

def base(request):
	"""
	Vista para el fichero base.html
	Author: Carlos Li
	"""
	return render(request, 'shop/base.html')

def default(request):
	return render(request, 'shop/list.html')

def product_list(request, catSlug=None):	
	"""
	queries that fill category, categories and products
	Author: Carlos Li
	"""
	categories = Category.objects.values().order_by('catName')

	if catSlug == None :
		category = None
		products = Product.objects.values().order_by('prodName')
	else:
		try:
			category=Category.objects.get(catSlug = catSlug)
			products=sorted(Product.objects.filter(category = category))
		except Category.DoesNotExist:
			return redirect('product_list')
	return render(request,'shop/list.html',
		{'category': category,
		'categories': categories,
		'products': products})

def product_detail(request, id, prodSlug):
	"""
	query that returns a product with id=prodId
	Author: Carlos Li
	"""	
	try:
		product=Product.objects.get(id = id, prodSlug = prodSlug)
	except Product.DoesNotExist:
		return redirect('product_list')
	form = CartAddProductForm()
	shoppingcart = ShoppingCart(request)
	having = shoppingcart.unitsOf(product)
	return render(request, 'shop/detail.html', {'product': product, 'form':form, 'having' : having})
