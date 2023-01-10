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
const plus =()=> {
    alert('dd')
}
let fieldList = document.querySelectorAll("input")
// fieldList.splice(4,0,"ddd")
fieldList.forEach(field => field.addEventListener('focus', (e) => {
    getActive(e.target)
}))
