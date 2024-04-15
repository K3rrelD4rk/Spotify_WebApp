document.addEventListener("DOMContentLoaded", function() {
    const songButtons = document.querySelectorAll(".song");
    const audioElement = document.getElementById("audio");
    const playPauseButton = document.getElementById("play-pause");
    const currentTimeSpan = document.querySelector(".current-time");
    const totalTimeSpan = document.querySelector(".total-time");
    const progressBar = document.querySelector(".progress-bar");
    const progressDot = document.querySelector(".progress-dot");

    // Update current time and total time
    function updateTime() {
        const currentTime = formatTime(audioElement.currentTime);
        const totalTime = formatTime(audioElement.duration);
        currentTimeSpan.textContent = currentTime;
        totalTimeSpan.textContent = totalTime;
    }

    // Format time in MM:SS format
    function formatTime(time) {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }

    // Update progress bar and progress dot
    function updateProgress() {
        const percent = (audioElement.currentTime / audioElement.duration) * 100;
        progressBar.style.width = percent + '%';
        progressDot.style.left = percent + '%';
    }

    // Add event listeners to song buttons
    songButtons.forEach(function(button) {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            const previewUrl = this.value;
            const artist = this.querySelector(".artist").innerText;
            const trackName = this.querySelector(".track-name").innerText;

            // Check if previewUrl is a URL or a file path
            if (previewUrl.startsWith('http') || previewUrl.startsWith('file')) {
                audioElement.src = previewUrl;
            } else {
                // Assuming the file path is relative to the server's root directory
                audioElement.src = '/' + previewUrl;
            }
            audioElement.play(); // Play the audio
            document.querySelector(".player h2").innerText = trackName;
            document.querySelector(".player h3").innerText = artist;
            playPauseButton.classList.add("playing"); // Add "playing" class to the player wrapper

            // Update time and progress bar
            updateTime();
            updateProgress();
        });
    });

    // Add event listener for time update
    audioElement.addEventListener("timeupdate", function() {
        updateTime();
        updateProgress();
    });

    // Function to toggle play/pause icon
    function togglePlayPauseIcon() {
        const playIcon = playPauseButton.querySelector(".play-icon");
        const pauseIcon = playPauseButton.querySelector(".pause-icon");

        if (audioElement.paused) {
            playIcon.style.display = "inline";
            pauseIcon.style.display = "none";
        } else {
            playIcon.style.display = "none";
            pauseIcon.style.display = "inline";
        }
    }

    // Add event listener for play/pause button click
    playPauseButton.addEventListener("click", function() {
        if (audioElement.paused) {
            audioElement.play();
        } else {
            audioElement.pause();
        }
        togglePlayPauseIcon();
    });
});
