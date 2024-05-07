var menu = document.getElementById("menu-open");

menu.onclick = function () {
  menu.classList.toggle("menu-close");
};

$(document).ready(function() {
    $(".menu-block").hide() <!-- прячет блок с категориями-->

    $(".menu-button").on("click", function() {
        $(".menu-block").slideToggle(500);
    });

    $(window).scroll(function() { <!--добавляет класс fixed к шапке сайта и убирает-->
        var mainScroll = $(".main").height() / 2
//        var mainScroll = 200
        if($(this).scrollTop() > mainScroll){
            $(".header").removeClass("fixed");
        }
        else if ($(this).scrollTop() < mainScroll){
            $(".header").addClass("fixed");
        }
    });

    $(function() {

        var pathname_url = window.location.pathname;
        var href_url = window.location.href;

        $(".menu-ul ul a").each(function () {

            var link = $(this).attr("href");
            if(pathname_url == link || href_url == link) {
                $(this).addClass("active-category");
            }

        });

    });

});