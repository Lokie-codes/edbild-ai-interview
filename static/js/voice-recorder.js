let mediaRecorder;
let chunks = [];
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const audioElement = document.querySelector('audio');

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            chunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, { type: 'audio/webm' });
            chunks = [];
            const audioURL = URL.createObjectURL(blob);
            audioElement.src = audioURL;

            sendAudioToServer(blob);
        };
    })
    .catch(error => {
        console.error('Error accessing microphone:', error);
    });

startButton.addEventListener('click', () => {
    mediaRecorder.start();
    startButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    startButton.disabled = false;
    stopButton.disabled = true;
});

function sendAudioToServer(blob) {
    const url = 'http://127.0.0.1:8000/answer/';
    const formData = new FormData();

    const audioFile = new File([blob], 'recorded_audio.wav', { type: 'audio/wav' });
    formData.append('audio', audioFile);

    const csrfToken = getCookie('csrftoken');

    const role = document.getElementById('role').value;
    const question = document.getElementById('question_id').value;
    const user = document.getElementById('user_id').value;
    const email = document.getElementById('email').value;
    const phone_number = document.getElementById('phone_number').value;

    formData.append('role', role);
    formData.append('question', question);
    formData.append('name', user);
    formData.append('email', email);
    formData.append('phone_number', phone_number);


    fetch(url, {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': csrfToken, },
    })
        .then(response => {
            // Handle the server response here if needed
            console.log('Audio file sent successfully.');
        })
        .catch(error => {
            console.error('Error sending audio file:', error);
        });
}

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}