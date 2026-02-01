import re
import logging

logger = logging.getLogger(__name__)

class ViolationDetector:
    """Detects potential compliance violations in text"""
    
    def __init__(self):
        # HIPAA patterns: SSN, Medical Record Numbers, Patient Names
        self.hipaa_patterns = {
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'medical_record': r'MRN:\s*\d+',
            'patient_id': r'Patient\s*ID:\s*\d+',
        }
        
        # GDPR patterns: Personal identifiers, email, phone
        self.gdpr_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        }
        
        # CCPA patterns: Consumer personal information
        self.ccpa_patterns = {
            'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            'drivers_license': r'DL:\s*\d{5,8}',
            'passport': r'Passport:\s*\d{6,9}',
        }

    def scan_text_for_violations(self, text: str) -> list:
        """Scan text and return detected violations"""
        detections = []
        
        # Check HIPAA patterns
        for violation_type, pattern in self.hipaa_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detections.append({
                    'regulation': 'HIPAA',
                    'type': violation_type,
                    'matches': matches,
                    'count': len(matches)
                })
        
        # Check GDPR patterns
        for violation_type, pattern in self.gdpr_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detections.append({
                    'regulation': 'GDPR',
                    'type': violation_type,
                    'matches': matches,
                    'count': len(matches)
                })
        
        # Check CCPA patterns
        for violation_type, pattern in self.ccpa_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detections.append({
                    'regulation': 'CCPA',
                    'type': violation_type,
                    'matches': matches,
                    'count': len(matches)
                })
        
        logger.info(f"Scan complete: {len(detections)} violation types detected")
        return detections

# Global detector instance
detector = ViolationDetector()

def scan_text_for_violations(text: str) -> list:
    """Public function to scan text"""
    return detector.scan_text_for_violations(text)