from agents.business_agent import BusinessAdminAgent
from utils.logger import log_task

agent = BusinessAdminAgent()

async def create_invoice(args):
    if len(args) < 3:
        return {"error": "Usage: create_invoice <invoice_id> <client> <item_json>"}
    try:
        invoice_id = args[0]
        client = args[1]
        items = json.loads(" ".join(args[2:]))
        result = agent.create_invoice(invoice_id, client, items)
        log_task("create_invoice", "complete", str(result))
        return result
    except Exception as e:
        return {"error": str(e)}

async def generate_contract(args):
    if len(args) < 2:
        return {"error": "Usage: generate_contract <party_a> <party_b> [contract_type] [details_json]"}
    party_a, party_b = args[0], args[1]
    contract_type = args[2] if len(args) >= 3 else "NDA"
    details = json.loads(" ".join(args[3:])) if len(args) > 3 else {}
    result = agent.generate_contract(party_a, party_b, contract_type, details)
    log_task("generate_contract", "complete", str(result))
    return result

async def summarize_meeting(args):
    if not args:
        return {"error": "Usage: summarize_meeting <transcript_text>"}
    text = " ".join(args)
    result = agent.summarize_meeting(text)
    log_task("summarize_meeting", "complete", result)
    return {"summary": result}

def register():
    return {
        "create_invoice": create_invoice,
        "generate_contract": generate_contract,
        "summarize_meeting": summarize_meeting
    }
