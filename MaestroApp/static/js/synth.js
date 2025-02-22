document.addEventListener("DOMContentLoaded", () => {
        const synth = new Tone.Synth().toDestination();

        function playSound(note, keyElement) {
            if (Tone.context.state !== "running") {
                Tone.start();
            }
            synth.triggerAttackRelease(note, "8n");
            keyElement.classList.add("active");
            setTimeout(() => keyElement.classList.remove("active"), 200);
        }

        document.addEventListener("keydown", (event) => {
            const keyElement = document.querySelector(`.key[data-key="${event.key.toLowerCase()}"]`);
            if (keyElement) {
                playSound(keyElement.dataset.note, keyElement);
            }
        });

        document.querySelectorAll(".key").forEach((keyElement) => {
            keyElement.addEventListener("click", () => {
                playSound(keyElement.dataset.note, keyElement);
            });
        });
    });