def ensure_trailing_slash(target_url):
    if not target_url.endswith('/'):
        target_url += '/'
    return target_url

def checkbox_checked(selected_attacks, attack_name):
    return attack_name in selected_attacks
