// クリック可能な画像をクリックしたときの処理
document.querySelector('.clickable-image').addEventListener('click', function() {
    // モーダルウィンドウを取得
    var modal = document.createElement('div');
    modal.className = 'modal';

    // 画像をモーダルウィンドウ内に追加
    var modalContent = document.createElement('img');
    modalContent.className = 'modal-content';
    modalContent.src = this.src;

    // 閉じるボタンを追加
    var closeBtn = document.createElement('span');
    closeBtn.className = 'close';
    closeBtn.innerHTML = '&times;';

    // モーダルウィンドウにコンテンツを追加
    modal.appendChild(modalContent);
    modal.appendChild(closeBtn);

    // モーダルウィンドウをドキュメントに追加
    document.body.appendChild(modal);

    // 画像をクリックしたときにモーダルウィンドウを表示
    modal.style.display = 'block';

    // 閉じるボタンがクリックされたときにモーダルウィンドウを非表示
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        document.body.removeChild(modal);
    });

    // モーダルウィンドウの背景がクリックされたときにモーダルウィンドウを非表示
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.removeChild(modal);
        }
    });
});
