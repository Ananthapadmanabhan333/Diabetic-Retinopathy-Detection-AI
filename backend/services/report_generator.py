import json
from pathlib import Path
import datetime

class ReportGenerator:
    def __init__(self, output_dir="./reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_json_report(self, patient_data, ai_results):
        report = {
            "resourceType": "DiagnosticReport",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "12345-6", # Dummy LOINC
                        "display": "Retina examination report"
                    }
                ]
            },
            "subject": {
                "reference": f"Patient/{patient_data['patient_id']}"
            },
            "issued": datetime.datetime.now().isoformat(),
            "results": ai_results
        }
        
        file_path = self.output_dir / f"{patient_data['patient_id']}_report.json"
        with open(file_path, "w") as f:
            json.dump(report, f, indent=4)
        return str(file_path)

    def generate_pdf_report(self, patient_data, ai_results):
        """
        Placeholder for PDF generation. 
        In production, we would use reportlab or weasyprint.
        """
        file_path = self.output_dir / f"{patient_data['patient_id']}_report.pdf"
        # Dummy PDF creation
        with open(file_path, "w") as f:
            f.write("%PDF-1.4\n%Dummy PDF for DR Report\n")
        return str(file_path)

if __name__ == "__main__":
    generator = ReportGenerator()
    print("Report Generator initialized.")
