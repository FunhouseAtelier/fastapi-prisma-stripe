# app/schemas/order.py

from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

InvoiceNumberStr = Annotated[
    str,
    Field(
        min_length=15,
        max_length=15,
        pattern=r"^\d{10}-\d{4}$",  # e.g. 2520240624-0001
        description=
        "Format: XXYYYYYYYY-NNNN (client account number and 4-digit iterator)",
    ),
]

OrderStatusStr = Annotated[
    Literal[
        "pending",
        "paid",
        "completed",
        "cancelled",
        "refunded",
        "disputed",
        "failed",
        "expired",
        "on_hold",
    ],
    Field(description="Order status"),
]

TotalDueInt = Annotated[int, Field(description="Total amount due, in cents")]
TransactionFeeInt = Annotated[
    int, Field(description="Payment processor fee, in cents")]
SalesTaxInt = Annotated[int, Field(description="Sales tax portion, in cents")]
RevenueInt = Annotated[
    int,
    Field(description="Total revenue (excluding fees/taxes), in cents")]

SalesCommissionInt = Annotated[
    int, Field(description="Commission owed to sales rep, in cents")]
TechCommissionInt = Annotated[
    int, Field(description="Commission owed to tech worker, in cents")]
CompanyCutInt = Annotated[
    int, Field(description="Remaining company revenue, in cents")]

StripePaymentIntendIdStr = Annotated[
    str,
    Field(
        min_length=10,
        max_length=30,
        pattern=
        r"^pi_[a-zA-Z0-9]{10,}$",  # Stripe PaymentIntent ID, e.g. pi_3NxP...
        description="Stripe PaymentIntent ID",
    ),
]

StripeInvoiceIdStr = Annotated[
    str,
    Field(
        min_length=10,
        max_length=30,
        pattern=r"^in_[a-zA-Z0-9]{10,}$",  # Stripe Invoice ID, e.g. in_3NxQ...
        description="Stripe Invoice ID",
    ),
]

StripeStatusStr = Annotated[
    Literal["draft", "open", "paid", "uncollectible", "void", "deleted"],
    Field(description="Status of the Stripe invoice"),
]

AssociateIdStr = str
ClientIdStr = str

AuditedAtDate = datetime

AuditNotesStr = Annotated[
    str,
    Field(max_length=1000,
          description="Internal notes from audit or review process"),
]
