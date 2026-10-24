from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CorrectionReport, CorrectionType, CorrectionStatus


def corrections_page(request):
    """
    Public correction and feedback submission page.
    Adheres to Section 2 and Section 11 guardrails: No sensitive case intake.
    """
    if request.method == "POST":
        reference = request.POST.get('reference_page_or_topic', '').strip()
        correction_type = request.POST.get('correction_type', CorrectionType.FACTUAL_ERROR)
        description = request.POST.get('specific_error_description', '').strip()
        suggested = request.POST.get('suggested_correction', '').strip()
        source = request.POST.get('official_source_proof', '').strip()
        name = request.POST.get('submitter_name', '').strip()
        email = request.POST.get('submitter_email', '').strip()

        if reference and description and source:
            CorrectionReport.objects.create(
                reference_page_or_topic=reference,
                correction_type=correction_type,
                specific_error_description=description,
                suggested_correction=suggested,
                official_source_proof=source,
                submitter_name=name,
                submitter_email=email,
                status=CorrectionStatus.PENDING,
            )
            messages.success(
                request, 
                "Your correction submission has been logged into the editorial review queue. Thank you for helping keep public legal information accurate."
            )
            return redirect('corrections_page')
        else:
            messages.error(
                request, 
                "Please fill in all required fields (Reference, Error Description, and Official Source Citation)."
            )

    # Fetch recently resolved public corrections for transparency
    resolved_corrections = CorrectionReport.objects.filter(
        status=CorrectionStatus.RESOLVED
    ).exclude(public_resolution_note='')[:5]

    initial_ref = request.GET.get('ref') or request.GET.get('doc') or ''

    return render(request, 'pages/corrections.html', {
        'correction_types': CorrectionType.choices,
        'resolved_corrections': resolved_corrections,
        'initial_ref': initial_ref,
    })
