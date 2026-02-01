# Compliance Rules for HIPAA, GDPR, CCPA

class ComplianceRuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def check_compliance(self, data):
        violations = []
        for rule in self.rules:
            if not rule.is_compliant(data):
                violations.append(rule)
        return violations

class HIPAAComplianceRule:
    def is_compliant(self, data):
        # Implement HIPAA compliance check logic
        return True  # Placeholder for actual compliance check

class GDPRComplianceRule:
    def is_compliant(self, data):
        # Implement GDPR compliance check logic
        return True  # Placeholder for actual compliance check

class CCPAComplianceRule:
    def is_compliant(self, data):
        # Implement CCPA compliance check logic
        return True  # Placeholder for actual compliance check

# Example Usage:
# engine = ComplianceRuleEngine()
# engine.add_rule(HIPAAComplianceRule())
# engine.add_rule(GDPRComplianceRule())
# engine.add_rule(CCPAComplianceRule())
# violations = engine.check_compliance(data)  # where data is the input to check compliance