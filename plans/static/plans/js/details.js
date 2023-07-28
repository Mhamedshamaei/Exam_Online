price = document.getElementById('price')
num = price.innerText
price.innerHTML = numeral(num).format('0,0')
price2 = document.getElementById('price2')
num2 = price2.innerText
price2.innerHTML = numeral(num2).format('0,0')
