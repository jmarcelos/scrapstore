from mongoengine import *
from model.home import *

connect(host='mongodb://scrapstore:scrapstore@ds059682.mongolab.com:59682/scrapstore')



extra1 = ExtraProduct(prod_id=1, url='xxx')
extra2 = ExtraProduct(prod_id=1, url='xxxw')
extra3 = ExtraProduct(prod_id=2, url='xxx')
extra4 = ExtraProduct(prod_id=3, url='xxx')
extra5 = ExtraProduct(prod_id=4, url='xxx')

product_list1 = [extra1, extra3, extra4, extra5]
product_list2 = [extra2]
set_product_list1 = set(product_list1)
set_product_list2 = set(product_list2)
print len(product_list1)
print len(set_product_list1)
print len(product_list2)
print len(set_product_list2)
print len(set_product_list1 - set_product_list2)

product_list2 = []

# x=HomePage(url='http://www.global.com')
# x1=HomePage(url='http://www.global.com?dasdsa')
# x2=HomePage(url='hwww.global.com.br')
# x3=HomePage(url='xurupita')
#
# HomePage.objects.insert([x,x1,x2,x3])
#print extra
