button = document.getElementById('timer_btn')

window.addEventListener('load', timer(60))

function timer(num) {
    time = num
    const timer_interval = setInterval(function () {
        if (time > 0) {
            time -= 1
            button.innerText = time
        } else {
            button.innerText = 'دوباره'
            if (button.parentElement.classList.contains('disabled')) {
                button.parentElement.classList.remove('disabled')
            }
            clearInterval(timer_interval)
        }

    }, 1000)
}

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


$(document).on('click', '#again', function (e) {
    e.preventDefault();
    Toastify({
        text: "ایمیل جدید درحال ارسال است",
        className: "info",
        style: {
            background: "linear-gradient(to right, #00b09b, #96c93d)",
        }
    }).showToast();
    text = 'درحال ارسال'
    $.ajax({
        url: $(this).attr('href'),
        type: 'GET',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (response) {
            $("#modal_btn").click()
        },
        error: function (error) {
            alert('eror')
        }
    })
    my_class = document.getElementById('again').classList
    my_class.add('disabled')
    my_class.remove('btn-outline-primary')
    my_class.add('btn-outline-success')
})
$(".otp-inputbar").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        $("#errmsg").html("Digits Only").show().fadeOut("slow");
        return false;
    }
});
i = 0
let final = []
$(".otp-inputbar").on("keyup keydown keypress", function (e) {
    if ($(this).val()) {
        $(this).next().focus();
        final.push($(this).val())
        console.log(final)
    }
    var KeyID = e.keyCode;
    switch (KeyID) {
        case 8:
            final.pop()
            $(this).val("");
            $(this).prev().focus();
            break;
        case 46:
            final.pop()
            $(this).val("");
            $(this).prev().focus();
            break;
        default:
            break;
    }
});

function set_val() {
    data = (final[0] + final[1] + final[2] + final[3] + final[4] + final[5])
    document.getElementById('final_input').value = parseInt(data)
}
