const input = document.getElementById('portal_url_input')
const p = document.getElementById('portal_url_p')
const hide_input = document.getElementById('portal_url_hide')

input.addEventListener('input', function () {
    const input_val = input.value.toLowerCase()
    p.textContent = input_val.replace(/\s+/g, '-')
    hide_input.value = input_val.replace(/\s+/g, '-')
})
