function ShowSearch() {
    document.getElementById('search-block').style.bottom = '50px';
    document.getElementById('search-icon').src = '/static/img/icons/close-search.png';
    document.getElementById('search-button').onclick = HideSearch;
}

function HideSearch() {
    document.getElementById('search-block').style.bottom = '-200px';
    document.getElementById('search-icon').src = '/static/img/icons/search.png';
    document.getElementById('search-button').onclick = ShowSearch;
}

async function SignOut() {
    let response = await fetch('/api/sign/out/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        ShowNotify(result['data']['message']);

        setTimeout(function(){
            window.location.href = '/sign/';
        }, 1500);
    } else {
        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}

async function SignIn() {
    let username = document.getElementById('SignIn-username').value;
    let password = document.getElementById('SignIn-password').value;

    let response = await fetch('/api/sign/in/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        localStorage.setItem('token', result['data']['token']);
        ShowNotify(result['data']['message']);
        document.getElementById('SignIn-username').value = '';
        document.getElementById('SignIn-password').value = '';

        setTimeout(function(){
            window.location.href = '/account/' + username + '/';
        }, 1500);
    } else {

        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


async function SubscribeToUser(username) {
    let response = await fetch('/api/subscribeToUser/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            token: localStorage.getItem('token')
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        ShowNotify(result['data']['message']);
        if (result['data']['subscrube_status'] === 0) {
            document.getElementById('subscribe_button').innerHTML = 'Подписаться';
            if (!document.getElementById('subscribers_count').innerHTML.includes('?')) {
                document.getElementById('subscribers_count').innerHTML = Number(document.getElementById('subscribers_count').innerHTML) - 1;
            }
        } else {
            document.getElementById('subscribe_button').innerHTML = 'Отписаться';
            if (!document.getElementById('subscribers_count').innerHTML.includes('?')) {
                document.getElementById('subscribers_count').innerHTML = Number(document.getElementById('subscribers_count').innerHTML) + 1;
            }
        }
    } else {

        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}

async function SignUp() {
    let username = document.getElementById('SignUp-username').value;
    let password = document.getElementById('SignUp-password').value;
    let nickname = document.getElementById('SignUp-nickname').value;
    let date_of_birth = document.getElementById('SignUp-date_of_birth').value;

    let response = await fetch('/api/sign/up/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password,
            nickname: nickname,
            date_of_birth: date_of_birth
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        localStorage.setItem('token', result['data']['token']);
        ShowNotify(result['data']['message']);
        document.getElementById('SignIn-username').value = '';
        document.getElementById('SignIn-password').value = '';
        document.getElementById('SignIn-nickname').value = '';
        document.getElementById('SignIn-date_of_birth').value = '';

        setTimeout(function(){
            window.location.href = '/';
        }, 1500);
    } else {

        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


function ShowSignUpBlock() {
    document.getElementById('sign-in-block').style.top = '-1500px'
    document.getElementById('sign-up-block').style.top = '0px'
}


function ShowSignInBlock() {
    document.getElementById('sign-in-block').style.top = '0px'
    document.getElementById('sign-up-block').style.top = '-1500px'
}


function HideToolbar() {
    document.getElementById('main-toolbar').style.opacity = '0';
    document.getElementById('toolbar-tools-img').src = '/static/img/icons/show.png';
    document.getElementById('toolbar-tools-img').onclick = function () {ShowToolbar();};
    localStorage.setItem('toolbar-view', 0);
    setTimeout(function(){
         document.getElementById('main-toolbar').style.display = 'none';
    }, 200);
}


function ShowToolbar() {
    document.getElementById('main-toolbar').style.display = 'inline-block';
    document.getElementById('toolbar-tools-img').src = '/static/img/icons/hide.png';
    document.getElementById('toolbar-tools-img').onclick = function () {HideToolbar();};
    localStorage.setItem('toolbar-view', 1);
    setTimeout(function(){
         document.getElementById('main-toolbar').style.opacity = '100';
    }, 200);
}


function checkToolbar() {
    if (localStorage.getItem('toolbar-view') === "0") {
        HideToolbar();
    } else if (localStorage.getItem('toolbar-view') === "1") {
        ShowToolbar();
    }
}

async function EditProfile() {
    let formData = new FormData();
    formData.append('username', document.getElementById('nickname-edit').value)
    formData.append('avatar', document.getElementById('profile-avatar').files[0])
    formData.append('nickname', document.getElementById('username-edit').value)
    formData.append('status_emoji', document.getElementById('status_emoji-edit').value)
    formData.append('status', document.getElementById('status-edit').value)
    formData.append('token', localStorage.getItem('token'))

    let response = await fetch('/api/account/editProfile/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        ShowNotify(result['data']['message']);

        setTimeout(function(){
            window.location.href = '/account/' + document.getElementById('nickname-edit').value + '/';
        }, 1500);
    } else {

        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


async function CreatePost() {
    let formData = new FormData();
    formData.append('text', document.getElementById('post-text').value)
    formData.append('image', document.getElementById('post-image').files[0])
    formData.append('theme', document.getElementById('post-theme').value)
    formData.append('token', localStorage.getItem('token'))

    let response = await fetch('/api/create/post/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        ShowNotify(result['data']['message']);

        setTimeout(function(){
            window.location.href = '/post/' + result['data']['post_id'] + '/';
        }, 1500);
    } else {

        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}

async function LikePost(post_id) {
    let response = await fetch('/api/likeModel/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': post_id,
            'model_name': 'post',
            'token': localStorage.getItem('token')
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        if (result['data']['like_status'] === 1) {
            document.getElementById('likes-count').innerHTML = Number(document.getElementById('likes-count').innerHTML) + 1;
            document.getElementById('like-icon').src = '/static/img/icons/like.png'
        } else {
            document.getElementById('likes-count').innerHTML = Number(document.getElementById('likes-count').innerHTML) - 1;
            document.getElementById('like-icon').src = '/static/img/icons/no_like.png'
        }
    } else {
        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


async function LikeComment(comment_id) {
    let response = await fetch('/api/likeModel/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': comment_id,
            'model_name': 'comment',
            'token': localStorage.getItem('token')
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        if (result['data']['like_status'] === 1) {
            document.getElementById('comment-likes-count' + comment_id).innerHTML = Number(document.getElementById('comment-likes-count' + comment_id).innerHTML) + 1;
            document.getElementById('comment-like-icon' + comment_id).src = '/static/img/icons/like.png'
        } else {
            document.getElementById('comment-likes-count' + comment_id).innerHTML = Number(document.getElementById('comment-likes-count' + comment_id).innerHTML) - 1;
            document.getElementById('comment-like-icon' + comment_id).src = '/static/img/icons/no_like.png'
        }
    } else {
        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


async function CreateComment(post_id) {
    let response = await fetch('/api/create/comment/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'post_id': post_id,
            'text': document.getElementById('comment-text').value,
            'token': localStorage.getItem('token')
        })
    });
    document.getElementById('comment-text').value = '';

    let result = await response.json();

    if (result['status'] === 'OK') {
        ShowNotify(result['data']['message']);
    } else {
        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


async function DeleteComment(comment_id) {
    let response = await fetch('/api/delete/comment/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'comment_id': comment_id,
            'token': localStorage.getItem('token')
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        ShowNotify(result['data']['message']);
    } else {
        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


async function DeletePost(post_id) {
    let response = await fetch('/api/delete/post/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'post_id': post_id,
            'token': localStorage.getItem('token')
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        ShowNotify(result['data']['message']);

        setTimeout(function(){
            window.location.href = '/';
        }, 1500);
    } else {
        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


async function DeleteComment(comment_id) {
    let response = await fetch('/api/delete/comment/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'comment_id': comment_id,
            'token': localStorage.getItem('token')
        })
    });
    let result = await response.json();

    if (result['status'] === 'OK') {
        document.getElementById('comment' + comment_id).remove();
        ShowNotify(result['data']['message']);
    } else {
        let notify_text = ''
        for (item in result['data']) {
            notify_text += result['data'][item][0] + ' (' + item + ')<br><br>';
        }
        ShowNotify(notify_text);
    }
}


function ShowComments() {
    document.getElementById('comments-block').style.display = 'block'
    document.getElementById('post-text').style.display = 'none'
    document.getElementById('comments-icon').src = '/static/img/icons/back.png'
    document.getElementById('comments-icon-block').onclick = function() {HideComments()}

}

function HideComments() {
    document.getElementById('comments-block').style.display = 'none'
    document.getElementById('post-text').style.display = 'block'
    document.getElementById('comments-icon').src = '/static/img/icons/comments.png'
    document.getElementById('comments-icon-block').onclick = function() {ShowComments()}
}

function HidePosts() {
    document.getElementById('posts').style.display = 'none'
    document.getElementById('link-conditions2').onclick = function() {HidePostCreateForm();}
}

function ShowPosts() {
    document.getElementById('posts').style.display = 'inline-block'
    document.getElementById('link-conditions2').onclick = function() {ShowPostCreateForm();}
}


function ShowPostCreateForm() {
    ShowConditions(2);
    HidePosts();
}

function HidePostCreateForm() {
    HideConditions(2);
    ShowPosts();
}