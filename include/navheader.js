const nav = document.querySelector('.topnav')
fetch('include/navheader.html')
.then(res =>res.text())
.then(data=>{
    nav.innerHTML=data
})