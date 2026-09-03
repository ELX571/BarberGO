with open("notifications/consumer.py", "r") as f:
    text = f.read()

text = text.replace(
    "await self.channel_layer.group_discard(self.group_name, self.channel_name)",
    "if hasattr(self, 'group_name'):\n            await self.channel_layer.group_discard(self.group_name, self.channel_name)"
)
with open("notifications/consumer.py", "w") as f:
    f.write(text)
