function showBackArrow() {
    let params = window.location.search.replace('?','').split('&').reduce(
        function(p,e){
            var a = e.split('=');
            p[ decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
            return p;
        },
        {}
    );
    console.log(params['back'])
    if (params['back']) {
        document.getElementById('back-button').href = params['back'];
        console.log('True');
    } else {
        document.getElementById('back-button').style.display = 'none';
        console.log('False');
    }
}