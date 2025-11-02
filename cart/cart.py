from django.conf import settings
from products.models import Product
from .models import CartItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user

        if self.user.is_authenticated:
            # 登入用戶：從 DB 讀取
            self.cart = {}
            from .models import CartItem
            for item in CartItem.objects.filter(user=self.user):
                self.cart[str(item.product.id)] = {
                    'quantity': item.quantity,
                    'id': str(item.product.id)
                }
        else:
            # 匿名用戶：從 session 讀取
            cart = self.session.get(settings.CART_SESSION_ID)
            if cart is None:
                # 確保 session 已建立並保存
                if not self.session.session_key:
                    self.session.save()  # 👈 關鍵：確保 session 存在
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}
        for item in self.cart.values():
            pid = item.get('id')
            if pid in product_map:
                product = product_map[pid]
                yield {
                    'product': product,
                    'quantity': item['quantity'],
                    'total_price': product.price * item['quantity'],
                    'id': pid
                }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)
        product = Product.objects.get(id=product_id)

        if self.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={'quantity': 0}
            )
            if update_quantity:
                cart_item.quantity += int(quantity)
            else:
                cart_item.quantity = int(quantity)

            if cart_item.quantity <= 0:
                cart_item.delete()
                # 同步移除 self.cart
                if product_id in self.cart:
                    del self.cart[product_id]
            else:
                cart_item.save()
                self.cart[product_id] = {'quantity': cart_item.quantity, 'id': product_id}
        else:
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'id': product_id}
            if update_quantity:
                self.cart[product_id]['quantity'] += int(quantity)
            else:
                self.cart[product_id]['quantity'] = int(quantity)
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
            self.session.modified = True
            self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user, product_id=product_id).delete()
        if product_id in self.cart:
            del self.cart[product_id]
        if not self.user.is_authenticated:
            self.save()

    def clear(self):
        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user).delete()
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for item in self.cart.values():
            pid = item['id']
            product = next((p for p in products if str(p.id) == pid), None)
            if product:
                total += product.price * item['quantity']
        return total

    def get_item(self, product_id):
        return self.cart.get(str(product_id))