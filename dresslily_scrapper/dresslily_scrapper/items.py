import scrapy
from dataclasses import dataclass


@dataclass
class ProductItem:
    product_id: int
    product_url: str
    name: str
    discount: int
    discounted_price: str
    original_price: str
    total_reviews: int
    product_info: str


@dataclass
class ReviewItem:
    product_id: int
    rating: int
    timestamp: float
    text: str
    size: str
    color: str
