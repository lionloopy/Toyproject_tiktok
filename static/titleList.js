$(document).ready(function () {
    listing();
});

function listing() {
    $.ajax({
        type: 'GET',
        url: '/music',
        data: {},
        success: function (response) {
            let rows = response['musics']

            for (let i = 0; i < 50; i++) {
                let rank = rows[i]['rank'];
                let image = rows[i]['image'];
                let title = rows[i]['title'];
                let singer = rows[i]['singer'];
                let album = rows[i]['album'];

                let temp_html = `<tr id="table" class="chart-text" onclick="moveToPostingPage(${rank})">
                                                <th scope="col" id="num" style="width: 80px;">${rank}</th>
                                                <th id="image" scope="col" colspan="3" style="width: 25px;height: 25px;"><img src="${image}"></th>
                                                <th scope="col" id="title" style="width: 200px" class="title-text">${title}</th>
                                                <th id="singer" scope="col" style="width: 50px" class="title-text">${singer}</th>
                                                <th id="album" scope="col" class="album-text">${album}</th>
                                         </tr>`
                $('#music-box').append(temp_html)
            }
        }
    })
}

const moveToPostingPage = (rank) => {
    // let a = new URL('http://127.0.0.1:5100/page/detail')
    // let b = new URLSearchParams(a)
    // let c = b.set("rank",rank)
    // window.location.href = c
    // console.log(c)

    let a = new URL(`http://3.36.74.123:5000/page/detail?rank=${rank}`)

    window.location.href = a

// ?gil=yes&log=wow&gillog=good
}
