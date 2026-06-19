import re

class PhishingAnalyzer:
    def __init__(self):
        self.red_flags = {
            'urgent_language': ['urgent', 'immediate', 'act now', 'verify your account', 'suspended', 'limited time'],
            'suspicious_links': ['bit.ly', 'tinyurl', 'ow.ly', 'short.link', 'shorturl'],
            'suspicious_domains': ['@gmail.com', '@yahoo.com', '@outlook.com', '@hotmail.com'],
            'spoofed_domains': ['paypall.com', 'amaz0n.com', 'g00gle.com', 'micros0ft.com'],
            'financial_keywords': ['bank', 'credit card', 'paypal', 'money', 'transfer', 'deposit', 'withdraw'],
            'personal_info_keywords': ['ssn', 'social security', 'password', 'username', 'login', 'account number'],
            'attachments': ['.exe', '.zip', '.rar', '.scr', '.bat', '.vbs', '.js']
        }
        
        self.phishing_samples = [
            {
                'sender': 'security@paypall.com',
                'subject': 'URGENT: Your PayPal Account Has Been Suspended',
                'body': """Dear User,

We have detected unusual activity on your PayPal account. To avoid permanent suspension, please verify your account immediately by clicking the link below:

http://bit.ly/verify-paypal-account

If you do not verify within 24 hours, your account will be permanently locked.

Thank you,
PayPal Security Team"""
            },
            {
                'sender': 'no-reply@bankofamerica-secure.com',
                'subject': 'Important: Unusual Login Activity Detected',
                'body': """Dear Customer,

We detected a login attempt from an unknown device. Please confirm your identity by visiting:

https://secure.bankofamerica.verify.com

Please enter your SSN and account number to verify.

Regards,
Bank of America Security"""
            },
            {
                'sender': 'info@amaz0n.com',
                'subject': 'Your Amazon Order #A2B3C4 has been delayed',
                'body': """Hello Customer,

Your recent Amazon order has been delayed due to a payment issue. Please update your payment information immediately:

http://tinyurl.com/amazon-payment-update

Failure to update will result in order cancellation.

Amazon Customer Service"""
            }
        ]

    def analyze_email(self, sender, subject, body):
        findings = []
        severity = 0
        
        text = f"{sender} {subject} {body}".lower()
        
        for category, keywords in self.red_flags.items():
            for keyword in keywords:
                if keyword in text:
                    findings.append({
                        'category': category.replace('_', ' ').title(),
                        'keyword': keyword,
                        'severity': 'High' if category in ['suspicious_links', 'financial_keywords', 'personal_info_keywords'] else 'Medium'
                    })
                    if category in ['suspicious_links', 'financial_keywords', 'personal_info_keywords']:
                        severity += 2
                    else:
                        severity += 1
        
        risk_level = "Critical" if severity >= 10 else "High" if severity >= 6 else "Medium" if severity >= 3 else "Low"
        
        return {
            'findings': findings,
            'severity': severity,
            'risk_level': risk_level,
            'total_red_flags': len(findings)
        }

    def display_analysis(self, index, email, analysis):
        print("\n" + "=" * 60)
        print(f"   PHISHING ANALYSIS #{index}")
        print("=" * 60)
        
        print(f"\nSender: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"\nBody: {email['body'][:200]}...")
        
        print("\n[ANALYSIS RESULTS]")
        print("-" * 40)
        print(f"Total Red Flags Found: {analysis['total_red_flags']}")
        print(f"Risk Level: {analysis['risk_level']}")
        print(f"Severity Score: {analysis['severity']}/10")
        
        if analysis['findings']:
            print("\nRed Flags Detected:")
            for finding in analysis['findings'][:10]:
                print(f"  ⚠️ {finding['category']}: '{finding['keyword']}' ({finding['severity']})")
        
        print("\n[CONCLUSION]")
        print("-" * 40)
        if analysis['risk_level'] in ['Critical', 'High']:
            print("This message is LIKELY A PHISHING ATTEMPT. Do NOT click any links or respond.")
        elif analysis['risk_level'] == 'Medium':
            print("This message shows suspicious signs. Verify the sender's identity before taking action.")
        else:
            print("This message appears relatively safe, but always verify unexpected requests.")

    def explain_phishing_techniques(self):
        print("\n" + "=" * 60)
        print("   COMMON PHISHING TECHNIQUES")
        print("=" * 60)
        
        techniques = [
            {"name": "Urgency/Threats", "description": "Creates panic by claiming account suspension, limited time, or legal action."},
            {"name": "Spoofed Sender Address", "description": "Uses email addresses that look legitimate but have slight misspellings."},
            {"name": "Suspicious Links", "description": "Uses URL shorteners or misspelled domains to hide the true destination."},
            {"name": "Request for Personal Info", "description": "Asks for passwords, SSN, credit card numbers, or login credentials."},
            {"name": "Sense of Authority", "description": "Pretends to be from banks, government agencies, or trusted companies."},
            {"name": "Too Good to Be True", "description": "Offers prizes, refunds, or job opportunities that seem unrealistic."}
        ]
        
        for tech in techniques:
            print(f"\n🔴 {tech['name']}")
            print(f"   {tech['description']}")

    def run(self):
        print("\n" + "=" * 60)
        print("   PHISHING AWARENESS ANALYSIS")
        print("=" * 60)
        
        print("\n[1] Analyzing Phishing Samples...")
        
        for i, email in enumerate(self.phishing_samples, 1):
            analysis = self.analyze_email(email['sender'], email['subject'], email['body'])
            self.display_analysis(i, email, analysis)
        
        self.explain_phishing_techniques()
        
        print("\n[SECURITY TIPS]")
        print("-" * 40)
        print("1. Always verify sender addresses before clicking links")
        print("2. Hover over links to see the actual URL before clicking")
        print("3. Look for spelling errors and unusual email addresses")
        print("4. Never share personal information via email")
        print("5. Enable Two-Factor Authentication (2FA) where possible")
        print("6. When in doubt, contact the company directly using official channels")
        
        print("\n" + "=" * 60)
        print("   PHISHING ANALYSIS COMPLETE")
        print("=" * 60)

def main():
    analyzer = PhishingAnalyzer()
    analyzer.run()

if __name__ == "__main__":
    main()