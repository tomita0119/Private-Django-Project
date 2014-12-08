$(document).ready(function(){
    $('.link_btn').click(function(){ clickbtn(this); });
    
    function clickbtn(button){
        console.log(button.id);
        console.log($('form.resource_add_form').attr('action'));
        $.ajax({
            'url':$('form.resource_add_form').attr('action'),
            'type':'POST',
            'data':{
                'ajax':button.id,
            },
            'dataType':'json',
            'success':function(response){  // 通信が成功したら動く処理で、引数には返ってきたレスポンスが入る
                console.log('success!');
            },
        });
    }
});