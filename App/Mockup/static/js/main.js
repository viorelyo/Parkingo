function loadTable() {
    const spinner = document.getElementById("spinner");

    spinner.removeAttribute('hidden');
    fetch('/spots', {
        method: 'GET',
        headers: {
            'Content-type': 'application/json'
        }
    })
    .then(data => data.json())
    .then(data => {
        spinner.setAttribute('hidden', '');
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