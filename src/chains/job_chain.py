from api.dynamic_faqs import generate_faqs

def get_job_faqs(job_role):
    """Generate FAQs dynamically for a specific job role."""
    return generate_faqs(job_role)