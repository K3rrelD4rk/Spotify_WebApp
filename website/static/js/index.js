// Funzione per la sostituzione dell'audio
function sostituisciSourceAudio(url) {
    var audioElement = document.getElementById('audio');
    if (!audioElement) {
        console.error("Elemento audio non trovato.");
        return;
    }

    audioElement.src = url;
}

// Funzione per la sostituzione del titolo e dell'artista
function sostituisciInformazioni(titolo, artista) {
    var titoloElement = document.querySelector('.player h2');
    var artistaElement = document.querySelector('.player h3');
    if (!titoloElement || !artistaElement) {
        console.error("Elementi titolo o artista non trovati.");
        return;
    }

    titoloElement.textContent = titolo;
    artistaElement.textContent = artista;
}

document.addEventListener('DOMContentLoaded', function() {
    // Funzione per la riproduzione e pausa dell'audio
    function togglePlayPause() {
        var audioElement = document.getElementById('audio');
        var playPauseButton = document.getElementById('play-pause');
        var playIcon = document.querySelector('.play-icon');
        var pauseIcon = document.querySelector('.pause-icon');
        if (!audioElement || !playPauseButton || !playIcon || !pauseIcon) {
            console.error("Elemento audio o pulsanti non trovati.");
            return;
        }

        if (audioElement.paused || audioElement.ended) {
            audioElement.play();
            playIcon.style.display = 'none';
            pauseIcon.style.display = 'inline';
        } else {
            audioElement.pause();
            playIcon.style.display = 'inline';
            pauseIcon.style.display = 'none';
        }
    }

    // Aggiorna la durata della canzone nel player
    function updateDuration() {
        var audioElement = document.getElementById('audio');
        var durationElement = document.querySelector('.total-time');
        if (!audioElement || !durationElement) {
            console.error("Elemento audio o elemento della durata non trovati.");
            return;
        }

        var duration = Math.floor(audioElement.duration);
        var minutes = Math.floor(duration / 60);
        var seconds = duration - minutes * 60;
        if (seconds < 10) {
            seconds = "0" + seconds;
        }
        durationElement.textContent = minutes + ":" + seconds;
    }

    // Aggiungi un evento di click al pulsante play/pausa
    var playPauseButton = document.getElementById('play-pause');
    if (playPauseButton) {
        playPauseButton.addEventListener('click', togglePlayPause);
    } else {
        console.error("Pulsante play/pausa non trovato.");
    }

    // Aggiorna la durata della canzone quando viene caricata
    var audioElement = document.getElementById('audio');
    if (audioElement) {
        audioElement.addEventListener('loadedmetadata', updateDuration);
    } else {
        console.error("Elemento audio non trovato.");
    }

    // Aggiorna la durata della canzone mentre viene riprodotta
    if (audioElement) {
        audioElement.addEventListener('timeupdate', updateDuration);
    }
});
