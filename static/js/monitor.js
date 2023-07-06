$(function(){

    setTimeout(function(){

        online_href = '<a href="/admin/schedule/monitorreal/add/" class="btn btn-success"><i class="fa fa-plus-circle"></i> &nbsp; 增加 实时任务监控</a>';
        $('#changelist > div:nth-child(1) > div.col-md-2.col-sm-12.col-xs-12.text-right > a').html('<i class="fa fa-plus-circle"></i> &nbsp;增加 离线任务监控')

        $('#changelist > div:nth-child(1) > div.col-md-2.col-sm-12.col-xs-12.text-right').append(online_href);

        console.log("monitor js");
    }, 200);

});
