jQuery(document).ready(function(){
    if(window.location.pathname === "/admin/metadata/pccvehicleinfo/"){
        //pcc车辆信息管理按钮添加   导出excel
        jQuery("#content-main").find("ul").append('<li><a href="/ajax/pcc_vehicle_export_excel/" class="button">导出Excel</a></li>');
        jQuery("#content-main").find("ul > li").css('float', 'left');
    }
    if(window.location.pathname === "/admin/metadata/pccupgradedetail/"){
        //pcc升级明细按钮添加   导出excel
        jQuery("#content-main").find("ul").append('<li><a href="/ajax/pcc_upgrade_export_excel/" class="button">导出Excel</a></li>');
        jQuery("#content-main").find("ul > li").css('float', 'left');
    }
    if(window.location.pathname === "/admin/metadata/pccproblemdetail/"){
        //pcc问题明细按钮添加   导出excel
        jQuery("#content-main").find("ul").append('<li><a href="/ajax/pcc_problem_export_excel/" class="button">导出Excel</a></li>');
        jQuery("#content-main").find("ul > li").css('float', 'left');
    }
    if(window.location.pathname === "/admin/metadata/pccdepotname/"){
        //pcc车厂管理按钮添加   导出excel
        jQuery("#content-main").find("ul").append('<li><a href="/ajax/pcc_depot_export_excel/" class="button">导出Excel</a></li>');
        jQuery("#content-main").find("ul > li").css('float', 'left');
    }
});