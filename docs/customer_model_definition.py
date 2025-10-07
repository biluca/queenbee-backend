customer_template = {
    "uuid": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "first_name": "John",
    "last_name": "Doe",
    "nickname": "Big J",
    "email": "john.doe@example.com",
    "phone": "(55) 999 999 999",
    "date_of_birth": "dd/mm/yyyy",
    "gender": "male",
    "created_at": "2025-07-31T18:00:00Z",
    "updated_at": "2025-07-31T18:00:00Z",
    "is_active": True,
    "address_street": "123 Main Street",
    "address_number": "Apt 4B",
    "address_neighborhood": "neighborhood",
    "address_city": "New York",
    "address_state": "NY",
    "address_zip_code": "10001",
    "address_country": "USA",
    "preferences": ["newsletter", "preferred_language", "sms_notifications"],
    "tags": ["vip", "newsletter_subscriber"],
}

mandatory_fields = [
    "uuid",
    "first_name",
    "last_name",
    "email",
    "phone",
    "date_of_birth",
    "gender",
    "created_at",
    "updated_at",
    "is_active",
    "address_street",
    "address_number",
    "address_neighborhood",
    "address_city",
    "address_state",
    "address_zip_code",
    "address_country",
]

enum_fields = [
    "preferences",
    "tags",
]

preferences_enum = ["whatsapp_news", "email_news"]
tags_enum = ["VIP", "Diabetic"]
