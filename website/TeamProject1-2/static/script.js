let currentUserEmail = "";

document.addEventListener('DOMContentLoaded', () => {
    loadImages();
});

async function loadImages() {
    const container = document.getElementById('gallery-container');
    try {
        const response = await fetch('/api/images');
        const images = await response.json();

        if (images.length === 0) {
            container.innerHTML = "<p>No intel found.</p>";
            return;
        }

        container.innerHTML = images.map(img => `
            <div class="gallery-item">
                <img src="${img.src}" alt="${img.name}" width="200" height="200">
                <p>${img.name}</p>
            </div>
        `).join('');

    } catch (error) {
        container.innerHTML = "<p style='color:red'>Comm Link Failure: Cannot fetch images.</p>";
    }
}

async function requestCode() {
    const emailInput = document.getElementById('email-input');
    const email = emailInput.value;

    if (!email) {
        alert("Enter an email.");
        return;
    }

    try {
        const res = await fetch('/api/login/request-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json();

        if (data.success) {
            currentUserEmail = email;
            document.getElementById('step-email').classList.add('hidden');
            document.getElementById('step-code').classList.remove('hidden');
            alert("Code sent! Check your secure comms (or server console).");
        } else {
            alert(data.message);
        }
    } catch (e) {
        alert("System Error: " + e);
    }
}

async function verifyCode() {
    const codeInput = document.getElementById('code-input');
    const code = codeInput.value;

    try {
        const res = await fetch('/api/login/verify-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: currentUserEmail, code })
        });
        const data = await res.json();

        if (data.success) {
            document.getElementById('login-form').classList.add('hidden');
            document.getElementById('secret-content').classList.remove('hidden');
        } else {
            alert(data.message);
        }
    } catch (e) {
        alert("System Error: " + e);
    }
}

function resetLogin() {
    document.getElementById('step-email').classList.remove('hidden');
    document.getElementById('step-code').classList.add('hidden');
    document.getElementById('email-input').value = "";
    document.getElementById('code-input').value = "";
}
