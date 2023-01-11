
        function sign_up() {
            location.href = "/signup";
        }

        // {% if msg %}
        // alert("{{ msg }}")
        // {% endif %}

        // 로그인
        function sign_in() {
            let email =  $('#input-name').val();
            let password = $('#input-password').val()
            $.ajax({
                type: 'POST',
                url: '/api/sign_in',
                data: {email_give:email, pw_give:password},
                success: function (response) {
                    if (response['result'] == 'success') {
                        $.cookie('mytoken', response['token'], {path:'/'});
                        //로그인이 정상적으로 된다면 token을 받아옵니다.
                        //이 토큰을 mytoken이라는 key값으로 쿠키에 저장합니다.
                        alert('로그인 성공!')
                        window.location.href = '/page/main'
                    } else {
                        alert(response['msg'])
                    }
                }
            })

        }

