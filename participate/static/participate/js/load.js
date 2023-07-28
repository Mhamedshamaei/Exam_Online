dic = {}
window.addEventListener('load', function () {
    dic = {}
})
var swiper = new Swiper(".mySwiper", {
    pagination: {
        el: ".swiper-pagination",
        type: "fraction",
    },
    navigation: {
        nextEl: ".swiper-button-prev",
        prevEl: ".swiper-button-next",
    },
    keyboard: true,
});

function AddToDb(key, value) {
    const q = document.getElementById('q')
    dic[key] = value
    for (const [key, value] of Object.entries(dic)) {
        dic[key] = value
        result = q.value.includes(`${key}:`)
        if (result) {
            q.value += `${key}:${value},`
        } else {
            q.value += `${key}:${value},`
        }
    }
    console.log(q.value)
}

function FinishExam() {
    q.value += `{${q.value}}`
    console.log(q.value)
}
