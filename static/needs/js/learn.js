$(function(){
    $('.dropdown-menu .dropdown-item').click(function(){
        var label = $('.dropdown-toggle', $(this).closest('.dropdown'));
        label.val($(this).attr('value'));
        label.text($(this).attr('value'));
        
        h_nid = "#h_" + $(this).attr('id');
        $(h_nid).val(label.val());
        console.log( $(h_nid).val());
        console.log("/static/needs");

    });
});


$(function(){
    $('.sort-table').tablesorter({
        textExtraction: function(node){
            var attr = $(node).attr('data-value');
            if(typeof attr !== 'undefined' && attr !== false){
                return attr;
            }
            return $(node).text();
        }
    });
});