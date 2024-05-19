var menu = document.getElementById("menu-open");

menu.onclick = function () {
  menu.classList.toggle("menu-close");
};

$(document).ready(function() {
    $(".menu-block").hide() <!-- прячет блок с категориями-->

    $(".menu-button").on("click", function() {
        $(".menu-block").slideToggle(500);
    });

// функция для скрытия/появления шапки при скролле
    var lastScrollTop = 0;
    $(window).scroll(function() {
        var st = $(this).scrollTop();
        if (st > lastScrollTop){
            // скроллим вниз
            $('.header').css('top', '-100px'); // прячем шапку
        } else {
            // скроллим вверх
            $('.header').css('top', '0'); // показываем шапку
        }
        lastScrollTop = st;
    });

// функция для активной категории
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

// Прячем блок c уведомлением через 5 секунд
    setTimeout(function() {
      $(".message").hide();
    }, 5000);

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
// для рекапчи
function onSubmit(token) {
    document.getElementById("demo-form").submit();
}



// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, соответствует ли cookie началу "name="
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }

    document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            fetch(`/like/${productId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                const icon = this.querySelector('i');
                    if (data.liked) {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        icon.style.color = 'red';
                    } else {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        icon.style.color = '';
                    }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });
    });
});
