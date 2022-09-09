// Asynchronous view updates

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