
        $(document).ready(function () {
            show_detail();
            show_comments();
        });
        function show_detail() {
            $.ajax({
                type: "GET",
                url: "/posting",
                data: {},
                success: function (response) {
                    let rows = response['musics']
                    for(let i = 0; i < rows.length; i++) {

                        let image = rows[i]['image']
                        let title = rows[i]['title']
                        let singer = rows[i]['singer']
                        let album = rows[i]['album']

                        let temp_html1 = `<img src=${image} alt="앨범 img" height="300" width="350">`
                        let temp_html2 = `<h3 class="card-title"> ${singer} - ${title}</h3>
                                          <p class="card-text text-muted">
                                            앨범명 : ${album}
                                          </p>`

                        $('.album').append(temp_html1);
                        $('.card-body').append(temp_html2);

                    }
                }
            });
        }

        function posting() {
            if (confirm("코멘트를 저장하시겠습니까?")) {
                let comment = $('#comment').val()

                $.ajax({
                    type: "POST",
                    url: "/posting",
                    data: {comment_give: comment},
                    success: function (response) {
                        alert(response["msg"])
                        window.location.reload()
                    }
                });
            } else {
                alert("취소하였습니다!");
            }
        }

        function show_comments() {
            $.ajax({
                type: "GET",
                url: "/posting",
                data: {},
                success: function (response) {
                    let rows = response['comments']
                    for(let i = 0; i < rows.length; i++) {

                        let comment = rows[i]['comment']
                        let number = rows[i]['num']

                        let temp_html = `<li class="list-group-item d-flex justify-content-between">
                                            <span id="comments" data-id="${number}">퐝원준 : ${comment} </span>
                                            <button type="button" class="btn btn-danger delete">삭제</button>
                                         </li>`

                        $('#comments-list').append(temp_html)

                    }
                }
            });

            $(document).on("click", '.delete' , function () {

            if (confirm("위 댓글을 삭제하시겠습니까?")) {
               let number = $('#comments').data("id");
               let comments = $('#comments').val();

               $.ajax({
                    type: "POST",
                    url: "/comment/delete",
                    data: {number_give: number, comments_give: comments},
                    success: function (response) {
                        alert(response["msg"]);
                        window.location.reload()
                    }
               });

            } else {
                alert("취소하였습니다!");
           }
            //show_music();
        });

            // $('.delete').click(function(){
            //     alert("삭제 할거지?")
            // });


       }

       // function show_music() {
       //      $.ajax({
       //          type: "GET",
       //          url: "/posting/music",
       //          data: {},
       //          success: function (response) {
       //              let rows = response['comments']
       //              for(let i = 0; i < rows.length; i++) {
       //                  let comment = rows[i]['comment']
       //
       //                  let temp_html = `<li class="list-group-item"><span class="fw-bold">퐝원준 : </span> ${comment}</li>`
       //
       //                  $('#comments-list').append(temp_html)
       //              }
       //          }
       //      });
       // }

