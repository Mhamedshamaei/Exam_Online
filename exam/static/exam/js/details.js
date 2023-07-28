all_teacher_box = {}
window.addEventListener("load", function () {
    all_teacher_box = {}
})
$(document).on('click', '#add_teacher', function (e) {
    e.preventDefault();
    all_teacher_box = {}
    const teachers_div = document.getElementById('teachers_div')
    teachers_div.innerHTML = ''
    $.ajax({
        url: $(this).attr('href'),
        type: 'GET',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (response) {
            $('#teacher_load').css("display", "none");
            const keys = Object.keys(response);
            if (keys.length) {
                for (const [key, value] of Object.entries(response)) {
                    teachers_div.innerHTML += `<div class="input-group my-3">
                                <div class="input-group-text">
                                    <input class="form-check-input mt-0 checkbox-js" id="${key}" type="checkbox" value=""
                                           name="${value}" onclick="CheckBox(id)"
                                           aria-label="Checkbox for following text input">
                                </div>
                                <input class="form-control" type="text" value="${value}"
                                       aria-label="readonly input example" readonly>
                            </div>`
                }
            } else {
                teachers_div.innerHTML = '                            <div class="alert alert-secondary mt-3" role="alert">\n' +
                    '                                کلاسی یافت نشد !\n' +
                    '                            </div>'
            }
        },
        error: function (error) {
            alert('مشکلی پیش آمده ، لطفا مجدد تلاش کنید')
        }
    })
})

function CheckBox(id) {
    check = document.getElementById(id)
    if (check.checked) {
        all_teacher_box[check.id] = check.name
    } else {
        delete all_teacher_box[check.id]
        document.getElementById('btn' + check.id).remove()
        document.getElementById('btn' + check.id).remove()
        document.getElementById('btn' + check.id).remove()
        document.getElementById('btn' + check.id).remove()
    }
    const tkeys = Object.keys(all_teacher_box);
    const small_teacher_div = document.getElementById('small-teacher-div')
    if (tkeys.length) {
        $('#not-now-alert-teacher').css("display", "none");
        small_teacher_div.innerHTML += `<div id="btn${check.id}" class="btn-group mb-2 mx-1" role="group" aria-label="Basic example">
                                <button type="button" class="btn btn-primary sm btn-sm">${check.name}</button>
                                <button type="button" class="btn btn-primary sm btn-sm" onclick="DeleteBox(${check.id})"><i class="bi bi-trash"></i>
                                </button>
                            </div>`
    } else {
        small_teacher_div.innerHTML = `<div class="alert alert-secondary" role="alert" id="not-now-alert">\n` +
            '                                هنوز چیزی انتخاب نشده !\n' +
            `                            </div>`
    }
}

function DeleteBox(id) {
    document.getElementById('btn' + id).remove()
    document.getElementById(id).checked = false
    delete all_teacher_box[id]
}

function SetTeacherValue() {
    for (i in all_teacher_box) {
        document.getElementById('final_teacher_dic').value += i + ","
    }
}

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
