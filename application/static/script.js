// TODO AJAX Calls for start and finish tickets

/*   
// Example POST method implementation:
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
  }

  postData('https://example.com/answer', { answer: 42 })
    .then((data) => {
      console.log(data); // JSON data parsed by `data.json()` call
    });


*/
    
async function postData(url = '') {
    const response = await fetch(url, { method: 'POST' })
    .then()
    
}

async function start_ticket(ticket_id) {
    res = await fetch(ticket_id + '/start', { method: 'POST'})
    data = await res.text()

    field = document.getElementById('started_at')
    field.readOnly = false;
    field.value = data;
    field.readOnly = true;
}

async function finish_ticket(ticket_id) {
    res = await fetch(ticket_id + '/finish', { method: 'POST'})
    data = await res.text()

    field = document.getElementById('finished_at')
    field.readOnly = false;
    field.value = data;
    field.readOnly = true;
}