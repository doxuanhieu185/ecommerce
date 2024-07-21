from decimal import Decimal
from store.models import Products

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values() if isinstance(item, dict) and 'qty' in item)

    def __iter__(self):
        all_product_ids = [int(key) for key in self.cart.keys() if key.isdigit()]
        products = Products.objects.filter(id__in=all_product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            if 'product' in item:  # Chỉ xử lý các mục có sản phẩm
                item['price'] = Decimal(item['price'])
                item['total'] = item['price'] * item['qty']
                yield item


    def get_total(self):
        total = sum(Decimal(item['price']) * Decimal(item['qty']) for item in self.cart.values() if 'price' in item and 'qty' in item)
        return total
