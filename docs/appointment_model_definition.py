appointment_template = {
    "uuid": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "customer_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "appointment_type_id": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "start_time": "2025-08-05T14:30:00Z",
    "end_time": "2025-08-05T15:00:00Z",
    "status": "confirmed",
    "created_at": "2025-07-31T18:15:00Z",
    "updated_at": "2025-07-31T18:20:00Z",
    "notes": "Customer requested a calm playlist during the session.",
    "cancellation_reason": "",
}

appointment_mandatory_fields = [
    "customer_id",
    "appointment_type_id",
    "start_time",
    "end_time",
]

enum_fields = [
    "status",
]

status_enum = ["Scheduled", "Confirmed", "Cancelled"]

appointment_type_template = {
    "uuid": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
    "description": "fc8b7f0c-c0b7-43e5-96f1-dcc667a21c4e",
}
