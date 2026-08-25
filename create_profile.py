import re

with open('/home/ismoilow/Desktop/easy_build/templates/build/profile.html', 'r', encoding='utf-8') as f:
    easy_html = f.read()

# Extract profile-container
match = re.search(r'(<div class="profile-container">.*?)<!-- INSTAGRAM-STYLE MINIMALIST MOBILE BOTTOM NAVIGATION -->', easy_html, re.DOTALL)
if match:
    profile_content = match.group(1)
    
    # Clean up easy_build specific tags (replace django url tags)
    profile_content = re.sub(r'\{% url \'build:[^\']+\' [^\%]+\%\}', '#', profile_content)
    profile_content = re.sub(r'\{% url \'build:[^\']+\' \%\}', '#', profile_content)
    profile_content = re.sub(r'\{% translate "[^"]+" %\}', lambda m: m.group(0).replace('translate', 'trans'), profile_content)
    
    # We will build the new template for BarberGo
    new_template = f"""{{% extends 'base.html' %}}
{{% load static %}}

{{% block extra_js %}}
<link rel="stylesheet" href="{{% static 'css/profile.css' %}}?v=1">
{{% endblock %}}

{{% block content %}}
{profile_content}
{{% endblock %}}
"""
    with open('/home/ismoilow/Desktop/my project/BarberGo/Templates/profile.html', 'w', encoding='utf-8') as f:
        f.write(new_template)
    print("Created profile.html")
else:
    print("Could not extract profile-container")
