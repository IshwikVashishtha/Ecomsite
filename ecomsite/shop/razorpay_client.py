import razorpay
from django.conf import settings

# This client is used to create orders and verify payments
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)