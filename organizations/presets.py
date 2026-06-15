ORGANIZATION_PRESETS = {
    "education": {
        "fields": [
            {"name": "HSC Batch", "key": "hsc_batch", "field_type": "text"},
            {"name": "IELTS Score", "key": "ielts_score", "field_type": "number"},
            {"name": "Preferred Country", "key": "preferred_country", "field_type": "select"},
            {"name": "Visa Status", "key": "visa_status", "field_type": "select"},
            {"name": "Guardian Name", "key": "guardian_name", "field_type": "text"},
        ],
        "tags": ["IELTS", "Canada", "Australia", "Hot Lead", "Visa Applied"],
        "lists": ["IELTS Students", "Canada Leads", "Visa Followup"],
    },
    "gym": {
        "fields": [
            {"name": "Membership Type", "key": "membership_type", "field_type": "select"},
            {"name": "Trainer", "key": "trainer", "field_type": "text"},
            {"name": "Goal Weight", "key": "goal_weight", "field_type": "number"},
            {"name": "Workout Plan", "key": "workout_plan", "field_type": "textarea"},
            {"name": "Renewal Date", "key": "renewal_date", "field_type": "date"},
        ],
        "tags": ["Active Member", "Personal Training", "Renewal Due", "Inactive"],
        "lists": ["Active Members", "Renewal Followup", "Personal Training Leads"],
    },
    "restaurant": {
        "fields": [
            {"name": "Favorite Item", "key": "favorite_item", "field_type": "text"},
            {"name": "Branch", "key": "branch", "field_type": "text"},
            {"name": "Birthday", "key": "birthday", "field_type": "date"},
            {"name": "Membership Tier", "key": "membership_tier", "field_type": "select"},
        ],
        "tags": ["VIP", "Birthday Offer", "Regular Customer", "Inactive Customer"],
        "lists": ["VIP Customers", "Birthday Campaign", "Regular Customers"],
    },
    "ecommerce": {
        "fields": [
            {"name": "Last Purchase Date", "key": "last_purchase_date", "field_type": "date"},
            {"name": "Order Count", "key": "order_count", "field_type": "number"},
            {"name": "Cart Status", "key": "cart_status", "field_type": "select"},
            {"name": "Preferred Category", "key": "preferred_category", "field_type": "text"},
        ],
        "tags": ["High Value", "Cart Abandoned", "Repeat Buyer", "First Purchase"],
        "lists": ["Repeat Buyers", "Cart Abandonment", "High Value Customers"],
    },
    "agency": {
        "fields": [
            {"name": "Lead Source", "key": "lead_source", "field_type": "text"},
            {"name": "Budget", "key": "budget", "field_type": "number"},
            {"name": "Project Type", "key": "project_type", "field_type": "select"},
            {"name": "Decision Stage", "key": "decision_stage", "field_type": "select"},
        ],
        "tags": ["Hot Lead", "Proposal Sent", "Client", "Follow Up"],
        "lists": ["Hot Leads", "Proposal Pipeline", "Clients"],
    },
}
