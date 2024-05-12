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
//        var mainScroll = $(".main").height() / 2
        var mainScroll = 50
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

//    Меняет стили для дефолтной кнопки загрузки фото(добавляем иконку)
    var icon = $('<i class="fa fa-user-circle" aria-hidden="true"><span class="image-text">загрузите ваше фото</span></i>');
    $('.profile form p:first-of-type label').append(icon);


// функция для анимации иконки с сообщением
    $('#feedback').mouseenter(function() {
        startShaking();
    });
    $('#feedback').mouseleave(function() {
        stopShaking();
    });

    function startShaking() {
        var block = $('#feedback');
        block.css('transition', 'transform 0.1s ease-in-out');
        var interval = setInterval(function() {
            var randomX = Math.random() * 10 - 5;
            var randomY = Math.random() * 10 - 5;
            block.css('transform', 'translate(' + randomX + 'px,' + randomY + 'px)');
        }, 100);
        block.data('interval', interval);
    }

    function stopShaking() {
        var block = $('#feedback');
        clearInterval(block.data('interval'));
        block.css('transform', 'translate(0, 0)');
    }
// прячет блок с отправкой сообщения
    $(".feedback-form").hide()

    $(".feedback").on("click", function() {
        $(".feedback-form").slideToggle(500);
    });

    setTimeout(function() {
      $(".message").hide();
    }, 5000); // Прячем блок через 5 секунд

});

// Функция для отображения комментариев на странице
$(document).ready(function() {
    var reviewsBlock = $(".reviews-all");
    var showMoreBtn = $("#show-more-btn");
    var reviewsCount = $(".reviews-count")
    var reviews = $(".review"); // Здесь будут храниться все комментарии
    var batchSize = 5; // Количество комментариев, отображаемых за раз
    var start = batchSize;

    // Функция для отображения комментариев
    function showReviews(startIndex, endIndex) {
        reviews.slice(startIndex, endIndex).show(); // Отображаем комментарии в заданном диапазоне
    }

    // Начальное скрытие всех комментариев, кроме первых batchSize
    reviews.slice(start).hide();

    // Проверка наличия комментариев и отображение кнопки и количество отзывов при необходимости
    if (reviews.length <= batchSize) {
        showMoreBtn.hide();
        reviewsCount.hide();
    }

    // При нажатии на кнопку "Показать еще"
    showMoreBtn.on("click", function() {
        var nextBatchEndIndex = Math.min(start + batchSize, reviews.length);
        showReviews(start, nextBatchEndIndex);
        start = nextBatchEndIndex; // Обновляем начальный индекс для следующей партии комментариев
        if (start >= reviews.length) {
            // Если больше нет комментариев, скрываем кнопку "Показать еще"
            showMoreBtn.hide();
        }
    });
});

//    function startShaking() {
//      var block = document.getElementById("feedback");
//      block.style.transition = 'transform 0.1s ease-in-out';
//      var interval = setInterval(function() {
//        var randomX = Math.random() * 10 - 5;
//        var randomY = Math.random() * 10 - 5;
//        block.style.transform = 'translate(' + randomX + 'px,' + randomY + 'px)';
//      }, 100);
//      block.interval = interval;
//    }
//
//    function stopShaking() {
//      var block = document.getElementById("feedback");
//      clearInterval(block.interval);
//      block.style.transform = 'translate(0, 0)';
//    }
