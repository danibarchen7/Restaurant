# # api/serializers.py
# from rest_framework import serializers

# class OrderSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     email = serializers.EmailField()  # Validate email format
#     meal = serializers.CharField()
#     drink = serializers.CharField()
#     time = serializers.CharField()
#     payOnline = serializers.BooleanField()
# from rest_framework import serializers
# from django.core.validators import MinValueValidator

# class OrderSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     email = serializers.EmailField()
#     meal = serializers.ChoiceField(
#         choices=[('Pizza', 'Pizza'), ('Burger', 'Burger'), ('Salad', 'Salad')]
#     )
#     drink = serializers.ChoiceField(
#         choices=[('Water', 'Water'), ('Coke', 'Coke'), ('Juice', 'Juice')],
#         required=False,
#         allow_blank=True
#     )
#     count = serializers.IntegerField(
#         validators=[MinValueValidator(1)],
#         default=1
#     )
#     time = serializers.TimeField(format="%H:%M")
#     payOnline = serializers.BooleanField(default=False)
#     notes = serializers.CharField(required=False, allow_blank=True)
#     receipt = serializers.FileField(required=False)
from rest_framework import serializers
from dishes.models import MenuItem
class MealItemSerializer(serializers.Serializer):
    meal = serializers.SlugRelatedField(
        slug_field="name",
        queryset=MenuItem.objects.all(),
        help_text="Select from available meals"
    )
    count = serializers.IntegerField(
        min_value=1,
        max_value=10,
        help_text="Quantity (1-10)"
    )

class OrderSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    items = MealItemSerializer(many=True)
    time = serializers.TimeField(format="%H:%M")

    def validate_items(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one meal required")
        if len(value) > 10:
            raise serializers.ValidationError("Maximum 10 items per order")
        return value