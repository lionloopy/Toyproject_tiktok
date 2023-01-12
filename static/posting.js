
    $(document).ready(function () {
    show_detail();
    show_comments();
});

    function get_rank() {
    const a = new URL(window.location.href);
    const b = a.searchParams;
    const rank = b.get('rank');
    return rank
}

    function show_detail() {
    $('.allbox'). empty()
    $.ajax({
    type: "GET",
    url: "/posting",
    data: {},
    success: function (response) {

    let musics = response['musics'];

    for (let i = 0; i < 50; i++) {
    let rank = musics[i]['rank']

    if (rank == get_rank()) {
    let image = musics[i]['image']
    let singer = musics[i]['singer']
    let title = musics[i]['title']
    let album = musics[i]['album']

    let temp_html1 = `<div class="card text-center">
                          <div class="card-header">
                            <ul class="nav nav-tabs card-header-tabs">
                              <li class="nav-item">
                                <a class="nav-link active" aria-current="true" href="#">앨범</a>
                              </li>
                              <li class="nav-item">
                                <a class="nav-link" href="https://www.tiktok.com/foryou?lang=ko-KR" style="color:#0AC9FF">틱톡 바로가기</a>
                              </li>
                            </ul>
                          </div>
                          <div class="card-body">
                            <img src=${image} class="card-img-top" alt="..." style="heigh:200px; width:200px;">
                            <div style="margin-top:20px;">
                            <h5 class="card-text">${title} - ${singer}</h5>
                            <p>${album}</a>
                            </div>
                          </div>
                        </div>`
    $('.allbox').append(temp_html1);

}

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
            for (let i = 0; i < rows.length; i++) {

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

    $(document).on("click", '.delete', function () {

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


}
