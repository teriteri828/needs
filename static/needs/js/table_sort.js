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