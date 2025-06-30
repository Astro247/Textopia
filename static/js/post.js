document.getElementById('submitPost').onclick = function () {
    const title = document.getElementById('postTitle').value
    const content = document.getElementById('textContent').value
    fetch('/createPost', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'title': title,
            'content': content
        })
    })
        .then(response => response.json())
        .then((data) => {
            if (data.success) {
                window.alert('Posted!')
                window.location.href = '/';
            }
            else {
                window.alert('All inputs must not be empty')
            }
        })
        .catch(err => {
            window.alert('500 Internal Server Error')
            console.error('500 Internal Server Error: ', err)
        });

}