

let showToast = (type, message) => {
    Toastify({
        text: message,
        className: type,
        style: {
            background: "linear-gradient(to right, #ffc107, #d09c00)",
        }
    }).showToast();
}


let addToFavorite = (bookId) => {
    
    let payload = {
        "book_id": bookId,
    };

    var requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    };

    fetch('/api/v1/books/favorite/add', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Hubo un problema al agregar el artículo a favoritos.', response);
            }
            return response.json();
        })
        .then(data => {
            let elementHTML = 'book_' + bookId;
            document.getElementById(elementHTML).style.border = "3px solid #ffc107";
            console.log(data)
            showToast('info', data.ok);
        })
        .catch(error => {
            console.error('Error al agregar el artículo a favoritos:', error);
    });
}

