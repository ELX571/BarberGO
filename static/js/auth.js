document.addEventListener("DOMContentLoaded", () => {
    
    // LOGIN FORM HANDLER
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const errorDiv = document.getElementById("loginError");
            errorDiv.style.display = "none";
            
            const btn = loginForm.querySelector("button");
            const originalBtnText = btn.innerText;
            btn.innerText = "Kutib turing...";
            btn.disabled = true;

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("/accounts/auth-jwt/login/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem("access_token", data.access_token);
                    document.cookie = "access_token=" + data.access_token + "; path=/; max-age=86400;";
                    localStorage.setItem("refresh_token", data.refresh_token);
                    localStorage.setItem("user_data", JSON.stringify(data.user));
                    window.location.href = "/";
                } else {
                    let errorMsg = "Xatolik yuz berdi!";
                    if (data.non_field_errors) errorMsg = data.non_field_errors[0];
                    else if (data.error) errorMsg = data.error;
                    else if (typeof data === 'object') {
                        errorMsg = Object.values(data)[0][0] || errorMsg;
                    }
                    errorDiv.innerText = errorMsg;
                    errorDiv.style.display = "block";
                }
            } catch (err) {
                errorDiv.innerText = "Tarmoq xatosi. Iltimos qayta urinib ko'ring.";
                errorDiv.style.display = "block";
            } finally {
                btn.innerText = originalBtnText;
                btn.disabled = false;
            }
        });
    }

    // CUSTOM SELECT LOGIC
    const customSelectWrapper = document.querySelector('.custom-select-wrapper');
    if (customSelectWrapper) {
        const trigger = customSelectWrapper.querySelector('.select-trigger');
        const options = customSelectWrapper.querySelectorAll('.select-option');
        const hiddenSelect = document.getElementById('role');
        const selectText = customSelectWrapper.querySelector('.select-text');

        // Toggle open/close
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            customSelectWrapper.classList.toggle('open');
        });

        // Handle option selection
        options.forEach(option => {
            option.addEventListener('click', () => {
                const value = option.getAttribute('data-value');
                const text = option.querySelector('.option-text').innerText;
                
                // Update hidden select
                hiddenSelect.value = value;
                
                // Update trigger UI
                selectText.innerText = text;
                trigger.classList.add('selected');
                
                // Update active state on options
                options.forEach(opt => opt.classList.remove('active'));
                option.classList.add('active');
                
                // Close select
                customSelectWrapper.classList.remove('open');
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!customSelectWrapper.contains(e.target)) {
                customSelectWrapper.classList.remove('open');
            }
        });
    }

    // REGISTER FORM HANDLER
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const errorDiv = document.getElementById("registerError");
            errorDiv.style.display = "none";
            
            const btn = registerForm.querySelector("button");
            const originalBtnText = btn.innerText;
            btn.innerText = "Kutib turing...";
            btn.disabled = true;

            const formData = {
                first_name: document.getElementById("first_name").value,
                last_name: document.getElementById("last_name").value,
                username: document.getElementById("reg_username").value,
                email: document.getElementById("email").value,
                phone_number: document.getElementById("phone_number").value,
                role: document.getElementById("role").value,
                password: document.getElementById("reg_password").value,
                re_password: document.getElementById("re_password").value
            };

            if (formData.password !== formData.re_password) {
                errorDiv.innerText = "Parollar mos emas!";
                errorDiv.style.display = "block";
                btn.innerText = originalBtnText;
                btn.disabled = false;
                return;
            }

            try {
                const response = await fetch("/accounts/auth-jwt/register/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem("access_token", data.access_token);
                    document.cookie = "access_token=" + data.access_token + "; path=/; max-age=86400;"
                    localStorage.setItem("refresh_token", data.refresh_token);
                    localStorage.setItem("user_data", JSON.stringify(data.user));
                    window.location.href = "/";
                } else {
                    // Extract error message
                    let errorMsg = "Xatolik yuz berdi!";
                    if (data.non_field_errors) errorMsg = data.non_field_errors[0];
                    else if (typeof data === 'object') {
                        // Get first error from fields
                        const firstKey = Object.keys(data)[0];
                        if (Array.isArray(data[firstKey])) {
                            errorMsg = `${firstKey}: ${data[firstKey][0]}`;
                        } else {
                            errorMsg = data[firstKey];
                        }
                    }
                    errorDiv.innerText = errorMsg;
                    errorDiv.style.display = "block";
                }
            } catch (err) {
                errorDiv.innerText = "Tarmoq xatosi. Iltimos qayta urinib ko'ring.";
                errorDiv.style.display = "block";
            } finally {
                btn.innerText = originalBtnText;
                btn.disabled = false;
            }
        });
    }

    // FORGET PASSWORD UI LOGIC
    const loginCard = document.getElementById("loginCard");
    const forgetCard1 = document.getElementById("forgetCard1");
    const forgetCard2 = document.getElementById("forgetCard2");

    const showForgetPasswordLink = document.getElementById("showForgetPasswordLink");
    const backToLoginLink = document.getElementById("backToLoginLink");
    const backToLoginLink2 = document.getElementById("backToLoginLink2");

    if (showForgetPasswordLink && loginCard && forgetCard1) {
        showForgetPasswordLink.addEventListener("click", (e) => {
            e.preventDefault();
            loginCard.style.display = "none";
            forgetCard1.style.display = "block";
            forgetCard2.style.display = "none";
        });
    }

    if (backToLoginLink && loginCard && forgetCard1) {
        backToLoginLink.addEventListener("click", (e) => {
            e.preventDefault();
            forgetCard1.style.display = "none";
            loginCard.style.display = "block";
        });
    }

    if (backToLoginLink2 && loginCard && forgetCard2) {
        backToLoginLink2.addEventListener("click", (e) => {
            e.preventDefault();
            forgetCard2.style.display = "none";
            loginCard.style.display = "block";
        });
    }

    // FORGET PASSWORD STEP 1: VERIFY CODE REQUEST
    const forget1Form = document.getElementById("forget1Form");
    if (forget1Form) {
        forget1Form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const errorDiv = document.getElementById("forget1Error");
            errorDiv.style.display = "none";
            
            const btn = forget1Form.querySelector("button");
            const originalBtnText = btn.innerText;
            btn.innerText = "Kutib turing...";
            btn.disabled = true;

            const username = document.getElementById("forget_username").value;

            try {
                const response = await fetch("/accounts/forget-password/verify_code/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username })
                });

                const data = await response.json();

                if (response.ok) {
                    // Success! Show Step 2
                    forgetCard1.style.display = "none";
                    forgetCard2.style.display = "block";
                } else {
                    errorDiv.innerText = data.error || data.message || "Foydalanuvchi topilmadi!";
                    errorDiv.style.display = "flex";
                }
            } catch (err) {
                errorDiv.innerText = "Tarmoq xatosi!";
                errorDiv.style.display = "flex";
            } finally {
                btn.innerText = originalBtnText;
                btn.disabled = false;
            }
        });
    }

    // FORGET PASSWORD STEP 2: RESTORE PASSWORD
    const forget2Form = document.getElementById("forget2Form");
    if (forget2Form) {
        forget2Form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const errorDiv = document.getElementById("forget2Error");
            const successDiv = document.getElementById("forget2Success");
            errorDiv.style.display = "none";
            successDiv.style.display = "none";
            
            const btn = forget2Form.querySelector("button");
            const originalBtnText = btn.innerText;
            btn.innerText = "Kutib turing...";
            btn.disabled = true;

            const code = document.getElementById("forget_code").value;
            const password = document.getElementById("forget_new_password").value;
            const re_password = document.getElementById("forget_re_password").value;

            if (password !== re_password) {
                errorDiv.innerText = "Parollar mos emas!";
                errorDiv.style.display = "flex";
                btn.innerText = originalBtnText;
                btn.disabled = false;
                return;
            }

            try {
                const response = await fetch("/accounts/forget-password/restore_password/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ code, password, re_password })
                });

                const data = await response.json();

                if (response.ok) {
                    successDiv.style.display = "block";
                    forget2Form.reset();
                    btn.style.display = "none"; // Hide button after success
                } else {
                    errorDiv.innerText = data.error || data.message || "Xatolik yuz berdi!";
                    errorDiv.style.display = "flex";
                }
            } catch (err) {
                errorDiv.innerText = "Tarmoq xatosi!";
                errorDiv.style.display = "flex";
            } finally {
                if(btn.style.display !== "none") {
                    btn.innerText = originalBtnText;
                    btn.disabled = false;
                }
            }
        });
    }

});
