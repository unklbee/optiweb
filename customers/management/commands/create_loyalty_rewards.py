# customers/management/commands/create_loyalty_rewards.py
from django.core.management.base import BaseCommand
from customers.models import LoyaltyReward


class Command(BaseCommand):
    def handle(self, *args, **options):
        rewards = [
            {
                'name': 'Diskon 10% Service',
                'description': 'Dapatkan diskon 10% untuk service apapun',
                'reward_type': 'DISCOUNT',
                'points_required': 500,
                'discount_percentage': 10,
                'minimum_order_value': 100000
            },
            {
                'name': 'Diskon 50rb',
                'description': 'Potongan harga Rp 50.000 untuk service',
                'reward_type': 'FIXED_AMOUNT',
                'points_required': 800,
                'discount_amount': 50000,
                'minimum_order_value': 200000
            },
            {
                'name': 'Free Cleaning Laptop',
                'description': 'Cleaning laptop gratis senilai Rp 75.000',
                'reward_type': 'FREE_SERVICE',
                'points_required': 1000,
                'minimum_order_value': 0
            }
        ]

        for reward_data in rewards:
            LoyaltyReward.objects.get_or_create(
                name=reward_data['name'],
                defaults=reward_data
            )