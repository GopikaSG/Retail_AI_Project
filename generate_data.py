# =====================================================
# IMPORTS
# =====================================================

import os
import json
import random
from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
from faker import Faker

# Gemini AI
import google.generativeai as genai

# Load .env
from dotenv import load_dotenv

# PDF Generation
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

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("docs", exist_ok=True)

print("Project folders created successfully!")

# =====================================================
# LOAD ENV VARIABLES
# =====================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:

    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )

# =====================================================
# GEMINI CONFIGURATION
# =====================================================

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

print("Gemini configured successfully!")

# =====================================================
# AI-BASED TICKET GENERATION
# =====================================================

print("\nGenerating AI-based retail tickets...")

ticket_prompt = """
Generate 20 realistic retail support tickets.

Output STRICTLY in valid CSV format.

Columns:
issue_type,ticket_text,priority,status

Requirements:
- enterprise retail support tone
- realistic customer complaints
- realistic operational issues
- no markdown
- no explanations
- no code blocks
"""

try:

    response = model.generate_content(
        ticket_prompt
    )

    csv_text = response.text.strip()

    print("\n========== RAW AI OUTPUT ==========\n")

    print(csv_text)

except Exception as e:

    print("Gemini failed!")

    print(e)

    # Fallback sample
    csv_text = """
issue_type,ticket_text,priority,status
Order Delay,"My shipment has not arrived for 5 days",High,Open
Refund Issue,"Refund still pending after return pickup",Medium,In Progress
Payment Failure,"Amount deducted but no order created",Critical,Escalated
Product Defect,"Delivered product is damaged",High,Open
Account Issue,"Unable to access my account",Medium,Resolved
"""

# =====================================================
# CONVERT TO DATAFRAME
# =====================================================

base_df = pd.read_csv(
    StringIO(csv_text)
)

print("\nAI-generated rows loaded!")

# =====================================================
# MASTER DATA
# =====================================================

channels = [
    "Email",
    "Chat",
    "Phone",
    "Mobile App"
]

locations = [
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Chennai",
    "Pune"
]

teams = [
    "Customer Support",
    "Warehouse Operations",
    "Payment Support",
    "Technical Support",
    "Fraud Investigation",
    "Logistics Team"
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Wallet"
]

customer_tiers = [
    "Silver",
    "Gold",
    "Platinum"
]

# =====================================================
# EXPAND TO 150 ROWS
# =====================================================

print("\nExpanding dataset to 150 rows...")

expanded_rows = []

for i in range(150):

    row = base_df.sample(1).iloc[0]

    city = random.choice(locations)

    created_time = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23)
    )

    expanded_rows.append({

        "ticket_id":
            f"{city[:3].upper()}-TKT{i:04}",

        "customer_id":
            f"CUST{random.randint(1000,9999)}",

        "order_id":
            f"ORD{random.randint(10000,99999)}",

        "issue_type":
            row["issue_type"],

        "ticket_text":
            row["ticket_text"],

        "priority":
            row["priority"],

        "status":
            row["status"],

        "channel":
            random.choice(channels),

        "location":
            city,

        "assigned_team":
            random.choice(teams),

        "payment_method":
            random.choice(payment_methods),

        "customer_tier":
            random.choice(customer_tiers),

        "requires_escalation":
            random.choice(["Yes", "No"]),

        "sla_breach":
            random.choice(["Yes", "No"]),

        "resolution_time_hours":
            random.randint(1, 72),

        "created_at":
            created_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    })

tickets_df = pd.DataFrame(expanded_rows)

# =====================================================
# SAVE TICKETS CSV
# =====================================================

tickets_df.to_csv(
    "data/retail_tickets.csv",
    index=False
)

print("Retail ticket dataset generated successfully!")

# =====================================================
# INCIDENT LOG GENERATION (JSON FORMAT)
# =====================================================

print("\nGenerating incident logs in JSON format...")

incident_prompt = """
Generate 10 realistic retail operational incident logs.

Return ONLY valid JSON.

Expected JSON format:

[
  {
    "incident_type": "...",
    "description": "...",
    "severity": "..."
  }
]

Requirements:
- enterprise operational tone
- realistic retail technical issues
- outage scenarios
- logistics problems
- payment failures
- no markdown
- no explanations
"""

try:

    incident_response = model.generate_content(
        incident_prompt
    )

    incident_json_text = (
        incident_response.text
        .strip()
        .replace("```json", "")
        .replace("```", "")
    )

    # Convert JSON string to Python list
    incident_data = json.loads(
        incident_json_text
    )

    print("\n========== RAW INCIDENT JSON ==========\n")

    print(
        json.dumps(
            incident_data,
            indent=2
        )
    )

except Exception as e:

    print("Gemini incident generation failed!")

    print(e)

    # Fallback JSON data
    incident_data = [
        {
            "incident_type":
                "Payment Gateway Failure",

            "description":
                "Payment transactions timing out during checkout",

            "severity":
                "Critical"
        },

        {
            "incident_type":
                "Website Downtime",

            "description":
                "Retail checkout service unavailable",

            "severity":
                "High"
        },

        {
            "incident_type":
                "Warehouse Delay",

            "description":
                "Shipment processing backlog detected",

            "severity":
                "Medium"
        }
    ]

# =====================================================
# CREATE INCIDENT DATAFRAME
# =====================================================

incident_rows = []

for i in range(30):

    row = random.choice(
        incident_data
    )

    incident_rows.append({

        "log_id":
            f"LOG{i:03}",

        "incident_type":
            row["incident_type"],

        "description":
            row["description"],

        "severity":
            row["severity"],

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

# =====================================================
# SAVE INCIDENT FILES
# =====================================================

# CSV
incident_df.to_csv(
    "data/retail_incident_logs.csv",
    index=False
)

# JSON
incident_df.to_json(
    "data/retail_incident_logs.json",
    orient="records",
    indent=4
)

print(
    "Incident logs generated successfully!"
)

print(
    "Saved as CSV and JSON."
)

# =====================================================
# ENTERPRISE SOP DOCUMENTS
# =====================================================

topics = {

    "sop_order_delay":
        "order delay handling",

    "sop_product_defect":
        "product defect handling",

    "sop_account_issue":
        "customer account issue handling",

    "sop_fraud_alert":
        "retail fraud alert handling"
}

documents = {}

print("\nGenerating enterprise SOP documents...")

for file_name, topic in topics.items():

    prompt = f"""
    Generate a detailed enterprise retail SOP document.

    TOPIC:
    {topic}

    STRICT FORMAT:

    Document Title
    Version
    Covers

    SECTION 1 — OVERVIEW

    SECTION 2 — COMMON CAUSES

    SECTION 3 — STEP-BY-STEP RESOLUTION PROCEDURE

    SECTION 4 — ESCALATION CRITERIA

    SECTION 5 — PREVENTION TIPS

    REQUIREMENTS:
    - realistic retail operations terminology
    - numbered workflow steps
    - escalation logic
    - internal operational references
    - professional customer support language
    - make it detailed and enterprise-grade
    - generate 2-3 pages worth of content
    """

    try:

        print(f"Generating {file_name}...")

        response = model.generate_content(
            prompt
        )

        documents[file_name] = response.text

        print(f"{file_name} generated!")

    except Exception as e:

        print(
            f"Gemini failed for {file_name}"
        )

        print(e)

        documents[file_name] = f"""
        SOP generation failed for:
        {topic}
        """

# =====================================================
# PDF CREATION FUNCTION
# =====================================================

def create_pdf(
    file_path,
    title,
    content
):

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

print("\nGenerating TXT and PDF SOP files...")

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
        file_name.replace(
            "_",
            " "
        ).title(),
        content
    )

print("SOP documents generated successfully!")

# =====================================================
# DATA QUALITY CHECKS
# =====================================================

print("\n========== DATA QUALITY CHECK ==========\n")

print("Missing Values:\n")

print(tickets_df.isnull().sum())

print("\nDuplicate Ticket IDs:")

print(
    tickets_df["ticket_id"]
    .duplicated()
    .sum()
)

print("\nDuplicate Incident Log IDs:")

print(
    incident_df["log_id"]
    .duplicated()
    .sum()
)

print("\nData quality checks completed!")

# =====================================================
# SAMPLE OUTPUT
# =====================================================

print("\n========== SAMPLE TICKETS ==========\n")

print(tickets_df.head())

print("\n========== SAMPLE INCIDENT LOGS ==========\n")

print(incident_df.head())

print("\nAll project files generated successfully!")