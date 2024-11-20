// イベントを追加する関数
function addEvent() {
    const month = document.getElementById('month-select').value;
    const day = document.getElementById('day-select').value;
    const event = document.getElementById('event-input').value;

    if (month && day && event) {
        const eventList = document.getElementById('event-list');
        const newEvent = document.createElement('div');
        newEvent.classList.add('event-item');
        newEvent.innerHTML = `
            <span>${month} ${day}: ${event}</span>
            <button class="delete-button" onclick="deleteEvent(this)">削除</button>
        `;
        eventList.appendChild(newEvent);

        document.getElementById('event-input').value = '';
    }
}

// イベントを削除する関数
function deleteEvent(button) {
    const eventItem = button.parentNode;
    eventItem.remove();
    saveEvents(); // 削除後に保存
}

// イベントリストを保存する関数
function saveEvents() {
    const events = document.getElementById('event-list').innerHTML;
    localStorage.setItem('scheduleEvents', events);
    alert('スケジュールが保存されました！');
}

// ページロード時にローカルストレージからイベントを読み込む
window.onload = function() {
    const savedEvents = localStorage.getItem('scheduleEvents');
    if (savedEvents) {
        document.getElementById('event-list').innerHTML = savedEvents;
    }
};

