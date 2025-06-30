document.getElementById('register').onclick = function () {
    const username = document.getElementById('username').value
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value
    const cPassword = document.getElementById('cPassword').value
    if (password !== cPassword) { return window.alert('The two passwords don\'t match!') }
    fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'username': username,
            'email': email,
            'password': password
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.alert('Registration successful!');
                window.location.href = '/login';
            } else {
                window.alert('Error: ' + data.error);
            }
        })
        .catch(err => {
            window.alert('500 Internal Server Error')
            console.error('500 Internal Server Error: ', err);
        });
}