import re

with open('Templates/hairstyles.html', 'r') as f:
    content = f.read()

# Find the start of the grid
start_tag = '<div class="hairstyles-grid">'
end_tag = '    </div>\n</div>\n{% endblock %}'

start_idx = content.find(start_tag)
end_idx = content.find(end_tag) + len('    </div>')

if start_idx != -1 and end_idx != -1:
    new_grid = """<div class="hairstyles-grid">
        {% for style in hairstyles %}
        <div class="hairstyle-card" data-category="all" data-aos="zoom-in" data-aos-delay="{{ forloop.counter0|add:'1' }}00">
            <div class="hairstyle-img-wrapper" style="height: 250px; overflow: hidden;">
                {% if style.image %}
                    <img src="{{ style.image.url }}" alt="{{ style.name }}" style="width: 100%; height: 100%; object-fit: cover;">
                {% elif style.image_url %}
                    <img src="{{ style.image_url }}" alt="{{ style.name }}" style="width: 100%; height: 100%; object-fit: cover;">
                {% else %}
                    <div class="hairstyle-img-placeholder" style="height: 100%;">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><line x1="20" y1="4" x2="8.12" y2="15.88"></line><line x1="14.47" y1="14.48" x2="20" y2="20"></line><line x1="8.12" y1="8.12" x2="12" y2="12"></line></svg>
                    </div>
                {% endif %}
            </div>
            <div class="hairstyle-info">
                <h3>{{ style.name }}</h3>
                <p>{{ style.description|truncatechars:100 }}</p>
                <div class="hairstyle-footer">
                    <div class="hairstyle-popularity">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                        <span>Yuz: {{ style.target_face_shapes }}</span>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div style="text-align: center; grid-column: 1 / -1; padding: 40px; color: #888;">
            <p>Hozircha hech qanday soch turmagi qo'shilmagan.</p>
        </div>
        {% endfor %}
    </div>"""
    
    new_content = content[:start_idx] + new_grid + content[end_idx:]
    with open('Templates/hairstyles.html', 'w') as f:
        f.write(new_content)
    print("Muvaffaqiyatli almashtirildi!")
else:
    print("Teglar topilmadi")
