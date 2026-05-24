import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

# PDF generation imports
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# =====================================================
# INITIAL SETUP
# =====================================================

fake = Faker()

# Create folders automatically
os.makedirs("data", exist_ok=True)
os.makedirs("docs", exist_ok=True)

print("Folders created successfully!")

# =====================================================
# PROMPT-ENGINEERED TEMPLATES
# =====================================================

# These prompts simulate prompt engineering concepts
# for enterprise AI workflow projects.

prompts_used = {

    "customer_complaints":
        """
        Generate realistic retail customer complaints
        for delayed delivery, refund issues,
        payment failures, damaged products,
        wrong item delivery, and app crashes.
        """,

    "incident_logs":
        """
        Generate realistic retail operational outage logs
        related to warehouse delays, website downtime,
        inventory mismatch, and payment gateway failures.
        """,

    "rag_documents":
        """
        Generate professional retail SOP documents
        and policy guides for customer support workflows.
        """
}

# =====================================================
# MASTER DATA
# =====================================================

issue_types = [
    "Order Delay",
    "Wrong Item",
    "Damaged Item",
    "Refund Issue",
    "Payment Issue",
    "Cancellation Issue",
    "Stock Issue",
    "App Issue"
]

products = [
    "Shoes",
    "Headphones",
    "Laptop Bag",
    "Smartwatch",
    "Jeans",
    "Mobile Charger",
    "Bluetooth Speaker",
    "Tablet",
    "Wireless Mouse",
    "Backpack"
]

channels = [
    "Email",
    "Chat",
    "Phone",
    "Mobile App"
]

priorities = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

statuses = [
    "Open",
    "In Progress",
    "Resolved",
    "Escalated"
]

locations = [
    "Mumbai Warehouse",
    "Delhi Store",
    "Bengaluru Hub",
    "Chennai Store",
    "Pune Warehouse",
    "Hyderabad Hub"
]

teams = [
    "Logistics Team",
    "Payment Support",
    "Warehouse Operations",
    "Technical Support",
    "Customer Support"
]

sentiments = [
    "Angry",
    "Frustrated",
    "Neutral",
    "Satisfied"
]

# =====================================================
# RETAIL COMPLAINT TEMPLATES
# =====================================================

complaint_templates = {

    "Order Delay": [

        "My order for {} has not been delivered yet.",

        "The delivery for my {} is delayed by several days.",

        "I am still waiting for my {} order.",

        "Shipment tracking for my {} has not updated."
    ],

    "Wrong Item": [

        "I received the wrong {} in my package.",

        "The delivered {} does not match my order.",

        "A different item was delivered instead of {}.",

        "The {} received is incorrect."
    ],

    "Damaged Item": [

        "The {} arrived damaged and unusable.",

        "My {} was delivered in broken condition.",

        "The packaging for {} was damaged.",

        "The delivered {} is defective."
    ],

    "Refund Issue": [

        "Refund for my {} has not been credited.",

        "My refund for {} is still pending.",

        "I returned the {} but refund is not processed.",

        "Refund status for {} has not been updated."
    ],

    "Payment Issue": [

        "Payment was deducted while ordering {} but order failed.",

        "Transaction completed but {} order was not placed.",

        "Amount deducted for {} but no order confirmation received.",

        "Payment issue occurred during checkout for {}."
    ],

    "Cancellation Issue": [

        "I cancelled my {} order but it is still active.",

        "Cancellation request for {} is not processed.",

        "Order cancellation failed for {}.",

        "I want to cancel {} but the order is still open."
    ],

    "Stock Issue": [

        "{} was shown available but later became out of stock.",

        "Inventory issue occurred while purchasing {}.",

        "{} was unavailable after order placement.",

        "Stock mismatch detected for {}."
    ],

    "App Issue": [

        "The app crashes while purchasing {}.",

        "Checkout page freezes for {} order.",

        "Unable to place {} order through app.",

        "Retail website not responding during {} purchase."
    ]
}

# =====================================================
# INCIDENT LOG TEMPLATES
# =====================================================

incident_templates = {

    "Payment Gateway Failure": [

        "Customers unable to complete payments due to gateway timeout.",

        "Multiple transaction failures detected in payment service.",

        "Payment processor latency increased significantly."
    ],

    "Inventory Mismatch": [

        "Inventory mismatch detected between warehouse and database.",

        "Product stock count inconsistency identified.",

        "Warehouse inventory sync issue detected."
    ],

    "Website Downtime": [

        "Retail website unavailable during peak traffic.",

        "Checkout service temporarily down.",

        "Frontend application outage detected."
    ],

    "Warehouse Delay": [

        "Warehouse dispatch delayed due to operational backlog.",

        "Shipment processing queue increased significantly.",

        "Packaging workflow delay reported."
    ],

    "Delivery Partner Delay": [

        "Courier partner experiencing shipment delays.",

        "Last-mile delivery delays reported in multiple cities.",

        "Logistics network disruption detected."
    ]
}

# =====================================================
# GENERATE RETAIL TICKETS
# =====================================================

print("Generating retail tickets...")

ticket_rows = []

for i in range(1, 301):

    issue_type = random.choice(issue_types)

    product = random.choice(products)

    complaint = random.choice(
        complaint_templates[issue_type]
    ).format(product)

    created_time = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23)
    )

    ticket_rows.append({

        "ticket_id":
            f"TKT{i:04}",

        "customer_id":
            f"CUST{random.randint(1000,9999)}",

        "order_id":
            f"ORD{random.randint(10000,99999)}",

        "product":
            product,

        "issue_type":
            issue_type,

        "ticket_text":
            complaint,

        "priority":
            random.choice(priorities),

        "customer_sentiment":
            random.choice(sentiments),

        "channel":
            random.choice(channels),

        "location":
            random.choice(locations),

        "assigned_team":
            random.choice(teams),

        "status":
            random.choice(statuses),

        "requires_escalation":
            random.choice(["Yes", "No"]),

        "sla_breach":
            random.choice(["Yes", "No"]),

        "created_at":
            created_time.strftime("%Y-%m-%d %H:%M:%S")
    })

# Convert to DataFrame
tickets_df = pd.DataFrame(ticket_rows)

# Save CSV
tickets_df.to_csv(
    "data/retail_tickets.csv",
    index=False
)

print("Retail tickets generated successfully!")

# =====================================================
# GENERATE INCIDENT LOGS
# =====================================================

print("Generating incident logs...")

incident_types = [
    "Payment Gateway Failure",
    "Inventory Mismatch",
    "Website Downtime",
    "Warehouse Delay",
    "Delivery Partner Delay"
]

incident_rows = []

for i in range(1, 91):

    incident_type = random.choice(incident_types)

    description = random.choice(
        incident_templates[incident_type]
    )

    incident_rows.append({

        "log_id":
            f"LOG{i:03}",

        "incident_type":
            incident_type,

        "severity":
            random.choice(priorities),

        "location":
            random.choice(locations),

        "affected_team":
            random.choice(teams),

        "system_status":
            random.choice([
                "Operational",
                "Partially Down",
                "Down"
            ]),

        "requires_immediate_action":
            random.choice(["Yes", "No"]),

        "description":
            description,

        "timestamp":
            (
                datetime.now() - timedelta(
                    hours=random.randint(1, 100)
                )
            ).strftime("%Y-%m-%d %H:%M:%S")
    })

# Convert to DataFrame
incident_df = pd.DataFrame(incident_rows)

# Save CSV
incident_df.to_csv(
    "data/retail_incident_logs.csv",
    index=False
)

print("Retail incident logs generated successfully!")

# =====================================================
# RAG DOCUMENT CONTENT
# =====================================================

refund_policy = """
RETAIL REFUND POLICY

1. Refunds should be processed within 5 business days.

2. Refunds delayed beyond 7 days must be escalated
to finance support.

3. Returned products must pass quality verification.

4. Damaged products are eligible for replacement
or refund.

5. All refund requests require valid order ID
and payment reference.
"""

damaged_item_sop = """
DAMAGED ITEM HANDLING SOP

1. Verify customer complaint images.

2. Confirm order details and shipment information.

3. Arrange return pickup within 48 hours.

4. Offer replacement if inventory is available.

5. Escalate repeated complaints to warehouse operations.
"""

payment_failure_guide = """
PAYMENT FAILURE ESCALATION GUIDE

1. Verify transaction ID and payment status.

2. Check payment gateway logs for failures.

3. Escalate unresolved payment failures.

4. Notify finance and customer support teams.

5. Monitor recurring payment outage incidents.
"""

order_delay_sop = """
ORDER DELAY TROUBLESHOOTING GUIDE

1. Verify shipment tracking information.

2. Confirm warehouse dispatch status.

3. Escalate long delivery delays to logistics team.

4. Provide revised ETA to customer.

5. Monitor repeated courier partner delays.
"""

documents = {
    "refund_policy": refund_policy,
    "damaged_item_sop": damaged_item_sop,
    "payment_failure_guide": payment_failure_guide,
    "order_delay_sop": order_delay_sop
}

# =====================================================
# PDF CREATION FUNCTION
# =====================================================

def create_pdf(file_path, title, content):

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    # Title
    title_para = Paragraph(
        f"<b>{title}</b>",
        styles['Title']
    )

    story.append(title_para)

    story.append(Spacer(1, 12))

    # Content
    paragraphs = content.split("\n")

    for para in paragraphs:

        if para.strip():

            p = Paragraph(
                para,
                styles['BodyText']
            )

            story.append(p)

            story.append(Spacer(1, 8))

    doc.build(story)

# =====================================================
# GENERATE TXT + PDF DOCUMENTS
# =====================================================

print("Generating RAG documents...")

for file_name, content in documents.items():

    # Save TXT
    txt_path = f"docs/{file_name}.txt"

    with open(
        txt_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)

    # Save PDF
    pdf_path = f"docs/{file_name}.pdf"

    create_pdf(
        pdf_path,
        file_name.replace("_", " ").title(),
        content
    )

print("TXT and PDF documents generated successfully!")

# =====================================================
# DATA QUALITY CHECKS
# =====================================================

print("\n========== DATA QUALITY CHECK ==========\n")

# Missing values
print("Missing Values:\n")

print(tickets_df.isnull().sum())

# Duplicate ticket IDs
print("\nDuplicate Ticket IDs:")

print(
    tickets_df["ticket_id"].duplicated().sum()
)

# Duplicate incident IDs
print("\nDuplicate Incident Log IDs:")

print(
    incident_df["log_id"].duplicated().sum()
)

print("\nData quality checks completed!")

# =====================================================
# README FILE
# =====================================================

readme_content = """
RETAIL AI PROJECT

PROJECT OVERVIEW
----------------
This project generates synthetic retail support datasets,
incident logs, and RAG knowledge documents for an
AI-powered retail support workflow.

GENERATED FILES
---------------
1. retail_tickets.csv
2. retail_incident_logs.csv
3. PDF SOP Documents

FEATURES
--------
- Synthetic ticket generation
- Operational outage simulation
- PDF document generation
- Prompt-engineered templates
- Data quality checks

USE CASES
---------
- Ticket Classification Agent
- Severity Detection Agent
- RAG Resolution Workflow
- Human Approval Workflow
"""

with open(
    "README.md",
    "w",
    encoding="utf-8"
) as f:

    f.write(readme_content)

print("README.md created successfully!")

# =====================================================
# DISPLAY SAMPLE OUTPUT
# =====================================================

print("\n========== SAMPLE RETAIL TICKETS ==========\n")

print(tickets_df.head())

print("\n========== SAMPLE INCIDENT LOGS ==========\n")

print(incident_df.head())

print("\nAll project files generated successfully!")