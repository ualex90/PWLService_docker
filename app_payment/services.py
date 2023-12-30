import stripe
import json

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name: str) -> str:
    """
    Create product in stripe service.
    Создание продукта на сервисе Stripe.
    """

    response = stripe.Product.create(name=name)
    product = json.loads(response.last_response.body)
    product_id = product.get('id')

    return product_id


def create_stripe_prise(product) -> str:
    """
    Create a new stripe prise.
    Создание нового платежа на сервисе stripe.
    """

    response = stripe.Price.create(
        unit_amount=product.amount * 100,
        currency=product.currency,
        product=product.stripe_product_id,
    )

    price = json.loads(response.last_response.body)
    price_id = price.get('id')

    return price_id


def create_stripe_session(price, count=1):
    """
    Create a session in stripe .
    Создание сессии для проведения оплаты сервисе stripe.
    """

    response = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price,
                "quantity": count,
            },
        ],
        mode="payment",
    )

    session = json.loads(response.last_response.body)
    session_url = session.get('url')

    return session_url


if __name__ == "__main__":
    pass
    # create_stripe_product("Test product 1")
    # print(create_stripe_session("price_1OJb0OBCFyaMmyJELOCFsTtQ"))

    test_session_url = "https://checkout.stripe.com/c/pay/cs_test_a1lhs1rVT6othyngxMgs4DUJlo5kMD4w1E9nMUEzJythlFHMcFKJpcN8Pk#fidkdWxOYHwnPyd1blpxYHZxWjA0Sk9QS1xHRkN8ZEhofE9ASjVjN0ZcUVBWblZzdnVhUzxqbmwzUlZvZkdjYnw1d0xTX3ZJMD1EcEZAMkRJQ3BVNzRnRDBmSmhPfVZqMmFrZ1VQN1Q2VH1GNTVLMW1ff0BzYCcpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
