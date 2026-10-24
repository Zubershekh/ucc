from django.shortcuts import render, get_object_or_404
from .models import LegalDocument, DocumentType
from apps.core.models import StatusTaxonomy


def library_list(request):
    """
    Official Legal Library Repository:
    Acts, Gazette notifications, rules, forms, official circulars, and committee materials.
    Filter by type and status.
    """
    doc_type = request.GET.get('type')
    status_filter = request.GET.get('status')
    
    documents = LegalDocument.objects.all()
    if doc_type:
        documents = documents.filter(document_type=doc_type)
    if status_filter:
        documents = documents.filter(status=status_filter)
        
    return render(request, 'pages/library_list.html', {
        'documents': documents,
        'doc_types': DocumentType.choices,
        'status_choices': StatusTaxonomy.CHOICES,
        'selected_type': doc_type,
        'selected_status': status_filter,
    })


def document_detail(request, slug):
    """Primary Legal Source Record Detail with provenance, checksum, and downloads."""
    document = get_object_or_404(LegalDocument, slug=slug)
    related_explainers = document.explainers.filter(editorial_status='PUBLISHED')
    
    return render(request, 'pages/document_detail.html', {
        'document': document,
        'related_explainers': related_explainers,
    })
