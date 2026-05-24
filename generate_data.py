# =====================================================
# RETAIL AI PROJECT
# HYBRID AI + TEMPLATE ARCHITECTURE
# =====================================================

# =====================================================
# IMPORTS
# =====================================================

import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

# PDF Generation
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# Gemini AI
import google.generativeai as genai

# =====================================================
# INITIAL SETUP
# =====================================================

fake = Faker()

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("docs", exist_ok=True)

print("Project folders created successfully!")

# =====================================================
# GEMINI CONFIGURATION
# =====================================================

# Replace with your Gemini API Key

API_KEY = "AIzaSyCQcltWTK4EtvlnUpqnduBcos_X8jzzhko"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

print("Gemini configured successfully!")

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
    "Tablet"
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
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Chennai",
    "Pune"
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

customer_tiers = [
    "Silver",
    "Gold",
    "Platinum"
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Wallet"
]

delivery_partners = [
    "Delhivery",
    "BlueDart",
    "Ekart",
    "XpressBees"
]

# =====================================================
# TEMPLATE-BASED COMPLAINTS
# =====================================================

complaint_templates = {

    "Order Delay": [
        "My order for {} has not been delivered yet.",
        "Shipment tracking for my {} has not updated.",
        "Delivery for my {} is delayed."
    ],

    "Wrong Item": [
        "I received the wrong {} in my package.",
        "Incorrect {} was delivered.",
        "Delivered item does not match my order."
    ],

    "Damaged Item": [
        "The {} arrived damaged and unusable.",
        "Packaging for {} was broken.",
        "The delivered {} is defective."
    ],

    "Refund Issue": [
        "Refund for my {} is still pending.",
        "Refund not received for returned {}.",
        "Refund process for {} is delayed."
    ],

    "Payment Issue": [
        "Payment deducted for {} but order failed.",
        "Transaction failed during {} purchase.",
        "Amount deducted but no order confirmation received."
    ],

    "Cancellation Issue": [
        "Unable to cancel my {} order.",
        "Cancellation request failed for {}.",
        "Cancelled order is still active."
    ],

    "Stock Issue": [
        "{} became out of stock after ordering.",
        "Inventory issue detected for {}.",
        "{} unavailable after payment."
    ],

    "App Issue": [
        "Retail app crashes during {} purchase.",
        "Checkout page freezes while ordering {}.",
        "Unable to place {} order through app."
    ]
}

# =====================================================
# RESOLUTION SUGGESTIONS
# =====================================================

resolution_suggestions = {

    "Order Delay":
        "Escalate to logistics support and provide updated ETA.",

    "Wrong Item":
        "Arrange replacement pickup and warehouse verification.",

    "Damaged Item":
        "Initiate return pickup and offer replacement/refund.",

    "Refund Issue":
        "Escalate to finance support and verify refund status.",

    "Payment Issue":
        "Check payment gateway logs and transaction ID.",

    "Cancellation Issue":
        "Verify cancellation eligibility and process request.",

    "Stock Issue":
        "Validate inventory sync and suggest alternatives.",

    "App Issue":
        "Escalate to technical support for debugging."
}

# =====================================================
# GENERATE RETAIL TICKETS
# TEMPLATE-BASED (SAVES API QUOTA)
# =====================================================

print("Generating retail ticket dataset...")

ticket_rows = []

for i in range(1, 151):

    issue_type = random.choice(issue_types)

    product = random.choice(products)

    complaint = random.choice(
        complaint_templates[issue_type]
    ).format(product)

    city = random.choice(locations)

    created_time = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23)
    )

    ticket_rows.append({

        "ticket_id":
            f"{city[:3].upper()}-TKT{i:04}",

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

        "customer_tier":
            random.choice(customer_tiers),

        "payment_method":
            random.choice(payment_methods),

        "delivery_partner":
            random.choice(delivery_partners),

        "channel":
            random.choice(channels),

        "location":
            city,

        "assigned_team":
            random.choice(teams),

        "status":
            random.choice(statuses),

        "requires_escalation":
            random.choice(["Yes", "No"]),

        "sla_breach":
            random.choice(["Yes", "No"]),

        "resolution_time_hours":
            random.randint(1, 72),

        "resolution_suggestion":
            resolution_suggestions[issue_type],

        "created_at":
            created_time.strftime("%Y-%m-%d %H:%M:%S")
    })

tickets_df = pd.DataFrame(ticket_rows)

tickets_df.to_csv(
    "data/retail_tickets.csv",
    index=False
)

print("Retail ticket dataset generated!")

# =====================================================
# TEMPLATE-BASED INCIDENT LOGS
# =====================================================

incident_templates = {

    "Payment Gateway Failure": [
        "Payment gateway latency increased during peak traffic.",
        "High transaction failure rate detected.",
        "Customers unable to complete payments."
    ],

    "Inventory Mismatch": [
        "Warehouse inventory sync issue detected.",
        "Stock inconsistency identified.",
        "Inventory mismatch between systems."
    ],

    "Website Downtime": [
        "Retail website unavailable during peak hours.",
        "Checkout service outage detected.",
        "Frontend application temporarily down."
    ],

    "Warehouse Delay": [
        "Shipment processing backlog detected.",
        "Warehouse operational delays increased.",
        "Dispatch workflow delayed."
    ],

    "Delivery Partner Delay": [
        "Courier network disruption identified.",
        "Shipment ETA increased.",
        "Logistics delays reported."
    ]
}

print("Generating incident logs...")

incident_rows = []

incident_types = list(
    incident_templates.keys()
)

for i in range(1, 31):

    incident_type = random.choice(
        incident_types
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
            random.choice(
                incident_templates[incident_type]
            ),

        "timestamp":
            (
                datetime.now() - timedelta(
                    hours=random.randint(1, 100)
                )
            ).strftime("%Y-%m-%d %H:%M:%S")
    })

incident_df = pd.DataFrame(
    incident_rows
)

incident_df.to_csv(
    "data/retail_incident_logs.csv",
    index=False
)

print("Incident logs generated!")

# =====================================================
# AI-BASED SOP DOCUMENT GENERATION
# ONLY 4 API CALLS → LOW COST
# =====================================================

document_prompts = {

    "refund_policy":
    """
    Generate a professional enterprise retail refund policy.

    Include:
    - document control
    - purpose
    - scope
    - workflow
    - SLA
    - escalation rules
    - audit requirements
    - customer communication

    Make it detailed and enterprise-grade.
    """,

    "damaged_item_sop":
    """
    Generate a professional damaged item handling SOP
    for retail support operations.

    Include:
    - verification process
    - warehouse coordination
    - replacement workflow
    - escalation rules
    - SLA requirements
    - audit logging

    Make it company-level and detailed.
    """,

    "payment_failure_guide":
    """
    Generate a professional payment failure
    escalation guide.

    Include:
    - transaction verification
    - gateway troubleshooting
    - escalation workflow
    - SLA requirements
    - customer communication
    - monitoring and reporting

    Make it enterprise-grade.
    """,

    "order_delay_sop":
    """
    Generate a professional order delay
    troubleshooting guide.

    Include:
    - shipment validation
    - logistics coordination
    - delay investigation
    - escalation process
    - SLA requirements
    - customer communication

    Make it detailed and professional.
    """
}

# =====================================================
# GENERATE DOCUMENTS USING GEMINI
# =====================================================

print("Generating AI-based SOP documents...")

documents = {}

for doc_name, prompt in document_prompts.items():

    try:

        print(f"Generating {doc_name}...")

        response = model.generate_content(
            prompt
        )

        documents[doc_name] = response.text

        print(f"{doc_name} generated successfully!")

    except Exception as e:

        print(
            f"Gemini failed for {doc_name}"
        )

        print(e)

        # Fallback
        documents[doc_name] = f"""
        {doc_name}

        AI generation failed.
        Fallback document generated.
        """

print("All SOP documents generated!")

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

    title_para = Paragraph(
        f"<b>{title}</b>",
        styles['Title']
    )

    story.append(title_para)

    story.append(Spacer(1, 12))

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
# GENERATE TXT + PDF FILES
# =====================================================

print("Generating TXT and PDF files...")

for file_name, content in documents.items():

    txt_path = f"docs/{file_name}.txt"

    with open(
        txt_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)

    pdf_path = f"docs/{file_name}.pdf"

    create_pdf(
        pdf_path,
        file_name.replace("_", " ").title(),
        content
    )

print("Documents generated successfully!")

# =====================================================
# DATA QUALITY CHECKS
# =====================================================

print("\n========== DATA QUALITY CHECK ==========\n")

print("Missing Values:\n")

print(tickets_df.isnull().sum())

print("\nDuplicate Ticket IDs:")

print(
    tickets_df["ticket_id"].duplicated().sum()
)

print("\nDuplicate Incident Log IDs:")

print(
    incident_df["log_id"].duplicated().sum()
)

print("\nData quality checks completed!")

# =====================================================
# AI-GENERATED README
# =====================================================

readme_prompt = """
Generate a professional README.md
for an AI-Based Retail Incident
Ticket Analyzer project.

Include:
- project overview
- features
- generated files
- technologies used
- workflow explanation
- use cases
"""

try:

    response = model.generate_content(
        readme_prompt
    )

    readme_content = response.text

except:

    readme_content = """
    RETAIL AI PROJECT
    """

with open(
    "README.md",
    "w",
    encoding="utf-8"
) as f:

    f.write(readme_content)

print("README.md generated successfully!")

# =====================================================
# SAMPLE OUTPUT
# =====================================================

print("\n========== SAMPLE RETAIL TICKETS ==========\n")

print(tickets_df.head())

print("\n========== SAMPLE INCIDENT LOGS ==========\n")

print(incident_df.head())

print("\nAll project files generated successfully!")