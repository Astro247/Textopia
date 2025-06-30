username = document.getElementById('username')
email = document.getElementById('email')

fetch('/getProfile', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
})
    .then(response => response.json())
    .then(data => {
        username.textContent = `Username: ${data.username}`
        email.textContent = `Email: ${data.email}`
    })
    .catch(err => {
        window.alert('500 Internal Server Error')
        console.error('500 Internal Server Error: ', err);
    });