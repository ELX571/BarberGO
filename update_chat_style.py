import re

with open('Templates/chat.html', 'r') as f:
    content = f.read()

new_styles = """
.chat-app { display: flex; height: calc(100vh - 120px); background: #fff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.08); margin: 20px; border: 1px solid #f1f5f9; }
.chat-list-panel { width: 340px; border-right: 1px solid #f1f5f9; background: #f8fafc; display: flex; flex-direction: column; overflow-y: auto; }
.chat-search { padding: 20px; border-bottom: 1px solid #f1f5f9; background: #f8fafc; }
.chat-search input { width: 100%; padding: 12px 18px; border-radius: 12px; border: 1px solid #e2e8f0; outline: none; font-family: var(--font-family); background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: 0.2s; }
.chat-search input:focus { border-color: #f97316; box-shadow: 0 0 0 3px rgba(249,115,22,0.1); }

.room-item { display: flex; gap: 14px; padding: 16px 20px; cursor: pointer; border-left: 4px solid transparent; transition: all 0.2s ease; border-bottom: 1px solid #f1f5f9; }
.room-item:hover { background: #f1f5f9; }
.room-item.active { background: #fff7ed; border-left-color: #f97316; }

.avatar-circle { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #f97316, #fb923c); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; flex-shrink: 0; box-shadow: 0 4px 10px rgba(249,115,22,0.2); }
.room-item-body { flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; }
.room-item-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.room-item-name { font-weight: 700; font-size: 15px; color: #0f172a; }
.room-item-time { font-size: 12px; color: #64748b; font-weight: 500; }
.room-item-bottom { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.room-item-last { font-size: 14px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.room-item-badge { background: #f97316; color: #fff; font-size: 12px; font-weight: 700; border-radius: 50%; min-width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; padding: 0 6px; flex-shrink: 0; }

.chat-active-panel { flex: 1; display: flex; flex-direction: column; background: #ffffff; }
.chat-placeholder { flex: 1; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 18px; font-weight: 500; background: #f8fafc; }

.chat-active-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 24px; border-bottom: 1px solid #f1f5f9; background: #fff; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); z-index: 10; }
.chat-active-who { display: flex; align-items: center; gap: 14px; }
.chat-active-name { font-weight: 700; font-size: 17px; color: #0f172a; }
.chat-active-status { font-size: 13px; color: #10b981; font-weight: 500; margin-top: 2px; }

.chat-menu-btn { background: none; border: none; font-size: 24px; cursor: pointer; color: #94a3b8; transition: 0.2s; }
.chat-menu-btn:hover { color: #f97316; }

.chat-messages { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 12px; background: #f8fafc; }
.msg { max-width: 65%; padding: 12px 16px; font-size: 15px; line-height: 1.5; position: relative; box-shadow: 0 2px 4px rgba(0,0,0,0.04); }
.msg.mine { align-self: flex-end; background: linear-gradient(135deg, #f97316, #fb923c); color: #fff; border-radius: 16px 16px 4px 16px; }
.msg.theirs { align-self: flex-start; background: #fff; color: #0f172a; border: 1px solid #f1f5f9; border-radius: 16px 16px 16px 4px; }
.msg small { display: block; opacity: 0.7; font-size: 11px; margin-top: 6px; text-align: right; font-weight: 500; }
.msg.theirs small { text-align: left; color: #94a3b8; }
.msg img { max-width: 100%; border-radius: 8px; margin-top: 5px; }
.msg video { max-width: 100%; border-radius: 8px; margin-top: 5px; }
.msg audio { max-width: 100%; margin-top: 5px; }

.chat-input-row { display: flex; align-items: center; gap: 12px; padding: 16px 24px; border-top: 1px solid #f1f5f9; background: #fff; }
.chat-icon-btn { width: 40px; height: 40px; border-radius: 50%; background: #f1f5f9; border: none; font-size: 18px; cursor: pointer; color: #64748b; transition: 0.2s; display: flex; align-items: center; justify-content: center; }
.chat-icon-btn:hover { background: #e2e8f0; color: #f97316; }
.chat-icon-btn.recording { color: #ef4444; animation: pulse 1s infinite; background: #fee2e2; }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.2); } 100% { transform: scale(1); } }

#chatInput { flex: 1; padding: 14px 20px; border-radius: 24px; border: 1px solid #e2e8f0; outline: none; font-family: var(--font-family); background: #f8fafc; font-size: 15px; transition: 0.2s; }
#chatInput:focus { border-color: #f97316; background: #fff; box-shadow: 0 0 0 3px rgba(249,115,22,0.1); }
.chat-send-btn { width: 46px; height: 46px; border-radius: 50%; background: #f97316; color: #fff; border: none; cursor: pointer; font-size: 18px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: 0.2s; box-shadow: 0 4px 10px rgba(249,115,22,0.3); }
.chat-send-btn:hover { background: #ea580c; transform: scale(1.05); }
"""

# Replace the style block
content = re.sub(r'<style>.*?</style>', f'<style>\n{new_styles}</style>', content, flags=re.DOTALL)

with open('Templates/chat.html', 'w') as f:
    f.write(content)

