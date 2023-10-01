$(document).ready(function(){
    // 画像をクリックしたときの処理
    $('.image-clickable').click(function(){
      var modal = $('#imageModal');
      var modalImg = $('#modalImage');
      modal.css('display', 'block');
      modalImg.attr('src', $(this).attr('src'));
    });
  
    // モーダルウィンドウを閉じる処理
    $('.close').click(function(){
      $('#imageModal').css('display', 'none');
    });
  });
  