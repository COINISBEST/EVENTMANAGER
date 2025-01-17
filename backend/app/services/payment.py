from typing import Dict
import razorpay
from fastapi import HTTPException
from app.core.config import settings

class PaymentService:
    def __init__(self):
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    def verify_payment(self, payment_data: Dict) -> bool:
        try:
            # Verify payment signature
            params_dict = {
                'razorpay_payment_id': payment_data.get('razorpay_payment_id'),
                'razorpay_order_id': payment_data.get('razorpay_order_id'),
                'razorpay_signature': payment_data.get('razorpay_signature')
            }

            if not all(params_dict.values()):
                raise HTTPException(
                    status_code=400,
                    detail="Missing required payment verification parameters"
                )

            self.client.utility.verify_payment_signature(params_dict)
            return True

        except razorpay.errors.SignatureVerificationError:
            raise HTTPException(
                status_code=400,
                detail="Invalid payment signature"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Payment verification failed: {str(e)}"
            ) 