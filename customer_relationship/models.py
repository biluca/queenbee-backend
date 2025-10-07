import uuid
from django.db import models
from django.core.validators import RegexValidator


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    PREFERENCES_CHOICES = [
        ("whatsapp_news", "WhatsApp News"),
        ("email_news", "Email News"),
    ]

    TAGS_CHOICES = [
        ("VIP", "VIP"),
        ("Diabetic", "Diabetic"),
    ]

    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    is_active = models.BooleanField(default=True)

    # Address Information
    address_street = models.CharField(max_length=255)
    address_number = models.CharField(max_length=50)
    address_neighborhood = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100)
    address_state = models.CharField(max_length=100)
    address_zip_code = models.CharField(max_length=20)
    address_country = models.CharField(max_length=100)

    # JSON fields for preferences and tags (arrays)
    preferences = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_address(self):
        return f"{self.address_street} {self.address_number}, {self.address_neighborhood}, {self.address_city}, {self.address_state} {self.address_zip_code}, {self.address_country}"


class AppointmentType(BaseModel):
    """Model for appointment types (e.g., Haircut, Manicure, etc.)"""

    description = models.CharField(max_length=255)

    class Meta:
        db_table = "appointment_types"
        ordering = ["description"]
        verbose_name = "Appointment Type"
        verbose_name_plural = "Appointment Types"

    def __str__(self):
        return self.description


class Appointment(BaseModel):
    """Model for appointments"""

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    # Basic Information
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="appointments"
    )
    appointment_type = models.ForeignKey(
        AppointmentType, on_delete=models.CASCADE, related_name="appointments"
    )

    # Schedule Information
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )

    # Additional Information
    notes = models.TextField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "appointments"
        ordering = ["-created_at"]
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"{self.customer.full_name} - {self.appointment_type.description} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def duration_minutes(self):
        """Calculate appointment duration in minutes"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return 0
