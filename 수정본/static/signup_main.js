$(document).ready(function () {
    userList = [] // 이메일 중복을 위해 기존 이메일을 받아올 리스트
    get_user();
})

function get_user() {

    $.ajax({
        type: 'GET', url: '/signin', data: {}, success: function (response) {
            userList = response.users
        }
    })
}


$('#selectEmail').change(function () {
    $('#selectEmail option:selected').each(function () {
        if ($(this).val() == '1') {
            $('#str_email02').val('')
            $('#str_email02').attr("disabled", false)
        } else {
            $("#str_email02").val($(this).text())
            $("#str_email02").attr("disabled", true)
        }
    })
})

function save_account() {
    let firstName = $('#firstName').val()
    let lastName = $('#lastName').val()
    let name = firstName + ' ' + lastName   // 성과 이름을 공백으로 구분하여 '최 승호'와 '최승 호'를 구분

    let eMail = $('#str_email01').val() + '@' + $('#str_email02').val()
    let password = $('#password').val()
    let passwordConfirm = $('#passwordConfirm').val()

    //공백 제어
    if ([firstName, lastName, $('#str_email01'), password, passwordConfirm].includes('')) {
        alert("빈칸을 입력하세요")
        return;
    }

    // 비밀번호 확인 불일치 제어
    if (password !== passwordConfirm) {
        $('.wrong').remove()
        $('#password').val('')
        $('#passwordConfirm').val('')
        $('#password').focus()
        $('#password_area').append('<div class="wrong">비밀번호가 일치하지 않습니다.</div>')
        return
    }

    // 이메일 중복 제어
    for (let i = 0; i < userList.length; i++) {
        if (userList[i].email === eMail) {
            $('.wrong').remove()
            $('#email-area').append('<div class="wrong">이미 가입된 이메일입니다.</div>')
            $('#str_email01').focus()
            return;
        }
    }

    // 약관 동의 제어
    if(!cAll.checked){
        alert("약관에 동의하세요")
        return;
    }


    // 회원가입 정보 포스트
    $.ajax({
        type: 'POST',
        url: '/api/signup',
        data: {name_give: name, email_give: eMail, password_give: password},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

//UI
const getActive = (target) => {
    fieldList.forEach(item => item.classList.remove('active', 'semi-active'))
    target.classList.add('active')
}
let fieldList = document.querySelectorAll("input")
fieldList.forEach(field => field.addEventListener('focus', (e) => {
    getActive(e.target)
}))

// Welcome UI
const showName = () => {
    $('#welcome-area').empty()
    $('#welcome-area').append('<h8 style="color: white">.</h8>')
    let firstName = $('#firstName').val()
    let lastName = $('#lastName').val()
    if (firstName === '' || lastName === '') {
        return
    }
    let fullName = lastName + firstName
    let tmp_html = `<h8 id="welcome-name">${fullName}님 반갑습니다.</h8>`
    $('#welcome-area').append(tmp_html)
    $('#welcome-name').fadeIn(2000)

}
fieldList[1].addEventListener("blur", () => {
    showName()
})
fieldList[0].addEventListener("blur", () => {
    showName()
})

//팝업 관련
var target = document.querySelector('.btn_open');
var btnPopClose = document.querySelector('.pop_wrap .btn_close');
var targetID;

// 팝업 열기
target.addEventListener('click', function () {
    targetID = this.getAttribute('href');
    document.querySelector(targetID).style.display = 'block';
});

// 팝업 닫기
btnPopClose.addEventListener('click', function () {
    this.parentNode.parentNode.style.display = 'none';
});

// 팝업 체크
const c1 = document.getElementById("c1")
const c2 = document.getElementById("c2")
const c3 = document.getElementById("c3")
const cAll = document.getElementById("c_all")
const checkArea = document.getElementById("check-area")

//전체 체크
cAll.addEventListener("change", () => {
    c1.checked = cAll.checked
    c2.checked = cAll.checked
    c3.checked = cAll.checked
})
checkArea.addEventListener("change", () => {
    if (c1.checked && c2.checked && c3.checked) {
        cAll.checked = true
    }
    if (cAll.checked) {
        btnPopClose.click()
    }
})
