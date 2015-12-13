$(document).ready(function() {
    //toggle `popup` / `inline` mode
    $.fn.editable.defaults.mode = 'inline';     
    
    //make username editable
    $('#category_name').editable();
    $('#item_title').editable();
    $('#item_description').editable();
                  
    //make status editable
    $('#status').editable({
        type: 'select',
        title: 'Select status',
        placement: 'right',
        value: 2,
        source: [
            {value: 1, text: 'status 1'},
            {value: 2, text: 'status 2'},
            {value: 3, text: 'status 3'}
        ]
        /*
        //uncomment these lines to send data on server
        ,pk: 1
        ,url: '/post'
        */
    });
                  
    $(function() {
                    $( "#button-edit" ).button({
                                            icons: {
                                            primary: "ui-icon-locked"
                                            },
                                            text: false
                                            });
                    $( "#button-7" ).button({
                                            disabled:true
                                            });
                    $( "#button-8" ).button({
                                            icons: {
                                            primary: "ui-icon-gear",
                                            secondary: "ui-icon-triangle-1-s"
                                            }
                                            });
    });
              
                  
});