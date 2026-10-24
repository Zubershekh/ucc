from django import template
from apps.core.models import StatusTaxonomy

register = template.Library()

@register.filter(name='localize_attr')
def localize_attr(obj, attr_name):
    """
    Returns obj.<attr_name>_gu if current context is Gujarati,
    otherwise obj.<attr_name>_en, with clean fallback.
    """
    if not obj:
        return ""
    # We will get language from the object or let template pass context
    # Usually accessed via helper tag below
    return getattr(obj, f"{attr_name}_en", getattr(obj, attr_name, ""))


@register.simple_tag(takes_context=True)
def get_bilingual(context, obj, attr_name, truncate_words=None):
    """
    Usage: {% get_bilingual obj 'title' %} or {% get_bilingual obj 'summary' 20 %}
    Respects context['current_lang'] and truncates if requested.
    """
    if not obj:
        return ""
    lang = context.get('current_lang', 'gu')
    target_attr = f"{attr_name}_{lang}"
    val = getattr(obj, target_attr, None)
    if not val:
        fallback_attr = f"{attr_name}_en" if lang == 'gu' else f"{attr_name}_gu"
        val = getattr(obj, fallback_attr, getattr(obj, attr_name, ""))
    
    if truncate_words and isinstance(val, str):
        try:
            limit = int(truncate_words)
            words = val.split()
            if len(words) > limit:
                return " ".join(words[:limit]) + "..."
        except (ValueError, TypeError):
            pass
    return val


@register.simple_tag(takes_context=True)
def get_status_label(context, status_code):
    """
    Returns translated status label according to current language.
    Usage: {% get_status_label doc.status %}
    """
    lang = context.get('current_lang', 'gu')
    if lang == 'gu':
        return StatusTaxonomy.LABELS_GU.get(status_code, status_code)
    return StatusTaxonomy.LABELS_EN.get(status_code, status_code)


@register.filter(name='status_badge_class')
def status_badge_class_filter(status_code):
    return StatusTaxonomy.BADGE_CLASSES.get(status_code, 'status-badge-neutral')


@register.simple_tag(name='status_badge_class')
def status_badge_class_tag(status_code):
    return StatusTaxonomy.BADGE_CLASSES.get(status_code, 'status-badge-neutral')
