def mobile_detection(request):
    """
    Detect if request is coming from a mobile device and add to context
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    # Simple mobile detection
    is_mobile = any([
        'mobile' in user_agent,
        'android' in user_agent,
        'iphone' in user_agent,
        'ipad' in user_agent,
    ])
    
    return {
        'is_mobile': is_mobile,
    }
