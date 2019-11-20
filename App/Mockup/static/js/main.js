function loadTable() {
    fetch('/spots', {
        method: 'GET',
        headers: {
            'Content-type': 'application/json'
        }
    })
    .then(data => data.json())
    .then(data => {
        console.log(data);
    })
}


// function uploadFrame() {
//     console.log("pls");
//     var input = document.querySelector('input[type="file"]');

//     const data = new FormData();
//     data.append('file', input.files[0]);
//     data.append('filename', 'example');
 
//     fetch('/upload', {
//         method: 'POST',
//         body: data
//     });
// }