# business_admin_agent.py

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger("BusinessAdminAgent")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class BusinessAdminAgent:
    def __init__(self, doc_dir: str = "data/documents"):
        self.invoice_dir = os.path.join(doc_dir, "invoices")
        self.contract_dir = os.path.join(doc_dir, "contracts")

        try:
            os.makedirs(self.invoice_dir, exist_ok=True)
            os.makedirs(self.contract_dir, exist_ok=True)
            logger.info("[Init] Directories created successfully.")
        except Exception as e:
            logger.exception(f"[Init] Failed to create directories: {e}")
            raise

    def create_invoice(self, invoice_id: str, client_name: str, items: List[Dict[str, float]]) -> Dict:
        if not invoice_id or not client_name or not items:
            raise ValueError("Invoice ID, client name, and items are required.")

        logger.info(f"[Invoice] Creating invoice for {client_name} with ID {invoice_id}")
        date_str = datetime.utcnow().strftime("%Y-%m-%d")

        try:
            total = round(sum(item.get('qty', 0) * item.get('price', 0.0) for item in items), 2)
        except Exception as e:
            logger.error(f"[Invoice] Error calculating total: {e}")
            raise

        invoice = {
            "invoice_id": invoice_id,
            "client": client_name,
            "date": date_str,
            "items": items,
            "total": total
        }

        path = os.path.join(self.invoice_dir, f"{invoice_id}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(invoice, f, indent=2)
            logger.info(f"[Invoice] Invoice {invoice_id} saved successfully.")
        except Exception as e:
            logger.exception(f"[Invoice] Failed to save invoice: {e}")
            raise IOError(f"Failed to save invoice: {e}")

        return invoice

    def generate_contract(
        self,
        party_a: str,
        party_b: str,
        contract_type: str = "NDA",
        details: Optional[Dict[str, str]] = None
    ) -> Dict:
        if not party_a or not party_b:
            raise ValueError("Both parties must be specified for contract generation.")

        now = datetime.utcnow().strftime("%Y-%m-%d")
        details = details or {}

        logger.info(f"[Contract] Generating {contract_type.upper()} contract between {party_a} and {party_b}")

        contract_text = f"""
        ===============================
               {contract_type.upper()} CONTRACT
        ===============================

        DATE: {now}

        BETWEEN:
        Party A: {party_a}
        AND
        Party B: {party_b}

        TERMS:
        - This contract is effective from {now}.
        - Confidentiality must be maintained at all times.
        - Scope: {details.get('scope', 'General business engagement')}
        - Duration: {details.get('duration', '12 months')}
        - Termination: {details.get('termination', '30 days notice by either party')}

        SIGNATURES:
        ___________________        ___________________
        {party_a}                 {party_b}
        """

        safe_filename = f"{party_a}_to_{party_b}_{contract_type}_{now}".replace(" ", "_").replace("/", "-")
        filename = f"{safe_filename}.txt"
        path = os.path.join(self.contract_dir, filename)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(contract_text.strip())
            logger.info(f"[Contract] Contract saved as {filename}")
        except Exception as e:
            logger.exception(f"[Contract] Failed to write contract: {e}")
            raise IOError(f"Failed to write contract: {e}")

        return {
            "status": "created",
            "file": filename,
            "path": path,
            "text": contract_text.strip()
        }

    def summarize_meeting(self, transcript_text: str) -> str:
        logger.info("[Meeting] Summarizing meeting transcript.")

        if not transcript_text.strip():
            logger.warning("[Meeting] Empty transcript provided.")
            return "Transcript is empty."

        summary_lines = []
        paragraphs = [p.strip() for p in transcript_text.split("\n") if p.strip()]

        for line in paragraphs:
            l_lower = line.lower()
            if "action" in l_lower:
                summary_lines.append(f"ACTION ITEM: {line}")
            elif "decision" in l_lower:
                summary_lines.append(f"DECISION: {line}")
            elif "agenda" in l_lower:
                summary_lines.append(f"AGENDA: {line}")

        if not summary_lines:
            logger.info("[Meeting] No key items found in transcript.")
            summary_lines.append("No key actions or decisions found in transcript.")

        return "\n".join(summary_lines)
