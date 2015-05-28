from django.http import Http404
from BABIDI import settings
from BABIDI_SERVICE.templates.utils import userUtil
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import get_object_or_404
import base64, json
import time, datetime, os

from BABIDI import models

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'stl'])

class Order(View) :
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(Order, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		if not 'loginSession' in request.session:
			context = (401, {"text" : "Login Please"})
			return HttpResponse(json.dumps(context[1]), status=context[0])

		if not kwargs['userId'] == request.session['loginSession']['userId']:
			context = (401, {"text" : "Permission Denied"})
			return HttpResponse(json.dumps(context[1]), status=context[0])

		user = get_object_or_404(models.UserAccount, id=request.session['loginSession']['userId']))
		if (user.is_active == 0):
			context = (410, {"text" : "user %d is deactivate" % (user.id)})
			return HttpResponse(json.dumps(context[1]), status=context[0])

		if 'orderId' in kwargs :
			context = self.getOrderDetail(user.id, kwargs['orderId'])
		else :
			context = self.getOrderList(user.id)
		return HttpResponse(json.dumps(context[1]), status=context[0])

	def getOrderList(self, userId) :
		entry = []
		shareModel = models.ModelShared.objects.filter(user=userId)
		for p in shareModel :
			orderList = models.OrderPrinting.objects.filter(model=p.id)
			for order in orderList :
				entry.append(order.id)
		context = (200, entry)
		return context

	def getOrderDetail(self, userId, orderId) :
		entries = []
		shareModel = models.ModelShared.objects.filter(user=userId)
		orderList = models.OrderPrinting.objects.filter(id=orderId)
		if shareModel.id != orderList.model :
			context = (401, {"text" : "Permission Denied"})
		else :
			for order in orderList :
				entry = {}
				entry['id'] = order.id
				entry['material'] = order.material_id
				entry['printer'] = order.printer_id
				entry['price'] = order.price
				entry['statusCode'] = order.status_code
				entry['shippingCode'] = order.shipping_code
				entry['address1'] = order.address1
				entry['address2'] = order.address2
				entry['country'] = order.country
				entry['time'] = order.time.strftime("%Y-%m-%d %H:%M:%S")
				if order.due_date :
					entry['dueDate'] = order.due_date.strftime("%Y-%m-%d")
				else :
					entry['dueDate'] = "0000-00-00"
				entries.append(entry)
			context = (200, entry)
		return context

def fileUpload(userId, file, fileType) :
	userDirectory = os.path.join(settings.MEDIA_ROOT, str(userId) + "/")
	stlDirectory = os.path.join(userDirectory, 'stl/')
	imgDirectory = os.path.join(userDirectory, 'img/')
	if not os.path.exists(userDirectory): os.makedirs(userDirectory)
	if not os.path.exists(stlDirectory): os.makedirs(stlDirectory)
	if not os.path.exists(imgDirectory): os.makedirs(imgDirectory)

	if fileType == 'stl' : filePath = os.path.join(stlDirectory + file.name)
	elif fileType == 'img' : filePath = os.path.join(userDirectory + file.name)

	with open(filePath, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
		destination.close()
	return filePat