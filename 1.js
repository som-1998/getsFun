// Frontend code (JavaScript)
const loginBtn = document.getElementById('login-btn');

loginBtn.addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message); // Login successful
        } else {
            alert(data.message); // Invalid credentials
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
