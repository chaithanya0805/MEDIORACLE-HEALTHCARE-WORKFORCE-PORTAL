from django.db import models
from apps.compliance.models import ComplianceRule
from apps.professionals.models import Credential, CredentialStatus
import datetime

class ComplianceService:
    @staticmethod
    def check_professional_for_shift(professional, shift):
        # Fetch compliance rules for this role (either global or facility-specific)
        rules = ComplianceRule.objects.filter(
            role=shift.role,
            active=True
        ).filter(
            models.Q(facility=shift.facility) | models.Q(facility__isnull=True)
        )

        missing = []
        expired = []
        warnings = []
        eligible = True

        for rule in rules:
            cred_type = rule.credential_type
            # Look for verified credentials of this type for the professional
            matching_creds = Credential.objects.filter(
                professional=professional,
                credential_type=cred_type
            )

            # Filter for verified credentials
            verified_creds = matching_creds.filter(verification_status=CredentialStatus.VERIFIED)

            if not verified_creds.exists():
                # Check if there is a pending or submitted credential
                pending_or_sub = matching_creds.filter(
                    verification_status__in=[CredentialStatus.PENDING, CredentialStatus.SUBMITTED]
                ).exists()
                
                status_txt = "Pending Verification" if pending_or_sub else "Not Uploaded"
                
                if rule.required:
                    eligible = False
                    missing.append({
                        "credential_type": cred_type.name,
                        "code": cred_type.code,
                        "status": status_txt
                    })
                else:
                    warnings.append(f"Missing non-mandatory credential: {cred_type.name} ({status_txt})")
            else:
                # Validate expiry
                active_cred = verified_creds.latest('issue_date')
                days = active_cred.expiry_days
                
                if days <= 0:
                    if rule.required:
                        eligible = False
                    expired.append({
                        "credential_type": cred_type.name,
                        "code": cred_type.code,
                        "number": active_cred.credential_number,
                        "expired_days_ago": abs(days)
                    })
                elif days < rule.minimum_validity_days:
                    warnings.append(f"{cred_type.name} valid for only {days} days, minimum required is {rule.minimum_validity_days} days")
                elif days <= 30:
                    warnings.append(f"{cred_type.name} expires in {days} days")
        
        return {
            "eligible": eligible,
            "missing": missing,
            "expired": expired,
            "warnings": warnings
        }
