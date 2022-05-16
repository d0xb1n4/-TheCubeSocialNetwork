function ShowNotify(text) {
    document.getElementById('hide-notify-button').style.display = 'inline-block'
    document.getElementById('notify-text').innerHTML = text;
    document.getElementById('notify').style.left = '10px';
}

function HideNotify() {
    document.getElementById('hide-notify-button').style.display = 'none'
    document.getElementById('notify-text').innerHTML = '';
    document.getElementById('notify').style.left = '-150px';
}