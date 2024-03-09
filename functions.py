def ensure_trailing_slash(target_url):
    if not target_url.endswith('/'):
        target_url += '/'
    return target_url

def ensure_start_http(target_url):
    if not target_url.startswith('http://') and not target_url.startswith('https://'):
        target_url = 'http://' + target_url
    return target_url

def checkbox_checked(selected_attacks, attack_name):
    return attack_name in selected_attacks
