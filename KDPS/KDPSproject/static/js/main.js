document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScriptが読み込まれました！");
    document.getElementById("sendOtpForm").addEventListener("submit", function (e) {
        e.preventDefault(); // デフォルト送信を無効化
        console.log("フォーム送信イベントをキャッチしました。");

        const email = document.getElementById("email").value;
        console.log("入力されたメールアドレス:", email);

        fetch("/send-otp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => response.json())
        .then(data => {
            console.log("サーバーレスポンス:", data);
            if (data.error) {
                alert(data.error);
            } else {
                alert("認証コードを送信しました！");
            }
        })
        .catch(error => {
            console.error("エラー:", error);
        });
    });
});
