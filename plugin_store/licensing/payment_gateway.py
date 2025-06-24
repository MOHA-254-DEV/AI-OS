import uuid

class PaymentGateway:
    def __init__(self):
        self.supported_methods = ['stripe', 'paypal']
        self.orders = {}

    def initiate_payment(self, method, amount, user_email, plugin_id):
        if method not in self.supported_methods:
            return False, "Unsupported payment method"
        
        order_id = str(uuid.uuid4())
        self.orders[order_id] = {
            "status": "pending",
            "plugin_id": plugin_id,
            "email": user_email,
            "amount": amount,
            "method": method
        }
        print(f"🧾 Payment initiated: {method.upper()} for ${amount} (Order ID: {order_id})")
        return True, order_id

    def confirm_payment(self, order_id):
        if order_id in self.orders:
            self.orders[order_id]["status"] = "paid"
            print(f"✅ Payment confirmed for order: {order_id}")
            return True
        return False

    def get_order_status(self, order_id):
        return self.orders.get(order_id, {}).get("status", "unknown")
