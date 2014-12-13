$(document).ready(function(){
    $('.post_resource_btn').click(function(){ clickbtn(this); });
    $('.fav_button').click(function(){ FavoriteResource(this) });
    $('.dlt_button').click(function(){ ShowConfirm(this) });
    
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
    
    function FavoriteResource(button){
        console.log(button);
        $.ajax({
            'url': $('form.resource_add_form').attr('action'),
            'type': 'POST',
            'data':{
                'favorite_resource_id': button.id,
            },
            'dataType': 'json',
            'success':function(response){
                console.log(response.favorite_success);
                if(response.favorite_success){
                    $(button).parent().prepend('<p>お気に入りに登録しました.</p>');
                } else {
                    $(button).parent().prepend('<p>既にお気に入りに登録されています.</p>');
                }
            },
        });
    }
    
    function ShowConfirm(button){
        console.log($(button).parent());
        $(button).parent().children($('div.dlt_confirm')).show();
    }
});