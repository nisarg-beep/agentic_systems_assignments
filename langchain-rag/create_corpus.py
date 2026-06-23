from pathlib import Path 

BASE_DIR=Path("/Users/khushijain/Desktop/iitr /agentic_systems_assignments/langchain-rag/documents")

documents= {
    "quiet_hours.md": """
    # Quiet Hours Policy

    Quiet hours are from 10:00 PM to 6:00 AM on all weekdays.
    During quiet hours, loud music, group calls, and hallway gatherings are not allowed.
    Violations may lead to a written warning.
""",

    "guest_policy.md": """
    # Guest Policy

    Day guests are allowed only between 9:00 AM and 8:00 PM.
    Overnight guests require prior warden approval at least 24 hours in advance.
    Maximum two guests per room at any time.
    """,
}

for filename , content in documents.items():
    file_path=BASE_DIR/filename
    file_path.write_text(content.strip(), encoding= "utf-8")
