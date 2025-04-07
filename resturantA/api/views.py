# from django.shortcuts import render

# # Create your views here.
# # api/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.mail import EmailMessage
# from django.conf import settings
# from .serializers import OrderSerializer

# class SendEmailAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = OrderSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         data = serializer.validated_data
        
#         try:
#             email = EmailMessage(
#                 subject=f"New Order from {data['name']}",
#                 body=f"""
#                     Order Details:
#                     Name: {data['name']}
#                     Email: {data['email']}
#                     Meal: {data['meal']}
#                     Drink: {data['drink']}
#                     Time: {data['time']}
#                     Payment Method: {'Online' if data['payOnline'] else 'Pickup'}
#                 """,
#                 from_email=settings.EMAIL_HOST_USER,  # Restaurant's email
#                 to=[settings.RECEIVER_EMAIL],           # Restaurant's inbox
#                 reply_to=[data['email']],              # User's email for replies
#             )
#             email.send(fail_silently=False)
            
#             return Response({"success": "Email sent"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
# #             )
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.mail import EmailMessage
# from django.conf import settings
# from .serializers import OrderSerializer
# import logging

# logger = logging.getLogger(__name__)

# class SendEmailAPIView(APIView):
#     """Handle order submissions and email notifications"""
    
#     def post(self, request, *args, **kwargs):
#         # Validate payload
#         serializer = OrderSerializer(data=request.data)
#         if not serializer.is_valid():
#             logger.warning(f"Invalid order data: {serializer.errors}")
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         data = serializer.validated_data
        
#         try:
#             # Build email message
#             email_body = f"""
#             NEW ORDER RECEIVED
#             ------------------
#             Customer Details:
#             Name: {data['name']}
#             Email: {data['email']}
            
#             Order Details:
#             Meal: {data['meal']}
#             Quantity: {data['count']}
#             Drink: {data.get('drink', 'No drink selected')}
#             Preferred Time: {data['time']}
#             Payment Method: {'Online' if data['payOnline'] else 'On Pickup'}
            
#             Additional Notes:
#             {data.get('notes', 'No additional notes')}
#             """.strip()

#             email = EmailMessage(
#                 subject=f"New Order: {data['meal']} x{data['count']}",
#                 body=email_body,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[settings.ORDERS_EMAIL],
#                 reply_to=[data['email']],
#                 headers={'X-Restaurant-Order': '1.0'},
#             )
            
#             # Add optional attachment
#             if receipt := data.get('receipt'):
#                 email.attach(receipt.name, receipt.read(), receipt.content_type)
            
#             email.send(fail_silently=False)
#             logger.info(f"Order email sent for {data['email']}")
            
#             return Response(
#                 {"message": "Order received successfully!"},
#                 status=status.HTTP_201_CREATED
#             )
            
#         except Exception as e:
#             logger.error(f"Order failed: {str(e)}", exc_info=True)
#             return Response(
#                 {"error": "Failed to process order. Please try again."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.core.mail import EmailMessage
from django.conf import settings
from .serializers import OrderSerializer
import logging
import json

logger = logging.getLogger(__name__)

class SendOrderEmailAPIView(APIView):
    """
    Handle order submissions with multiple meal items
    """
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        # Validate request data
        serializer = OrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(
                {
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        
        try:
            # Build email content
            email_body = [
                "📦 New Order Received",
                "=====================",
                f"👤 Customer: {data['name']} <{data['email']}>",
                f"⏰ Preferred Time: {data['time'].strftime('%H:%M')}",
                "\n🍽️ Order Items:"
            ]

            total_items = 0
            for idx, item in enumerate(data['items'], 1):
                email_body.append(f"{idx}. {item['meal']} x {item['count']}")
                total_items += item['count']

            email_body.extend([
                "\n----------",
                f"Total Items: {total_items}",
                f"Order ID: {request.data.get('client_reference', 'N/A')}"
            ])

            # Send email
            email = EmailMessage(
                subject=f"New Order: {total_items} Items ({data['name']})",
                body="\n".join(email_body),
                from_email=settings.RECEIVER_EMAIL,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[data['email']]
            )
            email.send(fail_silently=False)
            
            logger.info(f"Order processed successfully for {data['email']}")
            return Response(
                {
                    "status": "success",
                    "message": "Order received successfully!",
                    "order_id": request.data.get('client_reference')
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error(f"Order processing failed: {str(e)}", exc_info=True)
            return Response(
                {
                    "status": "error",
                    "message": "Failed to process order. Please try again.",
                    "system_error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )