function ShowConditions(conditions_id) {
    document.getElementById('conditions' + conditions_id).style.display = 'block';
    document.getElementById('link-conditions' + conditions_id).onclick = function() {HideConditions(conditions_id);}
}

function HideConditions(conditions_id) {
    document.getElementById('conditions' + conditions_id).style.display = 'none';
    document.getElementById('link-conditions' + conditions_id).onclick = function() {ShowConditions(conditions_id);}
}