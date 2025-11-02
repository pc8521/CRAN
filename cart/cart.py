from django.conf import settings
from products.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        # 僅用於迭代時查詢 Product，不修改 self.cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}
        
        for item in self.cart.values():
            product_id = item.get('id')
            if product_id in product_map:
                product = product_map[product_id]
                # 動態附加 product（不存入 session）
                total_price = product.price * item['quantity']
                yield {
                    'product': product,
                    'quantity': item['quantity'],
                    'total_price': total_price,
                    'id': product_id
                }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True  # 不需要重新賦值

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'id': product_id}
        
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
        else:
            self.cart[product_id]['quantity'] = int(quantity)
        
        # 移除數量為 0 的項目
        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product_id)
        else:
            self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]   
        self.session.modified = True

    def get_total_cost(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}
        
        total = 0
        for item in self.cart.values():
            product_id = item['id']
            if product_id in product_map:
                total += product_map[product_id].price * item['quantity']
        return total

    def get_item(self, product_id):
        return self.cart.get(str(product_id))