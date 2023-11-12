from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, PositiveInt, Field

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: EmailStr  # валидация email
    age: PositiveInt | None = Field(default=None, lt=130)  # целое положительное
    is_subscribed: bool = False


fake_db = []


@app.post('/create_user')
async def create_user(user: UserCreate) -> UserCreate:
    fake_db.append({'name': user.name,
                    'email': user.email,
                    'age': user.age,
                    'is_subscribed': user.is_subscribed})
    return user


@app.get('/users')
async def users():
    return {'users': fake_db}


sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


@app.get('/product/search')
async def search_product(keyword: str, category: str = None, limit: int = 10):
    products = sample_products
    if category:
        products = [product for product in products
                    if product['category'] == category]

    result = [product for product in products
              if keyword in product['name']]
    if result:
        return result[:limit]
    return {'error': 'not found'}


@app.get('/product/{product_id}')
async def search_product_by_id(product_id: int):
    result = {'error': 'not found'}
    for product in sample_products:
        if product['product_id'] == product_id:
            result = product
    return result
