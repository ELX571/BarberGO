/* ===== AI Chat Widget - BarberGo (Real AI Version) ===== */
(function() {
    'use strict';

    let chatOpen = false;
    let cameraStream = null;

    // DOM references
    let fab, chatWindow, messagesContainer, textInput, fileInput;

    // Inject HTML
    function injectWidget() {
        const widgetHTML = `
        <!-- Floating Action Button -->
        <button class="ai-chat-fab" id="aiChatFab" title="AI Soch Maslahatchi">
            <span class="fab-badge">AI</span>
            <span class="fab-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="6" cy="6" r="3"></circle>
                    <circle cx="6" cy="18" r="3"></circle>
                    <line x1="20" y1="4" x2="8.12" y2="15.88"></line>
                    <line x1="14.47" y1="14.48" x2="20" y2="20"></line>
                    <line x1="8.12" y1="8.12" x2="12" y2="12"></line>
                </svg>
            </span>
        </button>

        <!-- Chat Window -->
        <div class="ai-chat-window" id="aiChatWindow" style="display:none;">
            <!-- Camera Modal -->
            <div class="ai-lightbox" id="aiLightbox" onclick="this.classList.remove('open')">
                <img id="aiLightboxImg" src="" onclick="event.stopPropagation()">
            </div>
            
            <div class="ai-camera-modal" id="aiCameraModal">
                <video id="aiCameraVideo" autoplay playsinline></video>
                <canvas id="aiCameraCanvas"></canvas>
                <div class="ai-camera-controls">
                    <button class="ai-camera-close-btn" onclick="window.aiChat.closeCamera()">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </button>
                    <button class="ai-camera-snap-btn" onclick="window.aiChat.takeSnapshot()">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
                    </button>
                </div>
            </div>

            <!-- Header -->
            <div class="ai-chat-header">
                <div class="ai-chat-header-avatar">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><line x1="20" y1="4" x2="8.12" y2="15.88"></line><line x1="14.47" y1="14.48" x2="20" y2="20"></line><line x1="8.12" y1="8.12" x2="12" y2="12"></line></svg>
                </div>
                <div class="ai-chat-header-info">
                    <h4>AI Soch Maslahatchi</h4>
                    <span>✨ Gemini AI bilan ishlaydi</span>
                </div>
                <div class="ai-chat-header-actions">
                    <button class="ai-chat-header-btn" onclick="window.aiChat.toggleFullscreen()" title="To'liq ekran">
                        <svg id="aiFullscreenIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
                        </svg>
                    </button>
                    <button class="ai-chat-header-btn" onclick="window.aiChat.toggle()" title="Yopish">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </button>
                </div>
            </div>

            <!-- Messages -->
            <div class="ai-chat-messages" id="aiChatMessages">
                <div class="ai-msg bot">
                    Assalomu alaykum! 👋 Men <strong>BarberGo AI Soch Maslahatchi</strong>man.<br><br>
                    🤖 Men <strong>Gemini AI</strong> asosida ishlayman va yuzingizni haqiqiy tahlil qila olaman!<br><br>
                    📷 <strong>Kamerani yoqing</strong> yoki 🖼 <strong>Rasm yuboring</strong> — men yuzingiz shakliga mos soch turmagini topaman! ✂️
                </div>
            </div>

            <!-- Input area -->
            <div class="ai-chat-input-area">
                <button class="ai-chat-action-btn camera-btn" onclick="window.aiChat.openCamera()" title="Kamerani yoqish">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
                </button>
                <button class="ai-chat-action-btn photo-btn" onclick="document.getElementById('aiFileInput').click()" title="Rasm yuklash">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                </button>
                <input type="file" id="aiFileInput" accept="image/*" onchange="window.aiChat.handleFile(event)">
                <input type="text" id="aiChatTextInput" placeholder="Xabar yozing..." onkeydown="if(event.key==='Enter') window.aiChat.sendText()">
                <button class="ai-chat-action-btn send-btn" onclick="window.aiChat.sendText()" title="Yuborish">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
                </button>
            </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', widgetHTML);

        fab = document.getElementById('aiChatFab');
        chatWindow = document.getElementById('aiChatWindow');
        messagesContainer = document.getElementById('aiChatMessages');
        textInput = document.getElementById('aiChatTextInput');
        fileInput = document.getElementById('aiFileInput');

        fab.addEventListener('click', () => window.aiChat.toggle());
    }

    // Toggle chat
    function toggleChat() {
        chatOpen = !chatOpen;
        if (chatOpen) {
            chatWindow.style.display = 'flex';
            requestAnimationFrame(() => {
                chatWindow.classList.add('open');
            });
            textInput.focus();
        } else {
            chatWindow.classList.remove('open');
            setTimeout(() => {
                chatWindow.style.display = 'none';
            }, 350);
            closeCamera();
        }
        fab.classList.toggle('active', chatOpen);
    }

    // Toggle fullscreen
    function toggleFullscreen() {
        const icon = document.getElementById('aiFullscreenIcon');
        if (chatWindow.classList.contains('fullscreen')) {
            chatWindow.classList.remove('fullscreen');
            // Back to expand icon
            icon.innerHTML = '<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>';
        } else {
            chatWindow.classList.add('fullscreen');
            // Shrink icon
            icon.innerHTML = '<path d="M8 3v3h-3m18-3v3h-3m0 18v-3h3m-18 3v-3h-3"></path>';
        }
    }

    // Add message
    function addMessage(content, type, isHTML) {
        const div = document.createElement('div');
        div.className = `ai-msg ${type}`;
        if (isHTML) { div.innerHTML = content; } else { div.textContent = content; }
        messagesContainer.appendChild(div);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return div;
    }

    // Typing indicator
    function showTyping() {
        const div = document.createElement('div');
        div.className = 'ai-typing';
        div.id = 'aiTypingIndicator';
        div.innerHTML = '<span></span><span></span><span></span>';
        messagesContainer.appendChild(div);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    function hideTyping() {
        const el = document.getElementById('aiTypingIndicator');
        if (el) el.remove();
    }

    // ====== REAL AI: Analyze face via backend ======
    function analyzeFace(imageDataUrl) {
        // Show user's photo
        addMessage(`<img src="${imageDataUrl}" alt="Rasm" onclick="window.aiChat.openLightbox('${imageDataUrl}')">`, 'user', true);
        showTyping();

        fetch('/ai/analyze-face/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageDataUrl })
        })
        .then(res => res.json())
        .then(data => {
            hideTyping();

            if (data.error) {
                addMessage('⚠️ ' + (data.message || 'Xatolik yuz berdi'), 'bot', false);
                return;
            }

            const result = data.data;

            // Face analysis message
            const shapeEmoji = {
                'oval': '🟢', 'Oval': '🟢',
                'dumaloq': '🔵', 'Dumaloq': '🔵', 'round': '🔵',
                "to'rtburchak": '🟧', "To'rtburchak": '🟧', 'square': '🟧',
                "cho'ziq": '🟣', "Cho'ziq": '🟣', 'oblong': '🟣',
                'yurak': '❤️', 'Yurak shakli': '❤️', 'heart': '❤️',
                'olmos': '💎', 'Olmos shakli': '💎', 'diamond': '💎'
            };

            const emoji = shapeEmoji[result.face_shape] || '🔍';
            addMessage(
                `${emoji} <strong>Yuz shakli:</strong> ${result.face_shape}<br><br>` +
                `📋 ${result.face_analysis}`,
                'bot', true
            );

            // Recommendation cards
            if (result.recommendations && result.recommendations.length > 0) {
                setTimeout(() => {
                    let html = '✂️ <strong>Sizga mos soch turmaklari:</strong><div class="ai-result-grid">';
                    result.recommendations.forEach(r => {
                        let iconHtml = r.image_url 
                            ? `<img src="${r.image_url}" alt="${r.name}">`
                            : `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5"><circle cx="6" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><line x1="20" y1="4" x2="8.12" y2="15.88"></line><line x1="14.47" y1="14.48" x2="20" y2="20"></line><line x1="8.12" y1="8.12" x2="12" y2="12"></line></svg>`;
                            
                        html += `
                        <div class="ai-result-card" onclick="window.aiChat.openLightbox('${r.image_url}')">
                            <div class="ai-result-card-img">
                                ${iconHtml}
                            </div>
                            <div class="ai-result-card-body">
                                <div class="ai-result-card-header">
                                    <h5>${r.name}</h5>
                                    <div class="ai-result-card-match">${r.match_percent}%</div>
                                </div>
                                <p>${r.description}</p>
                            </div>
                        </div>`;
                    });
                    html += '</div>';
                    addMessage(html, 'bot', true);
                }, 600);
            }
        })
        .catch(err => {
            hideTyping();
            console.error('AI error:', err);
            addMessage('⚠️ Serverga ulanishda xatolik. Qaytadan urinib ko\'ring.', 'bot', false);
        });
    }

    // ====== REAL AI: Send text via backend ======
    function sendText() {
        const text = textInput.value.trim();
        if (!text) return;
        addMessage(text, 'user', false);
        textInput.value = '';
        showTyping();

        fetch('/ai/chat/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            hideTyping();
            if (data.error) {
                addMessage('⚠️ ' + (data.message || 'Xatolik'), 'bot', false);
            } else {
                addMessage(data.reply, 'bot', false);
            }
        })
        .catch(err => {
            hideTyping();
            console.error('Chat error:', err);
            addMessage('⚠️ Serverga ulanishda xatolik.', 'bot', false);
        });
    }

    // Handle file upload
    function handleFile(event) {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(e) {
            analyzeFace(e.target.result);
        };
        reader.readAsDataURL(file);
        event.target.value = '';
    }

    // Camera
    function openCamera() {
        const modal = document.getElementById('aiCameraModal');
        const video = document.getElementById('aiCameraVideo');
        modal.classList.add('open');

        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user', width: 640, height: 480 } })
            .then(stream => {
                cameraStream = stream;
                video.srcObject = stream;
            })
            .catch(err => {
                console.error('Camera error:', err);
                modal.classList.remove('open');
                addMessage('⚠️ Kameraga ruxsat berilmadi. Brauzer sozlamalaridan kameraga ruxsat bering.', 'bot', false);
            });
    }

    function closeCamera() {
        const modal = document.getElementById('aiCameraModal');
        const video = document.getElementById('aiCameraVideo');
        if (modal) modal.classList.remove('open');
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            cameraStream = null;
        }
        if (video) video.srcObject = null;
    }

    function takeSnapshot() {
        const video = document.getElementById('aiCameraVideo');
        const canvas = document.getElementById('aiCameraCanvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        const dataUrl = canvas.toDataURL('image/jpeg', 0.85);
        closeCamera();
        analyzeFace(dataUrl);
    }

    // Init
    document.addEventListener('DOMContentLoaded', function() {
        injectWidget();
    });

    // Public API
    window.aiChat = {
        toggle: toggleChat,
        toggleFullscreen: toggleFullscreen,
        sendText: sendText,
        handleFile: handleFile,
        openCamera: openCamera,
        closeCamera: closeCamera,
        takeSnapshot: takeSnapshot,
        openLightbox: function(src) {
            if (!src) return;
            document.getElementById('aiLightboxImg').src = src;
            document.getElementById('aiLightbox').classList.add('open');
        }
    };
})();
