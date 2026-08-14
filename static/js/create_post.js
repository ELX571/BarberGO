document.addEventListener("DOMContentLoaded", () => {
    const createPostForm = document.getElementById("createPostForm");
    
    if (createPostForm) {
        createPostForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const errorDiv = document.getElementById("postError");
            const successDiv = document.getElementById("postSuccess");
            const btn = createPostForm.querySelector("button");
            
            errorDiv.style.display = "none";
            successDiv.style.display = "none";
            
            const originalBtnText = btn.innerHTML;
            btn.innerHTML = "Saqlanmoqda...";
            btn.disabled = true;

            const token = localStorage.getItem("access_token");
            if (!token) {
                errorDiv.innerText = "Avval tizimga kiring!";
                errorDiv.style.display = "block";
                btn.innerHTML = originalBtnText;
                btn.disabled = false;
                return;
            }

            const formData = new FormData();
            formData.append("title", document.getElementById("title").value);
            formData.append("description", document.getElementById("description").value);
            
            const imageFile = document.getElementById("image").files[0];
            if (imageFile) formData.append("image", imageFile);
            
            const videoFile = document.getElementById("video").files[0];
            if (videoFile) formData.append("video", videoFile);

            try {
                const response = await fetch("/posts/posts/", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`
                        // Do not set Content-Type for FormData, the browser sets it automatically with the correct boundary
                    },
                    body: formData
                });

                const data = await response.json();

                if (response.ok || response.status === 201) {
                    successDiv.innerText = "Post muvaffaqiyatli yaratildi!";
                    successDiv.style.display = "block";
                    createPostForm.reset();
                    
                    // Redirect to home page after a short delay
                    setTimeout(() => window.location.href = "/", 1500);
                } else {
                    let errorMsg = "Xatolik yuz berdi!";
                    if (data.error) {
                        errorMsg = data.error;
                    } else if (typeof data === 'object') {
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
                btn.innerHTML = originalBtnText;
                btn.disabled = false;
            }
        });
    }
});
