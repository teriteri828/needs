$(function(){
    $('.dropdown-menu .dropdown-item').click(function(){
        var label = $('.dropdown-toggle', $(this).closest('.dropdown'));
        label.val($(this).attr('value'));
        label.text($(this).attr('value'));
        
        h_nid = "#h_" + $(this).attr('id');
        $(h_nid).val(label.val());
        console.log( $(h_nid).val());

    });
});