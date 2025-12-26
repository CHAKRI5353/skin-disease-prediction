document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("imageInput");
    const preview = document.getElementById("preview");
    const dropzone = document.getElementById("dropzone");
    const clearBtn = document.getElementById("clearBtn");
    const analyzeBtn = document.querySelector(".controls .btn[type='submit']");
    const ghostBtn = document.querySelector(".controls .btn.ghost");

    // Function to handle image change and preview
    input.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Hide the placeholder text/icon
        const placeholder = dropzone.querySelector(".placeholder");
        if (placeholder) {
            placeholder.style.display = "none";
        }

        const url = URL.createObjectURL(file);
        preview.src = url;
        preview.style.display = "block";
    });

    // simple drag UI (Preserves animation)
    dropzone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropzone.style.transform = "translateY(-6px) scale(1.01)";
    });

    dropzone.addEventListener("dragleave", (e) => {
        dropzone.style.transform = "";
    });

    dropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropzone.style.transform = "";
        const dt = e.dataTransfer;
        if (dt.files && dt.files.length) {
            input.files = dt.files;
            // Manually trigger the 'change' event to update the preview
            const evt = new Event("change", { bubbles: true });
            input.dispatchEvent(evt);
        }
    });

    // Clear button logic to reset the app state
    clearBtn && clearBtn.addEventListener("click", () => {
        // Clear the file input
        input.value = "";

        // Reload the current page to clear both the JS preview and the server-side prediction results
        window.location.href = window.location.pathname;
    });

    // ADDED: Simple active state for buttons for haptic-like feedback
    if (analyzeBtn) {
        analyzeBtn.addEventListener('mousedown', () => {
            analyzeBtn.style.transform = 'scale(0.98)';
        });
        analyzeBtn.addEventListener('mouseup', () => {
            analyzeBtn.style.transform = 'translateY(-2px)'; // Return to hover state
        });
    }
    if (ghostBtn) {
        ghostBtn.addEventListener('mousedown', () => {
            ghostBtn.style.transform = 'scale(0.98)';
        });
        ghostBtn.addEventListener('mouseup', () => {
            ghostBtn.style.transform = 'translateY(-2px)'; // Return to hover state
        });
    }
});