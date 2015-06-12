/**
 * Created by Ishayahu on 12.06.2015.
 */
// request permission on page load
document.addEventListener('DOMContentLoaded', function () {
    if (Notification.permission !== "granted")
        Notification.requestPermission();
});

function SoundNotify(icon,text,link,sound) {
    if (!Notification) {
        alert('Desktop notifications not available in your browser. Try Chromium.');
        return;
    }

    if (Notification.permission !== "granted")
        Notification.requestPermission();
    else {
        var notification = new Notification(
                'Notification title', {
            icon: icon,
            body: text
        });

        if (link!=0) {
            notification.onclick = function () {
                window.open(link);
            };
        }
        if (sound!=0) {
            var el = document.getElementById('sound');
            el.innerHTML = '<audio id=alarm-sound>' +
                '<source src="' + sound + '" type=audio/wav />' +
                '</audio>';
            document.getElementById('alarm-sound').play();
        }
    }

}
