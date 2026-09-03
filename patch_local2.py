with open("orders/views.py", "r") as f:
    text = f.read()

text = text.replace(
    "action_text = 'accept qildi' if new_status == Order.Status.ACCEPTED else 'cancel qildi'\n        message = f'{barber_name} sizning orderingizni {action_text}'",
    "action_text = 'qabul qildi' if new_status == Order.Status.ACCEPTED else 'bekor qildi'\n        message = f'Sartarosh {barber_name} sizning brongizni {action_text}.'"
)

with open("orders/views.py", "w") as f:
    f.write(text)
