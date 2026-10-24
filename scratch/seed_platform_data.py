import os
import sys
import django
import datetime

sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import SiteSettings, StatusTaxonomy, EditorialStatus
from apps.topics.models import Topic
from apps.library.models import LegalDocument, DocumentType
from apps.timeline.models import TimelineEvent, TimelineCategory
from apps.explainers.models import Explainer
from apps.news.models import NewsArticle, NewsCategory, FactCheckStatus
from apps.glossary_faq.models import FAQ, GlossaryTerm

print("Seeding Gujarat UCC platform data...")

# 1. Superuser
admin_user, created = User.objects.get_or_create(
    username="admin",
    defaults={
        "email": "editor@uccgujarat.org",
        "is_staff": True,
        "is_superuser": True,
        "first_name": "Editorial",
        "last_name": "Admin"
    }
)
if created:
    admin_user.set_password("admin1234")
    admin_user.save()
    print("Created superuser: admin / admin1234")
else:
    print("Superuser admin already exists.")

# 2. SiteSettings
settings, _ = SiteSettings.objects.get_or_create(
    id=1,
    defaults={
        "site_name_en": "Gujarat UCC Digital Public Information Platform",
        "site_name_gu": "ગુજરાત સમાન નાગરિક સંહિતા (UCC) માહિતી મંચ",
        "current_status": StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        "status_summary_en": "Presidential Assent received on 17 Sept 2026; Published in Extraordinary Gazette on 1 Oct 2026. Commencement notification by State Govt awaited.",
        "status_summary_gu": "૧૭ સપ્ટેમ્બર ૨૦૨૬ના રોજ રાષ્ટ્રપતિની મંજૂરી પ્રાપ્ત; ૧ ઓક્ટોબર ૨૦૨૬ના રોજ અસાધારણ ગેઝેટમાં પ્રકાશિત. રાજ્ય સરકાર દ્વારા અમલવારી જાહેરનામું બાકી છે.",
        "last_verified_date": datetime.date(2026, 10, 24),
        "verified_official_source_url": "https://cms.neva.gov.in/NeVA/GJ/FileStructures/PaperLaid/15/8/AsIntroduced/17%20of2026_AsIn.pdf",
        "official_committee_url": "https://uccgujarat.in/",
        "show_announcement": True,
        "announcement_banner_en": "Official Notice: The Gujarat UCC Act has been Gazetted but is not yet operative. Provisions come into force only upon State Government commencement notification.",
        "announcement_banner_gu": "સત્તાવાર સૂચના: ગુજરાત UCC કાયદો ગેઝેટમાં પ્રકાશિત થયો છે પરંતુ હજુ સુધી અમલમાં આવ્યો નથી. રાજ્ય સરકાર દ્વારા અમલવારી જાહેરનામું બહાર પાડ્યા બાદ જ જોગવાઈઓ લાગુ થશે.",
    }
)
print("Configured SiteSettings.")

# 3. Core Topics (The 6 Pillars)
topics_data = [
    {
        "slug": "marriage-registration",
        "name_en": "Marriage & Registration",
        "name_gu": "લગ્ન અને નોંધણી",
        "order": 1,
        "icon_name": "ring",
        "summary_en": "Codified legal age, compulsory state registration of all marriages within prescribed timelines, and prohibition of child marriages.",
        "summary_gu": "લગ્નની કાયદાકીય વય, નિયત સમયમર્યાદામાં તમામ લગ્નોની ફરજિયાત નોંધણી અને બાળલગ્ન પર કડક પ્રતિબંધ.",
        "overview_body_en": "The Gujarat UCC establishes universal marriage regulations applicable across all communities. Key highlights include:\n1. Minimum marriageable age set at 21 for males and 21 for females.\n2. Compulsory registration of all solemnized marriages with the local registrar within 60 days.\n3. Complete prohibition of polygamy or bigamy while a spouse is living.\n4. Protection of religious ceremonies and customary rituals while mandating legal documentation.",
        "overview_body_gu": "ગુજરાત UCC તમામ સમુદાયો માટે સમાન લગ્ન નિયમો સ્થાપિત કરે છે:\n૧. લગ્ન માટે ન્યૂનતમ વય પુરુષ અને સ્ત્રી બંને માટે ૨૧ વર્ષ નિયત.\n૨. તમામ ધાર્મિક વિધિથી થયેલ લગ્નોની ૬૦ દિવસમાં સ્થાનિક રજિસ્ટ્રાર સમક્ષ ફરજિયાત નોંધણી.\n૩. હયાત પત્ની/પતિ હોય ત્યાં સુધી બીજા લગ્ન (બહુપત્નીત્વ/બહુપતિત્વ) પર સંપૂર્ણ પ્રતિબંધ.\n૪. ધાર્મિક રીતરિવાજોનું રક્ષણ પરંતુ કાનૂની દસ્તાવેજીકરણ ફરજિયાત."
    },
    {
        "slug": "divorce-dissolution",
        "name_en": "Divorce & Dissolution",
        "name_gu": "છૂટાછેડા અને વિસર્જન",
        "order": 2,
        "icon_name": "scale",
        "summary_en": "Uniform judicial grounds for dissolution of marriage, abolition of unilateral extra-judicial divorces, and fair alimony protections.",
        "summary_gu": "લગ્ન વિસર્જન માટે એકસમાન અદાલતી આધારો, એકપક્ષીય મૌખિક છૂટાછેડાની નાબૂદી અને ન્યાયી ભરણપોષણ સુરક્ષા.",
        "overview_body_en": "Divorce proceedings are brought strictly within the formal judicial purview:\n1. No marriage can be dissolved through unilateral declarations, customary pronunciations, or extra-judicial proclamations.\n2. Equal, neutral grounds available to both spouses including cruelty, desertion, adultery, and mutual consent.\n3. Statutory alimony and maintenance provisions safeguarding vulnerable spouses.",
        "overview_body_gu": "છૂટાછેડાની પ્રક્રિયાને સંપૂર્ણપણે અદાલતી અધિકારક્ષેત્ર હેઠળ લાવવામાં આવી છે:\n૧. કોઈ પણ લગ્ન એકપક્ષીય મૌખિક જાહેરાત કે બિન-અદાલતી પ્રથા દ્વારા વિસર્જિત કરી શકાશે નહીં.\n૨. પતિ અને પત્ની બંને માટે ક્રૂરતા, ત્યાગ, વ્યભિચાર અને પરસ્પર સંમતિ જેવા સમાન કાયદાકીય આધારો.\n૩. આર્થિક રીતે નબળા જીવનસાથીના હિતોનું રક્ષણ કરતી ન્યાયી ભરણપોષણ જોગવાઈ."
    },
    {
        "slug": "succession-inheritance",
        "name_en": "Succession & Inheritance",
        "name_gu": "વારસાઈ અને ઉત્તરાધિકાર",
        "order": 3,
        "icon_name": "tree",
        "summary_en": "Gender-equal intestate succession granting equal shares to daughters, sons, wives, and mothers in ancestral and self-acquired property.",
        "summary_gu": "પૂર્વજોની તેમજ સ્વ-અર્જિત સંપત્તિમાં દીકરીઓ, દીકરાઓ, પત્ની અને માતાને સંપૂર્ણ સમાન વારસા હક આપતી સમાન જોગવાઈ.",
        "overview_body_en": "Intestate succession rules are codified to ensure complete gender parity:\n1. Daughters and sons receive identical shares in estate distribution.\n2. Surviving widow and mother hold equal priority rights in Class-I heir classification.\n3. Removal of historical discriminatory personal law clauses restricting female coparcenary rights.",
        "overview_body_gu": "બિન-વસિયતી વારસાઈમાં લિંગભેદ દૂર કરવામાં આવ્યો છે:\n૧. મિલકતના વિતરણમાં દીકરીઓ અને દીકરાઓનો હિસ્સો એકસરખો રહેશે.\n૨. વિધવા પત્ની અને માતાને પ્રથમ વર્ગના વારસદાર તરીકે સમાન પ્રાથમિકતા.\n૩. સ્ત્રીઓના મિલકત અધિકારો પરના પરંપરાગત વ્યક્તિગત કાયદાકીય નિયંત્રણોની નાબૂદી."
    },
    {
        "slug": "wills-estates",
        "name_en": "Wills & Estates",
        "name_gu": "વિલ અને વસિયતનામું",
        "order": 4,
        "icon_name": "file",
        "summary_en": "Universal testamentary freedom allowing individuals of all faiths to bequeath self-acquired assets freely subject to dependent maintenance.",
        "summary_gu": "તમામ ધર્મના વ્યક્તિઓ માટે વસિયતનામું કરવાની મુક્ત છૂટ, આશ્રિતોના ભરણપોષણના અધિકારને આધીન.",
        "overview_body_en": "Testamentary disposition framework:\n1. Every adult person of sound mind may dispose of their property by Will.\n2. Prescribed verification and attestation procedures to prevent fraud.\n3. Mandatory protections for dependent children, parents, and spouses who cannot be entirely disinherited from reasonable sustenance.",
        "overview_body_gu": "વસિયતનામાની જોગવાઈઓ:\n૧. પુખ્ત વયની સ્વસ્થ મનની કોઈપણ વ્યક્તિ પોતાની સંપત્તિનું વિલ બનાવી શકે છે.\n૨. બનાવટી વિલ અટકાવવા માટે સાક્ષીઓની સહી અને સત્તાવાર પ્રમાણીકરણ નિયમો.\n૩. આશ્રિત બાળકો, વૃદ્ધ માતાપિતા અને પત્નીના વાજબી ભરણપોષણનું રક્ષણ."
    },
    {
        "slug": "live-in-relationships",
        "name_en": "Live-in Relationships",
        "name_gu": "લિવ-ઇન સંબંધો",
        "order": 5,
        "icon_name": "heart",
        "summary_en": "Mandatory statement of live-in relationship for adult partners, protection from exploitation, and statutory legitimacy of children.",
        "summary_gu": "પુખ્ત યુગલો માટે લિવ-ઇન સંબંધની નોંધણી નિવેદન, શોષણ સામે રક્ષણ અને જન્મેલા બાળકોને કાયદેસર દરજ્જો.",
        "overview_body_en": "Statutory framework governing cohabitation outside marriage:\n1. Partners residing in Gujarat entering into a live-in relationship must submit a statement of live-in relationship to the designated Registrar within 30 days.\n2. Prohibition where either partner is a minor or married to another living spouse.\n3. Children born out of live-in relationships are deemed legitimate under statutory law with full inheritance rights from both biological parents.\n4. Deserted female partners are entitled to claim maintenance through competent courts.",
        "overview_body_gu": "લિવ-ઇન સંબંધોનું વૈધાનિક માળખું:\n૧. ગુજરાતમાં સહજીવન શરૂ કરતા યુગલોએ ૩૦ દિવસમાં સંબંધની નોંધણી માટે રજિસ્ટ્રારને સંયુક્ત નિવેદન આપવાનું રહેશે.\n૨. જો કોઈ પક્ષકાર સગીર હોય અથવા પરણેલો હોય તો આવા સંબંધ પર પ્રતિબંધ.\n૩. આવા સંબંધથી જન્મેલા બાળકને કાયદેસર (Legitimate) માનવામાં આવશે અને પિતા-માતા બંનેની મિલકતમાં સમાન વારસાઈ અધિકાર મળશે.\n૪. સંબંધમાંથી મુક્ત કરાયેલ મહિલા અદાલત સમક્ષ ભરણપોષણ માંગી શકે છે."
    },
    {
        "slug": "maintenance-guardianship",
        "name_en": "Maintenance & Guardianship",
        "name_gu": "ભરણપોષણ અને વાલીપણું",
        "order": 6,
        "icon_name": "shield",
        "summary_en": "Universal legal duty to provide maintenance to dependent parents, spouses, and children, with paramount focus on the welfare of the child.",
        "summary_gu": "આશ્રિત માતાપિતા, પત્ની/પતિ અને સંતાનોને ભરણપોષણ પૂરું પાડવાની કાનૂની ફરજ, બાળકના શ્રેષ્ઠ હિતને સર્વોચ્ચ પ્રાથમિકતા.",
        "overview_body_en": "Maintenance and custody regulations:\n1. Unconditional statutory obligation for capable offspring to support aged or infirm parents.\n2. Child custody decisions governed strictly by the paramount welfare of the minor rather than religious dogma.\n3. Expeditious disposal of maintenance claims to avoid economic destitution.",
        "overview_body_gu": "ભરણપોષણ અને વાલીપણાના નિયમો:\n૧. વૃદ્ધ અથવા અસમર્થ માતાપિતાને સાચવવાની સંતાનોની ફરજિયાત કાનૂની જવાબદારી.\n૨. બાળકની કસ્ટડીમાં ધાર્મિક પૂર્વગ્રહોના બદલે બાળકના સર્વાંગી હિત (Welfare of Child) ને જ સર્વોચ્ચ મહત્વ.\n૩. આર્થિક મુશ્કેલી નિવારવા માટે ભરણપોષણ અરજીઓનો ઝડપી નિકાલ."
    }
]

created_topics = {}
for td in topics_data:
    t, _ = Topic.objects.get_or_create(slug=td["slug"], defaults=td)
    created_topics[td["slug"]] = t
print(f"Created {len(created_topics)} topics.")

# 4. Primary Legal Documents in Library
docs_data = [
    {
        "slug": "gujarat-ucc-bill-2026",
        "title_en": "The Gujarat Uniform Civil Code Bill, 2026 (Bill No. 17 of 2026)",
        "title_gu": "ગુજરાત સમાન નાગરિક સંહિતા વિધેયક, ૨૦૨૬ (વિધેયક ક્રમાંક ૧૭/૨૦૨૬)",
        "document_type": DocumentType.ACT,
        "issuing_authority_en": "Gujarat Legislative Assembly",
        "issuing_authority_gu": "ગુજરાત વિધાનસભા સચિવાલય",
        "document_number": "Gujarat Bill No. 17 of 2026",
        "publication_date": datetime.date(2026, 3, 12),
        "status": StatusTaxonomy.PASSED_BY_ASSEMBLY,
        "official_source_url": "https://cms.neva.gov.in/NeVA/GJ/FileStructures/PaperLaid/15/8/AsIntroduced/17%20of2026_AsIn.pdf",
        "file_checksum": "a8fbc8921e42b23a76e938f0d8a178bc902c312781bcf7120c198a287dfb6103",
        "file_size_formatted": "2.4 MB PDF",
        "relevant_sections": "Parts I through VII, Sections 1 to 142",
        "language": "both",
        "summary_en": "Complete statutory text as introduced and passed by the Gujarat Legislative Assembly, containing parts on preliminary definitions, marriage, divorce, succession, and live-in relationships.",
        "summary_gu": "ગુજરાત વિધાનસભામાં રજૂ કરાયેલ અને પસાર થયેલ મૂળ વૈધાનિક ખરડો, જેમાં પ્રારંભિક વ્યાખ્યાઓ, લગ્ન, છૂટાછેડા, વારસાઈ અને લિવ-ઇન સંબંધોની કુલ ૧૪૨ કલમો સમાવિષ્ટ છે.",
        "is_featured": True
    },
    {
        "slug": "extraordinary-gazette-oct-2026",
        "title_en": "Gujarat Extraordinary Gazette Notification Vol. LXVII No. 42 (Assented Act)",
        "title_gu": "ગુજરાત અસાધારણ ગેઝેટ જાહેરનામું વોલ્યુમ LXVII ક્રમાંક ૪૨ (મંજૂર કાયદો)",
        "document_type": DocumentType.GAZETTE,
        "issuing_authority_en": "Legal Department, Government of Gujarat",
        "issuing_authority_gu": "કાયદા વિભાગ, ગુજરાત સરકાર, ગાંધીનગર",
        "document_number": "Gujarat Act No. 17 of 2026 / Gazette Vol. LXVII",
        "publication_date": datetime.date(2026, 10, 1),
        "status": StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        "official_source_url": "https://cms.neva.gov.in/NeVA/GJ/FileStructures/PaperLaid/15/8/AsIntroduced/17%20of2026_AsIn.pdf",
        "file_checksum": "f1d48c089b33a027e1f4e1792bc4500fa88921cf8b77a0928cd998bca41315e9",
        "file_size_formatted": "3.1 MB PDF",
        "relevant_sections": "Assented Enactment; Section 1(2) Appointed Date Provision",
        "language": "both",
        "summary_en": "Official extraordinary state gazette publishing the Gujarat Uniform Civil Code Act following Presidential assent received on 17 September 2026 under Article 201. Contains the vital commencement clause specifying operational date to be appointed.",
        "summary_gu": "૧૭ સપ્ટેમ્બર ૨૦૨૬ના રોજ રાષ્ટ્રપતિની મંજૂરી બાદ ૧ ઓક્ટોબર ૨૦૨૬ના રોજ ગુજરાત સરકાર દ્વારા બહાર પાડવામાં આવેલ સત્તાવાર અસાધારણ ગેઝેટ. જેમાં કલમ ૧(૨) હેઠળ કાયદો કઈ તારીખે અમલમાં આવશે તે અલગ જાહેરનામા દ્વારા નિયત કરવાનો ઉલ્લેખ છે.",
        "is_featured": True
    },
    {
        "slug": "presidential-assent-order-sep-2026",
        "title_en": "Order of Presidential Assent under Article 201 of the Constitution",
        "title_gu": "બંધારણના અનુચ્છેદ ૨૦૧ હેઠળ રાષ્ટ્રપતિની મંજૂરીનો સત્તાવાર આદેશ",
        "document_type": DocumentType.NOTIFICATION,
        "issuing_authority_en": "Ministry of Home Affairs & Ministry of Law, Govt of India",
        "issuing_authority_gu": "ગૃહ મંત્રાલય અને કાયદા મંત્રાલય, ભારત સરકાર",
        "document_number": "MHA Order Ref: F.No. 18/UCC-GJ/2026",
        "publication_date": datetime.date(2026, 9, 17),
        "status": StatusTaxonomy.PRESIDENTIAL_ASSENT,
        "official_source_url": "https://uccgujarat.in/",
        "file_checksum": "9b12cc8f4a132eef08912781bcf7120c198a287dfb6103a8fbc8921e42b23a76",
        "file_size_formatted": "840 KB PDF",
        "relevant_sections": "Article 201, Constitution of India",
        "language": "en",
        "summary_en": "Official communication notifying assent of the President of India to the Gujarat Uniform Civil Code Bill, 2026 as reserved by the Governor under Article 200.",
        "summary_gu": "રાજ્યપાલ દ્વારા અનુચ્છેદ ૨૦૦ હેઠળ સુરક્ષિત રાખવામાં આવેલ ગુજરાત UCC ખરડા પર ભારતના રાષ્ટ્રપતિની સત્તાવાર મંજૂરી આપતો આદેશ.",
        "is_featured": False
    },
    {
        "slug": "ucc-committee-consultation-report",
        "title_en": "Report of the High-Level Expert Committee on Gujarat UCC",
        "title_gu": "ગુજરાત UCC ઉચ્ચસ્તરીય નિષ્ણાત સમિતિનો પરામર્શ અહેવાલ",
        "document_type": DocumentType.COMMITTEE,
        "issuing_authority_en": "Gujarat UCC Committee",
        "issuing_authority_gu": "ગુજરાત યુનિફોર્મ સિવિલ કોડ નિષ્ણાત સમિતિ",
        "document_number": "UCC-GJ-RPT-2026",
        "publication_date": datetime.date(2026, 2, 28),
        "status": StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        "official_source_url": "https://uccgujarat.in/",
        "file_checksum": "78a9c2114e9b882103a8fbc8921e42b23a76e938f0d8a178bc902c312781bcf7",
        "file_size_formatted": "8.5 MB PDF",
        "relevant_sections": "Chapters 1 through 9; Public Feedback Synthesis",
        "language": "both",
        "summary_en": "Comprehensive findings, public memorandums analysis, and comparative jurisprudence submitted by the Committee chaired by retired High Court Judge.",
        "summary_gu": "હાઈકોર્ટના નિવૃત્ત ન્યાયાધીશની અધ્યક્ષતા હેઠળની સમિતિ દ્વારા તૈયાર કરાયેલ વ્યાપક અહેવાલ, જેમાં લાખો નાગરિકોના મંતવ્યો અને ભલામણોનું વિશ્લેષણ છે.",
        "is_featured": False
    }
]

created_docs = {}
for dd in docs_data:
    d, _ = LegalDocument.objects.get_or_create(slug=dd["slug"], defaults=dd)
    created_docs[dd["slug"]] = d
print(f"Created {len(created_docs)} legal documents.")

# 5. Timeline Events
timeline_data = [
    {
        "event_date": datetime.date(2026, 10, 24),
        "title_en": "Verification Review of State Implementation Architecture & Subordinate Rules",
        "title_gu": "રાજ્ય અમલવારી માળખું અને પેટા-નિયમોની ચકાસણી સમીક્ષા",
        "category": TimelineCategory.RULES,
        "status_label": StatusTaxonomy.UNDER_VERIFICATION,
        "description_en": "State law department continues formulation of registration rules and online registration portal specifications. Operational commencement notification remains awaited.",
        "description_gu": "કાયદા વિભાગ દ્વારા લગ્ન અને લિવ-ઇન નોંધણીના પોર્ટલ નિયમોની તૈયારી ચાલુ છે. અમલવારી તારીખનું સત્તાવાર જાહેરનામું હજી બાકી છે.",
        "official_source_title": "Legal Department Progress Bulletin",
        "official_source_url": "https://uccgujarat.in/",
        "is_verified": True
    },
    {
        "event_date": datetime.date(2026, 10, 1),
        "title_en": "Gujarat UCC Act Published in Extraordinary Gazette",
        "title_gu": "ગુજરાત UCC કાયદો અસાધારણ ગેઝેટમાં પ્રકાશિત",
        "category": TimelineCategory.GAZETTE,
        "status_label": StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        "description_en": "The assent of the President of India having been obtained, the Gujarat Uniform Civil Code Act, 2026 is published in the Extraordinary Gazette Vol. LXVII No. 42 for general information.",
        "description_gu": "રાષ્ટ્રપતિની મંજૂરી મળ્યા બાદ ગુજરાત સમાન નાગરિક સંહિતા કાયદો અસાધારણ ગેઝેટમાં પ્રકાશિત કરવામાં આવ્યો. કલમ ૧(૨) મુજબ અમલવારી તારીખ અલગથી જાહેર કરાશે.",
        "official_source_title": "Gujarat Extraordinary Gazette",
        "official_source_url": "https://cms.neva.gov.in/NeVA/GJ/FileStructures/PaperLaid/15/8/AsIntroduced/17%20of2026_AsIn.pdf",
        "related_document": created_docs.get("extraordinary-gazette-oct-2026"),
        "is_verified": True
    },
    {
        "event_date": datetime.date(2026, 9, 17),
        "title_en": "Presidential Assent Accorded under Article 201",
        "title_gu": "અનુચ્છેદ ૨૦૧ હેઠળ રાષ્ટ્રપતિની મંજૂરી પ્રાપ્ત થઈ",
        "category": TimelineCategory.ASSENT,
        "status_label": StatusTaxonomy.PRESIDENTIAL_ASSENT,
        "description_en": "The President of India accords formal assent to the Gujarat Uniform Civil Code Bill, 2026, following review by the Union Ministry of Home Affairs and Ministry of Law.",
        "description_gu": "કેન્દ્રીય ગૃહ અને કાયદા મંત્રાલયની સમીક્ષા બાદ ભારતના રાષ્ટ્રપતિએ ગુજરાત UCC ખરડા પર પોતાની સહી કરી મંજૂરી આપી.",
        "official_source_title": "Rashtrapati Bhavan / MHA Release",
        "official_source_url": "https://uccgujarat.in/",
        "related_document": created_docs.get("presidential-assent-order-sep-2026"),
        "is_verified": True
    },
    {
        "event_date": datetime.date(2026, 3, 12),
        "title_en": "Passed by Gujarat Legislative Assembly",
        "title_gu": "ગુજરાત વિધાનસભા દ્વારા વિધેયક પસાર કરાયું",
        "category": TimelineCategory.ASSEMBLY,
        "status_label": StatusTaxonomy.PASSED_BY_ASSEMBLY,
        "description_en": "Following extensive debate, the Gujarat Legislative Assembly passes Bill No. 17 of 2026 and reserves it for the assent of the President under Article 200.",
        "description_gu": "વિધાનસભા સત્રમાં સઘન ચર્ચા બાદ બહુમતીથી UCC બિલ પસાર કરવામાં આવ્યું અને બંધારણીય જોગવાઈ અનુસાર રાષ્ટ્રપતિની મંજૂરી અર્થે મોકલાયું.",
        "official_source_title": "NeVA Legislative Assembly Record",
        "official_source_url": "https://cms.neva.gov.in/NeVA/GJ/FileStructures/PaperLaid/15/8/AsIntroduced/17%20of2026_AsIn.pdf",
        "related_document": created_docs.get("gujarat-ucc-bill-2026"),
        "is_verified": True
    },
    {
        "event_date": datetime.date(2026, 2, 28),
        "title_en": "High-Level Expert Committee Submits Final Draft",
        "title_gu": "નિષ્ણાત સમિતિએ રાજ્ય સરકારને અંતિમ ડ્રાફ્ટ સોંપ્યો",
        "category": TimelineCategory.COMMITTEE,
        "status_label": StatusTaxonomy.PROPOSED_REPORTED,
        "description_en": "The 5-member expert committee chaired by a retired High Court judge delivers its final report and statutory draft after collecting public feedback across districts.",
        "description_gu": "સમગ્ર ગુજરાતના જિલ્લાઓમાં નાગરિક પરામર્શ બાદ નિવૃત્ત ન્યાયાધીશની અધ્યક્ષતાવાળી સમિતિએ રાજ્ય સરકારને પોતાનો અહેવાલ રજૂ કર્યો.",
        "official_source_title": "Gujarat UCC Committee Portal",
        "official_source_url": "https://uccgujarat.in/",
        "related_document": created_docs.get("ucc-committee-consultation-report"),
        "is_verified": True
    }
]

for te in timeline_data:
    TimelineEvent.objects.get_or_create(
        event_date=te["event_date"],
        title_en=te["title_en"],
        defaults=te
    )
print(f"Created {len(timeline_data)} timeline events.")

# 6. Plain-Language Legal Explainers
explainers_data = [
    {
        "slug": "marriage-registration-rules-who-is-covered",
        "topic": created_topics["marriage-registration"],
        "title_en": "Compulsory Marriage Registration: Who is Covered, Timelines & Exceptions",
        "title_gu": "ફરજિયાત લગ્ન નોંધણી: કોના પર લાગુ પડે છે, સમયમર્યાદા અને અપવાદો",
        "summary_deck_en": "Under the Gujarat UCC Act, all marriages solemnized in the state must be registered within 60 days. Traditional religious ceremonies remain valid, but state registration creates conclusive legal proof of marital rights.",
        "summary_deck_gu": "ગુજરાત UCC કાયદા હેઠળ રાજ્યમાં સંપન્ન થયેલા તમામ લગ્નોની ૬૦ દિવસમાં નોંધણી કરાવવી ફરજિયાત છે. ધાર્મિક રીતરિવાજો યથાવત રહેશે, પરંતુ કાનૂની અધિકારો માટે નોંધણી અનિવાર્ય છે.",
        "what_the_text_says_en": "The statutory text mandates that every marriage solemnized in Gujarat after the commencement date must be submitted for registration before the Registrar of the local area within 60 days. Failure to register attracts a nominal periodic statutory fine but does not invalidate the marriage itself.",
        "what_the_text_says_gu": "કાયદાની મૂળ કલમો સ્પષ્ટ કરે છે કે કાયદાના અમલ બાદ ગુજરાતમાં સંપન્ન થયેલ તમામ લગ્નો સ્થાનિક રજિસ્ટ્રાર સમક્ષ ૬૦ દિવસમાં નોંધાવવા પડશે. નિયત સમયમાં નોંધણી ન કરાવવા બદલ દંડની જોગવાઈ છે, પરંતુ માત્ર નોંધણી ન હોવાને કારણે લગ્ન અમાન્ય ઠરતા નથી.",
        "who_is_covered_en": "1. All citizens domiciled in Gujarat regardless of religion or personal faith.\n2. Marriages solemnized outside Gujarat if at least one spouse is a resident of Gujarat.\n3. Existing marriages solemnized prior to the Act may be registered voluntarily or within an extended window upon notification of rules.",
        "who_is_covered_gu": "૧. ધર્મ કે સંપ્રદાયના ભેદભાવ વિના ગુજરાતમાં વસતા તમામ નાગરિકો.\n૨. ગુજરાત બહાર થયેલ લગ્ન જો દંપતીમાંથી કોઈ એક પક્ષકાર ગુજરાતનો રહેવાસી હોય.\n૩. કાયદા પૂર્વે થયેલા લગ્નો નિયમો જાહેર થયા બાદ નિર્ધારિત સમયમાં સ્વેચ્છાએ નોંધાવી શકાશે.",
        "exceptions_en": "Members of Scheduled Tribes residing in scheduled areas are explicitly exempt under Section 3. Customary rites (e.g. Saptapadi, Nikah, Anand Karaj, Church vows) are fully protected and not replaced; registration merely records the fact of marriage.",
        "exceptions_gu": "બંધારણના અનુચ્છેદ ૩૬૬(૨૫) હેઠળની અનુસૂચિત જનજાતિઓ (Scheduled Tribes) ને કલમ ૩ હેઠળ મુક્તિ આપવામાં આવી છે. સપ્તપદી, નિકાહ, આનંદ કારજ જેવી ધાર્મિક વિધિઓ યથાવત રહેશે; નોંધણી માત્ર તેનો કાયદાકીય રેકોર્ડ રાખે છે.",
        "procedural_steps_en": "Step 1: Submit joint memorandum online or in-person with proof of age (21 for bride and groom).\nStep 2: Attach confirmation of solemnization with signatures of both spouses and two witnesses.\nStep 3: Verification by local Registrar and issuance of Digital Marriage Certificate within 15 days.",
        "procedural_steps_gu": "તબક્કો ૧: વર-કન્યા બંનેના ૨૧ વર્ષ પૂર્ણ થયાના પુરાવા સાથે સંયુક્ત અરજી.\nતબક્કો ૨: લગ્ન સંપન્ન થયાની સાક્ષી આપતી બે વ્યક્તિઓની સહી સાથેનું નિવેદન.\nતબક્કો ૩: રજિસ્ટ્રાર દ્વારા ચકાસણી અને ૧૫ દિવસમાં ડિજિટલ લગ્ન પ્રમાણપત્ર જારી.",
        "misconceptions_en": "Myth: UCC replaces religious marriage ceremonies.\nFact: Religious and customary ceremonies remain fully protected under law; only post-ceremony administrative registration is compulsory.",
        "misconceptions_gu": "ગેરમાન્યતા: UCC લગ્નની ધાર્મિક વિધિઓ બદલી નાખશે.\nહકીકત: લગ્નની તમામ પરંપરાગત અને ધાર્મિક વિધિઓ યથાવત રહેશે; માત્ર વિધિ પૂર્ણ થયા બાદ સરકારી ચોપડે નોંધણી કરાવવાની રહે છે.",
        "legal_status_badge": StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        "editorial_status": EditorialStatus.PUBLISHED,
        "primary_document": created_docs.get("extraordinary-gazette-oct-2026"),
        "source_citations": "Sections 4, 5, 8 & 9, Gujarat Uniform Civil Code Act, 2026 (Act No. 17 of 2026)",
        "author_name": "Adv. M. K. Patel (Senior Legal Researcher)",
        "legal_reviewer_name": "Adv. H. S. Trivedi, High Court of Gujarat (Legal QA)",
        "last_verified_date": datetime.date(2026, 10, 24),
        "reviewed_date": datetime.date(2026, 10, 22),
        "is_featured": True
    },
    {
        "slug": "succession-inheritance-daughter-rights",
        "topic": created_topics["succession-inheritance"],
        "title_en": "Equal Inheritance for Daughters: Property Partition & Coparcenary Explained",
        "title_gu": "દીકરીઓ માટે વારસામાં સમાન અધિકાર: મિલકતની વહેંચણી અને કાનૂની જોગવાઈ",
        "summary_deck_en": "The Gujarat UCC abolishes gender discrimination in intestate succession. Daughters and sons possess identical equal shares in ancestral and paternal estates.",
        "summary_deck_gu": "ગુજરાત UCC કાયદો બિન-વસિયતી વારસાઈમાં સ્ત્રી-પુરુષ ભેદભાવ દૂર કરે છે. પિતાની સંપત્તિ અને પૈતૃક મિલકતમાં દીકરીઓ અને દીકરાઓને સમાન હિસ્સો મળે છે.",
        "what_the_text_says_en": "Under the new succession schedules, intestate property (property not disposed of by Will) devolves equally among Class-I heirs without distinction between married or unmarried daughters, sons, the surviving spouse, and the mother.",
        "what_the_text_says_gu": "નવી વારસાઈ જોગવાઈ મુજબ જો વ્યક્તિ વિલ કર્યા વિના અવસાન પામે, તો તેની સંપત્તિમાં પરણેલી કે અપરિણીત દીકરીઓ, દીકરાઓ, વિધવા પત્ની અને માતા તમામ વચ્ચે સમાન હિસ્સો થશે.",
        "who_is_covered_en": "Applies to all property partitions and inheritance openings transpiring in Gujarat post-commencement. Covers both ancestral and self-acquired immovable assets.",
        "who_is_covered_gu": "કાયદાના અમલ બાદ ગુજરાતમાં થતી તમામ મિલકત વહેંચણીઓને લાગુ પડશે. પૈતૃક અને સ્વ-અર્જિત બંને પ્રકારની સ્થાવર-જંગમ મિલકતનો સમાવેશ થાય છે.",
        "exceptions_en": "Scheduled Tribe lands subject to specific tenancy protections under regional land revenue codes remain protected. Does not alter valid registered Wills executed during lifetime.",
        "exceptions_gu": "ખેતીની જમીન અને ભાડૂઆત નિયમો હેઠળના આદિવાસી સંરક્ષણો યથાવત રહેશે. વ્યક્તિએ પોતાની હયાતીમાં કરેલ કાયદેસરના વિલ પર આ જોગવાઈ અસર કરતી નથી.",
        "procedural_steps_en": "1. Obtain statutory succession certificate or legal heir declaration from competent civil court or revenue authority.\n2. Submit equal mutation entry application before local revenue/talati registrar.",
        "procedural_steps_gu": "૧. સક્ષમ સિવિલ કોર્ટ અથવા મહેસૂલ અધિકારી પાસેથી વારસાઈ પ્રમાણપત્ર મેળવવું.\n૨. સ્થાનિક તલાટી/મામલતદાર સમક્ષ તમામ વારસદારોના નામે સમાન વહેંચણીની કાચી-પાકી નોંધ કરાવવી.",
        "misconceptions_en": "Myth: Married daughters cannot claim a share in father's self-acquired property.\nFact: UCC provides that marital status does not diminish a daughter's statutory inheritance rights.",
        "misconceptions_gu": "ગેરમાન્યતા: પરણેલી દીકરીઓ પિતાની સંપત્તિમાં હક માંગી શકતી નથી.\nહકીકત: UCC કાયદા હેઠળ દીકરી પરણેલી હોય કે અપરિણીત, તેનો વારસાઈ હક દીકરા જેટલો જ સમાન રહે છે.",
        "legal_status_badge": StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        "editorial_status": EditorialStatus.PUBLISHED,
        "primary_document": created_docs.get("extraordinary-gazette-oct-2026"),
        "source_citations": "Sections 48 through 62, Schedule II, Gujarat UCC Act, 2026",
        "author_name": "Adv. S. R. Desai",
        "legal_reviewer_name": "Adv. H. S. Trivedi, High Court of Gujarat (Legal QA)",
        "last_verified_date": datetime.date(2026, 10, 24),
        "reviewed_date": datetime.date(2026, 10, 21),
        "is_featured": True
    },
    {
        "slug": "live-in-relationship-declaration-law",
        "topic": created_topics["live-in-relationships"],
        "title_en": "Live-in Relationships: Statement of Relationship, Penalties & Rights of Children",
        "title_gu": "લિવ-ઇન સંબંધો: નોંધણી નિવેદન, નિયમો અને બાળકોના કાનૂની અધિકારો",
        "summary_deck_en": "Explaining the mandatory statement of live-in relationship requirement under the Gujarat UCC, criminal thresholds, and constitutional privacy safeguards.",
        "summary_deck_gu": "ગુજરાત UCC હેઠળ લિવ-ઇન સંબંધના નિવેદનની જોગવાઈ, તેની સમયમર્યાદા, પ્રતિબંધિત બાબતો અને જન્મેલા બાળકોના કાયદેસર અધિકારોની સમજૂતી.",
        "what_the_text_says_en": "Adult partners cohabiting in a nature of marriage must submit a declaration to the Registrar. The Registrar verifies that neither partner is married, neither partner is a minor, and mutual free consent exists. Children born of such relationships enjoy full legal legitimacy.",
        "what_the_text_says_gu": "લગ્ન જેવી વ્યવસ્થામાં સાથે રહેતા પુખ્ત વયના પક્ષકારોએ રજિસ્ટ્રાર સમક્ષ નિવેદન આપવાનું રહેશે. રજિસ્ટ્રાર ચકાસશે કે કોઈ પક્ષકાર પરણેલો કે સગીર નથી. આવા સંબંધથી જન્મેલા સંતાનને કાયદેસર સંતાન તરીકે તમામ અધિકારો મળશે.",
        "who_is_covered_en": "Partners who are both residents of Gujarat or residing together within the territorial jurisdiction of the State of Gujarat.",
        "who_is_covered_gu": "ગુજરાતના રહેવાસી હોય અથવા રાજ્યની હદમાં સહજીવન વિતાવતા પુખ્ત યુગલો.",
        "exceptions_en": "Relationships where one partner is under 18 years of age or within prohibited degrees of consanguinity are void and punishable.",
        "exceptions_gu": "જો કોઈ પક્ષકાર ૧૮ વર્ષથી ઓછી ઉંમરનો હોય અથવા પ્રતિબંધિત કૌટુંબિક સંબંધો (Prohibited Degrees) માં આવતો હોય તો આવા સંબંધ ગેરકાયદે રહેશે.",
        "procedural_steps_en": "Submission of joint statement -> Summary verification by Registrar within 30 days -> Entry into confidential registry.",
        "procedural_steps_gu": "સંયુક્ત નિવેદન સબમિટ કરવું -> ૩૦ દિવસમાં રજિસ્ટ્રાર દ્વારા ગોપનીય ચકાસણી -> રજિસ્ટરમાં નોંધ.",
        "misconceptions_en": "Myth: Live-in relationships are declared illegal.\nFact: Consensual adult live-in relationships are legal; the statute requires administrative registration for social security and to prevent exploitation.",
        "misconceptions_gu": "ગેરમાન્યતા: લિવ-ઇન સંબંધો ગેરકાયદેસર જાહેર કરવામાં આવ્યા છે.\nહકીકત: પુખ્ત વયના યુગલો માટે સહજીવન કાયદેસર છે; માત્ર મહિલાઓ અને બાળકોની સુરક્ષા માટે સરકારી નોંધણીની વ્યવસ્થા કરવામાં આવી છે.",
        "legal_status_badge": StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        "editorial_status": EditorialStatus.PUBLISHED,
        "primary_document": created_docs.get("extraordinary-gazette-oct-2026"),
        "source_citations": "Sections 124 to 134, Gujarat Uniform Civil Code Act, 2026",
        "author_name": "Adv. R. K. Joshi",
        "legal_reviewer_name": "Adv. H. S. Trivedi, High Court of Gujarat (Legal QA)",
        "last_verified_date": datetime.date(2026, 10, 24),
        "reviewed_date": datetime.date(2026, 10, 20),
        "is_featured": True
    }
]

for ed in explainers_data:
    Explainer.objects.get_or_create(slug=ed["slug"], defaults=ed)
print(f"Created {len(explainers_data)} plain-language explainers.")

# 7. Editorial News & Fact Checks
news_data = [
    {
        "slug": "gazette-published-why-act-is-not-yet-in-force",
        "headline_en": "Extraordinary Gazette Published: Why the Gujarat UCC Act is Not Yet Operative",
        "headline_gu": "અસાધારણ ગેઝેટ પ્રકાશિત: ગુજરાત UCC કાયદો હજી કેમ અમલમાં આવ્યો નથી?",
        "category": NewsCategory.OFFICIAL_UPDATE,
        "fact_check_status": FactCheckStatus.OFFICIAL_CONFIRMED,
        "is_breaking": True,
        "published_date": datetime.datetime(2026, 10, 2, 11, 0),
        "author_name": "Legal Affairs Correspondent",
        "reviewer_name": "Senior Editorial Board",
        "excerpt_en": "While Presidential Assent was gazetted on 1 October 2026, Section 1(2) specifies that the Act will come into force only on a date appointed by the State Government via separate Gazette notification.",
        "excerpt_gu": "૧ ઓક્ટોબર ૨૦૨૬ના રોજ કાયદો ગેઝેટમાં પ્રકાશિત થયો હોવા છતાં, કલમ ૧(૨) ની શરત અનુસાર રાજ્ય સરકાર દ્વારા અલગથી અમલવારી જાહેરનામું બહાર પાડવામાં ન આવે ત્યાં સુધી કાયદો અમલી ગણાશે નહીં.",
        "body_en": "Following the Presidential assent accorded on 17 September 2026, the Government of Gujarat officially published Act No. 17 of 2026 in the Extraordinary Gazette dated 1 October 2026.\n\nHowever, a common misconception currently circulating in media reports suggests that the law has immediately taken effect across the state. This is legally incorrect.\n\nUnder Section 1, Sub-section (2) of the enacted Act:\n'It shall come into force on such date as the State Government may, by notification in the Official Gazette, appoint.'\n\nUntil the State Government issues this specific commencement notification, existing civil statutes and personal laws continue in full operation. Government officials confirm that subordinate rules, registration portals, and appellate authorities are being prepared before notifying the operational appointed date.",
        "body_gu": "૧૭ સપ્ટેમ્બર ૨૦૨૬ના રોજ રાષ્ટ્રપતિની મંજૂરી બાદ ગુજરાત સરકારે ૧ ઓક્ટોબર ૨૦૨૬ના અસાધારણ ગેઝેટમાં કાયદો પ્રકાશિત કર્યો છે.\n\nજોકે, સોશિયલ મીડિયા અને કેટલાક મીડિયા અહેવાલોમાં એવી ગેરસમજ ફેલાઈ રહી છે કે કાયદો તુરંત અમલમાં આવી ગયો છે. આ બાબત કાનૂની રીતે સદંતર ખોટી છે.\n\nઅધિનિયમની કલમ ૧ પેટા-કલમ (૨) માં સ્પષ્ટ શબ્દોમાં જણાવાયું છે:\n'રાજ્ય સરકાર સત્તાવાર ગેઝેટમાં જાહેરનામા દ્વારા જે તારીખ નિયત કરે તે તારીખથી આ કાયદો અમલમાં આવશે.'\n\nજ્યાં સુધી રાજ્ય સરકાર આ અમલવારી જાહેરનામું બહાર ન પાડે ત્યાં સુધી જૂના કાયદાઓ જ અમલમાં રહેશે. નિયમો ઘડાયા બાદ જ સત્તાવાર તારીખ જાહેર કરવામાં આવશે.",
        "sources_list": "1. Gujarat Extraordinary Gazette Vol. LXVII No. 42 (1 Oct 2026)\n2. Section 1(2), Gujarat Act 17 of 2026\n3. Press Briefing, Legal Department, Government of Gujarat"
    },
    {
        "slug": "fact-check-scheduled-tribes-exemption",
        "headline_en": "Fact Check: Does the Gujarat UCC Apply to Scheduled Tribes?",
        "headline_gu": "ફેક્ટ ચેક: શું ગુજરાત UCC અનુસૂચિત જનજાતિઓ (આદિવાસી સમાજ) પર લાગુ પડે છે?",
        "category": NewsCategory.FACT_CHECK,
        "fact_check_status": FactCheckStatus.OFFICIAL_CONFIRMED,
        "is_breaking": False,
        "published_date": datetime.datetime(2026, 10, 10, 15, 30),
        "author_name": "Fact Check Desk",
        "reviewer_name": "Adv. H. S. Trivedi",
        "excerpt_en": "False rumors claiming tribal customs are superseded by UCC are contrary to statutory text. Section 3 of Gujarat Act 17 of 2026 provides absolute statutory exemption for Scheduled Tribes.",
        "excerpt_gu": "UCC થી આદિવાસી પરંપરાઓ નાબૂદ થશે તેવી અફવાઓ કાયદાકીય રીતે ખોટી છે. કાયદાની કલમ ૩ હેઠળ અનુસૂચિત જનજાતિઓને સંપૂર્ણ વૈધાનિક મુક્તિ આપવામાં આવી છે.",
        "body_en": "Claim: Viral messages claim that tribal customary marriage rites and indigenous succession practices will become void once Gujarat UCC takes effect.\n\nStatutory Fact: False.\n\nSection 3 of the Gujarat Uniform Civil Code Act, 2026 explicitly creates a non-derogable exclusion:\n'Nothing contained in this Act shall apply to the members of any Scheduled Tribes within the meaning of clause (25) of Article 366 of the Constitution of India.'\n\nConsequently, the customary laws, community councils, and ancestral inheritance systems of tribal populations across Gujarat remain entirely untouched by this legislation.",
        "body_gu": "દાવો: સોશિયલ મીડિયા પર એવો દાવો કરવામાં આવી રહ્યો છે કે UCC લાગુ થવાથી આદિવાસી સમાજના રીતરિવાજો અને પરંપરાગત વારસાઈ વ્યવસ્થા રદ થઈ જશે.\n\nકાનૂની સત્ય: આ દાવો સંપૂર્ણ અસત્ય છે.\n\nગુજરાત UCC કાયદાની કલમ ૩ માં સ્પષ્ટ મુક્તિ આપવામાં આવી છે:\n'ભારતના બંધારણના અનુચ્છેદ ૩૬૬ ના ખંડ (૨૫) ના અર્થમાં આવતી કોઈપણ અનુસૂચિત જનજાતિના સભ્યોને આ કાયદાની કોઈપણ બાબત લાગુ પડશે નહીં.'\n\nઆથી આદિવાસી સમાજના તમામ પરંપરાગત અધિકારો અને કાયદાઓ સંપૂર્ણ સુરક્ષિત છે.",
        "sources_list": "1. Section 3, Gujarat Uniform Civil Code Act, 2026\n2. Article 366(25), Constitution of India\n3. Official Clarification, Department of Tribal Development, Gujarat"
    }
]

for nd in news_data:
    NewsArticle.objects.get_or_create(slug=nd["slug"], defaults=nd)
print(f"Created {len(news_data)} news articles.")

# 8. FAQs & Glossary Terms
faqs_data = [
    {
        "question_en": "Is the Gujarat UCC Act currently in force in October 2026?",
        "question_gu": "શું ઓક્ટોબર ૨૦૨૬માં ગુજરાત UCC કાયદો અમલમાં છે?",
        "short_answer_en": "No. The Act has received Presidential Assent and appeared in the Gazette, but the commencement notification is awaited.",
        "short_answer_gu": "ના. કાયદાને રાષ્ટ્રપતિની મંજૂરી મળી ગઈ છે અને ગેઝેટમાં પ્રકાશિત થયો છે, પરંતુ અમલવારી માટેનું સરકારી જાહેરનામું હજુ બાકી છે.",
        "detailed_answer_en": "Under Section 1(2) of the Act, provisions become operational only on an appointed date notified by the State Government. Until that notification appears, pre-existing marriage and personal laws remain legally binding.",
        "detailed_answer_gu": "કાયદાની કલમ ૧(૨) સ્પષ્ટ કરે છે કે કાયદો રાજ્ય સરકાર દ્વારા નિયત તારીખે જ અમલમાં આવશે. તેથી હાલ જૂના કાયદા જ લાગુ છે.",
        "citations": "Section 1(2), Gujarat Act 17 of 2026",
        "is_featured": True,
        "order": 1
    },
    {
        "question_en": "Will existing marriages solemnized before UCC need to be re-registered?",
        "question_gu": "શું UCC પૂર્વે થયેલા જૂના લગ્નો ફરીથી નોંધાવવા પડશે?",
        "short_answer_en": "No re-registration of legally recognized existing marriages is required.",
        "short_answer_gu": "ના, કાયદેસર રીતે થયેલા જૂના લગ્નોની ફરીથી નોંધણી કરાવવી ફરજિયાત નથી.",
        "detailed_answer_en": "Marriages already registered under previous Acts (e.g. Special Marriage Act, Gujarat Registration of Marriages Act) remain fully recognized. The Act primarily governs new solemnizations post-commencement.",
        "detailed_answer_gu": "અગાઉ નોંધાયેલા લગ્નો કાયદેસર માન્ય રહેશે. આ કાયદો મુખ્યત્વે કાયદો અમલમાં આવ્યા પછી થનારા નવા લગ્નોને લાગુ પડશે.",
        "citations": "Section 8, Savings Clause, Gujarat Act 17 of 2026",
        "is_featured": True,
        "order": 2
    },
    {
        "question_en": "Can daughters be excluded from ancestral property through a Will?",
        "question_gu": "શું વસિયતનામા (વિલ) દ્વારા દીકરીને પૂર્વજોની મિલકતમાંથી બાકાત રાખી શકાય?",
        "short_answer_en": "Self-acquired property may be bequeathed by Will, but dependent maintenance protections apply.",
        "short_answer_gu": "સ્વ-અર્જિત મિલકતનું વિલ થઈ શકે છે, પરંતુ આશ્રિતોના ભરણપોષણની સુરક્ષા કાયદા હેઠળ રહે છે.",
        "detailed_answer_en": "An owner has testamentary freedom over self-acquired property, but if a person dies intestate (without a Will), daughters hold an unbreakable statutory equal share alongside sons.",
        "detailed_answer_gu": "જો કોઈ વ્યક્તિ વિલ કર્યા વિના અવસાન પામે તો દીકરીનો હિસ્સો કોઈ છીનવી શકતું નથી. સ્વ-અર્જિત મિલકતમાં વ્યક્તિ વિલ કરી શકે છે.",
        "citations": "Sections 48 & 72, Gujarat Act 17 of 2026",
        "is_featured": True,
        "order": 3
    }
]

for fd in faqs_data:
    FAQ.objects.get_or_create(question_en=fd["question_en"], defaults=fd)
print(f"Created {len(faqs_data)} FAQs.")

glossary_data = [
    {
        "term_en": "Uniform Civil Code (UCC)",
        "term_gu": "સમાન નાગરિક સંહિતા",
        "plain_language_definition_en": "A single set of secular laws governing family matters—marriage, divorce, inheritance, and maintenance—applicable to all citizens irrespective of religion.",
        "plain_language_definition_gu": "ધર્મ કે જાતિના ભેદભાવ વિના તમામ નાગરિકો માટે લગ્ન, છૂટાછેડા, વારસાઈ અને ભરણપોષણ જેવા અંગત નાગરિક અધિકારોનું એકસમાન કાયદાકીય માળખું.",
        "statutory_source": "Article 44, Constitution of India",
        "order": 1
    },
    {
        "term_en": "Extraordinary Gazette",
        "term_gu": "અસાધારણ ગેઝેટ",
        "plain_language_definition_en": "An official government publication used to promulgate urgent statutory enactments, presidential assents, and major public orders.",
        "plain_language_definition_gu": "સરકાર દ્વારા તાકીદના કાયદાઓ, રાષ્ટ્રપતિ મંજૂરી અને કાનૂની જાહેરનામાઓ પ્રસિદ્ધ કરવા માટે બહાર પાડવામાં આવતું સત્તાવાર ગેઝેટ.",
        "statutory_source": "General Clauses Act",
        "order": 2
    },
    {
        "term_en": "Intestate Succession",
        "term_gu": "બિન-વસિયતી વારસાઈ",
        "plain_language_definition_en": "The legal distribution of property belonging to a deceased person who did not leave a valid Will.",
        "plain_language_definition_gu": "જ્યારે કોઈ વ્યક્તિ કાયદેસરનું વિલ (વસિયતનામું) કર્યા વિના અવસાન પામે ત્યારે કાયદાની જોગવાઈ મુજબ તેની સંપત્તિની સગા-સંબંધીઓ વચ્ચે થતી વહેંચણી.",
        "statutory_source": "Part IV, Gujarat Act 17 of 2026",
        "order": 3
    },
    {
        "term_en": "Commencement Notification",
        "term_gu": "અમલવારી જાહેરનામું",
        "plain_language_definition_en": "A formal notification issued in the government gazette by the executive government specifying the precise calendar date on which an assented Act becomes operative.",
        "plain_language_definition_gu": "સરકાર દ્વારા ગેઝેટમાં બહાર પાડવામાં આવતું જાહેરનામું જે નિર્ધારિત કરે છે કે કાયદો કઈ ચોક્કસ તારીખથી રાજ્યમાં અમલમાં આવશે.",
        "statutory_source": "Section 1(2), Gujarat Act 17 of 2026",
        "order": 4
    }
]

for gd in glossary_data:
    GlossaryTerm.objects.get_or_create(term_en=gd["term_en"], defaults=gd)
print(f"Created {len(glossary_data)} glossary terms.")

print("All Gujarat UCC platform seed data populated successfully!")
