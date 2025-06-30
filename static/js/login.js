document.getElementById('login').onclick = function () {
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value
    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'email': email,
            'password': password
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.alert('Login successful!');
                window.location.href = '/';
            } else {
                window.alert('Error: ' + data.error);
            }
        })
        .catch(err => {
            window.alert('500 Internal Server Error')
            console.error('500 Internal Server Error: ', err);
        });
}