order_model_definition = {
    "uuid": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "customer_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "order_type_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "payment_type_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "appointment_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e", *** OPTIONAL
    "order_items": [
        {
            "order_item_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
            "item_name": "Titanium Nose Ring",
            "quantity": 1,
            "unit_price": 29.99,
            "total_price": 29.99,
        },
        {
           "order_item_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
            "item_name": "Piercing Aftercare Spray",
            "quantity": 2,
            "unit_price": 9.50,
            "total_price": 19.00,
        },
        {
           "order_item_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
            "item_name": "Antiseptic Kit",
            "quantity": 1,
            "unit_price": 19.50,
            "total_price": 19.50,
        },
    ],
    "total": 68.49,
    "created_at": "2025-07-31T18:45:00Z",
    "updated_at": "2025-07-31T19:00:00Z",
}

order_mandatory_fields = [
    "customer_id",
    "order_type_id",
    "payment_type_id",
    "order_items", ***AT LEAST 1
    "total" *** This one is calculated by the backend
]

order_item_model_definition = {
    "uuid": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "description": "Antiseptic Kit",
    "inventory_quantity": 10,
    "unit_price": 19.50,
    "created_at": "2025-07-31T18:45:00Z",
    "updated_at": "2025-07-31T19:00:00Z",
}

order_type_model_definition = {
    "uuid": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "type": "Income",
    "created_at": "2025-07-31T18:45:00Z",
    "updated_at": "2025-07-31T19:00:00Z",
}

order_type_enum_fields = [
    "type",
]

order_type_enum= [
    "Income",
    "Expense",
]


payment_type_model_definition = {
    "uuid": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "type": "Credit Card",
    "created_at": "2025-07-31T18:45:00Z",
    "updated_at": "2025-07-31T19:00:00Z",
}

payment_type_enum_fields = [
    "type",
]

payment_type_enum= [
    "Cash",
    "Credit Card",
    "Debit Card",
    "Exchange",
    "Bank Slip",
    "Pix",
]


