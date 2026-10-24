"""
URL Configuration for Gujarat UCC Digital Public Information Platform.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.core import views as core_views
from apps.core import admin_views
from apps.topics import views as topic_views
from apps.explainers import views as explainer_views
from apps.library import views as library_views
from apps.timeline import views as timeline_views
from apps.news import views as news_views
from apps.glossary_faq import views as faq_views
from apps.corrections import views as correction_views

# Customize Admin Site branding
admin.site.site_header = "Gujarat UCC Platform • Editorial & Legal CMS"
admin.site.site_title = "Gujarat UCC Admin"
admin.site.index_title = "Publishing Queue & Legal Provenance Dashboard"

urlpatterns = [
    # Standard Django Admin
    path('admin/', admin.site.urls),
    
    # Custom Editorial & Legal Review Admin Dashboard
    path('portal-admin/', admin_views.admin_dashboard_home, name='portal_admin_home'),
    path('portal-admin/login/', admin_views.portal_login_view, name='portal_admin_login'),
    path('portal-admin/logout/', admin_views.portal_logout_view, name='portal_admin_logout'),
    path('portal-admin/content/', admin_views.admin_content_list, name='portal_admin_content'),
    path('portal-admin/content/explainer/add/', admin_views.admin_explainer_edit, name='portal_admin_explainer_add'),
    path('portal-admin/content/explainer/<int:pk>/edit/', admin_views.admin_explainer_edit, name='portal_admin_explainer_edit'),
    path('portal-admin/review-queue/', admin_views.admin_review_queue, name='portal_admin_review_queue'),
    path('portal-admin/settings/', admin_views.admin_settings_view, name='portal_admin_settings'),
    path('portal-admin/roles/', admin_views.admin_roles_view, name='portal_admin_roles'),
    path('portal-admin/audit-logs/', admin_views.admin_audit_logs_view, name='portal_admin_audit_logs'),
    
    # Core Public Pages
    path('', core_views.home, name='home'),
    path('understand-ucc/', core_views.understand_ucc, name='understand_ucc'),
    path('about/', core_views.about_page, name='about_page'),
    path('editorial-policy/', core_views.editorial_policy, name='editorial_policy'),
    path('privacy/', core_views.privacy_policy, name='privacy_policy'),
    path('terms/', core_views.terms_page, name='terms_page'),
    path('search/', core_views.search_page, name='search_page'),
    
    # Topics
    path('topics/', topic_views.topics_list, name='topics_list'),
    path('topics/<slug:slug>/', topic_views.topic_detail, name='topic_detail'),
    
    # Plain-Language Explainers
    path('explainers/', explainer_views.explainers_list, name='explainers_list'),
    path('explainers/<slug:slug>/', explainer_views.explainer_detail, name='explainer_detail'),
    
    # Legal Library (Acts, Gazettes, Rules)
    path('library/', library_views.library_list, name='library_list'),
    path('library/<slug:slug>/', library_views.document_detail, name='document_detail'),
    
    # Timeline
    path('timeline/', timeline_views.timeline_page, name='timeline_page'),
    
    # News & Updates
    path('news/', news_views.news_list, name='news_list'),
    path('news/<slug:slug>/', news_views.news_detail, name='news_detail'),
    
    # FAQs & Glossary
    path('faq-glossary/', faq_views.faq_glossary, name='faq_glossary'),
    
    # Corrections & Feedback
    path('corrections/', correction_views.corrections_page, name='corrections_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
