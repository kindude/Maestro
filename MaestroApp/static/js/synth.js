window.addEventListener("DOMContentLoaded", () => {
    const synth = new Tone.Synth().toDestination();
    const recorder = new Tone.Recorder();
    synth.connect(recorder);

    let audioStarted = false;

    const playBtn = document.getElementById("play-btn");
    const recordBtn = document.getElementById("record-btn");
    const stopBtn = document.getElementById("stop-btn");

    function ensureAudioStarted() {
        if (!audioStarted) {
            Tone.start().then(() => {
                console.log("AudioContext started");
                audioStarted = true;
            });
        }
    }

    playBtn.addEventListener("click", () => {
        ensureAudioStarted();
        playBtn.disabled = true;
    });

    recordBtn.addEventListener("click", async () => {
        console.log("Hello");

        ensureAudioStarted();
        await recorder.start();
        recordBtn.disabled = true;
        stopBtn.disabled = false;
        console.log("Recording started");
    });

    stopBtn.addEventListener("click", async () => {
        const recording = await recorder.stop();
        const url = URL.createObjectURL(recording);
        const a = document.createElement("a");
        a.href = url;
        a.download = "my-tune.wav";
        a.click();
        recordBtn.disabled = false;
        stopBtn.disabled = true;
        console.log("Recording saved");
    });

    document.addEventListener("keydown", (e) => {
        ensureAudioStarted();
        const key = e.key.toLowerCase();
        const el = document.querySelector(`.key[data-key="${key}"]`);
        if (el) {
            const note = el.getAttribute("data-note");
            synth.triggerAttackRelease(note, "8n");
            el.classList.add("active");
            setTimeout(() => el.classList.remove("active"), 150);
        }
    });
});
