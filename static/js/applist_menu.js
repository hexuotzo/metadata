jQuery(document).ready(function(){
    //$('li a[href^="/admin/metadata/detail/"]').hide()
    //$('li a[href^="/admin/metadata/hivetablecolumninfo/"]').hide()

    // 立即执行按钮
    $(".execute_now").click(function(){
        rule_id = $(this).attr('data-attr')
        console.log(rule_id)

        $.ajax({
            type:"POST",
            url:"/ajax/rule_execute_now" ,
            data:{'rule_id':rule_id},
            dataType:"json",
            success:function(res){
                if(res.success=='ok'){
                    alert(res.msg)
                }else{
                    console.log('error!')
                }
            }
        });

    })
});