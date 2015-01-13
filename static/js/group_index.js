$(document).ready(function(){
    $('.post_resource_btn').click(function(){ clickbtn(this); });
    $('.fav_button').click(function(){ FavoriteResource(this) });
    $('.dlt_button').click(function(){ ShowConfirm(this) });
    
    $('.show_comment').click(function(){ $(this).next().toggle(); });
    
    $('.memo_edit').click(function(){ EditMemo(this) });
    $('.memo_edit_area').parent().children('.complete_button').click(function(){ CompleteEditMemo(this) });
    $('.memo_edit_area').parent().children('.cancel_button').click(function(){ CancelEditMemo(this) });
    
    function clickbtn(button){
        console.log(button.id);
        console.log($('form.resource_add_form').attr('action'));
        console.log($('.group_name').attr('href'));
        $.ajax({
            'url':$('.group_name').attr('href'),
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
    
    function EditMemo(button){
        console.log('リソースID → '+button.id);
        console.log($(button).parent().children('input'));
        $(button).parent().children('span.memo').css('display', 'none');
        $(button).parent().children('div').show();
        $(button).parent().children('div').children('input')
            .val($(button).parent().children('span.memo').text())
            .focus();
    }
    
    function CompleteEditMemo(button){
        var resource_id = $(button).parent().children('.memo_edit_area').attr('id');
        var memo_edit_value = $(button).parent().children('.memo_edit_area').val();
            
        $.ajax({
            'url': $('form.resource_add_form').attr('action'),
            'type': 'POST',
            'data': {
                'memo_edit_resource_id': resource_id,
                'memo_edit_value':  memo_edit_value
            },
            'dataType': 'json',
            'success': function(response){
                console.log(response.edit_success);
                if(response.edit_success){
                    $(button).parent().css('display', 'none');
                    $(button).parent().parent().children('button.memo_edit').show();
                    $(button).parent().parent().children('span.memo')
                        .text($(button).parent().children('.memo_edit_area').val())
                        .show();
                }
            },
        });
    }
    
    function CancelEditMemo(button){
        console.log('aaaa');
        $(button).parent().css('display', 'none');
        $(button).parent().parent().children('span.memo').show();
    }
    
    $('.resource_moreread').click(function(){
        var ID = $(this).attr('id');
        console.log(ID);
        if(ID){
            $('#more'+ID).html('<p>読み込み中...</p>');
            $.ajax({
                'url': $('form.resource_add_form').attr('action'),
                'type': 'POST',
                'data': {
                    'moreid': ID
                },
                'dataType': 'json',
                'success': function(response){
                    console.log(response.moreread_success);
                }
            });
        }
    });
});