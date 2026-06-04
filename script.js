let voices = [];

function loadVoices() {
  voices = speechSynthesis.getVoices();

  let voiceSelect = document.getElementById("voiceSelect");
  voiceSelect.innerHTML = "";

  voices.forEach((voice, i) => {
    let option = document.createElement("option");
    option.value = i;
    option.textContent = voice.name + " (" + voice.lang + ")";
    voiceSelect.appendChild(option);
  });
}

speechSynthesis.onvoiceschanged = loadVoices;

function speakText() {
  let text = document.getElementById("text").value;

  let utterance = new SpeechSynthesisUtterance(text);

  let selectedVoice = document.getElementById("voiceSelect").value;
  utterance.voice = voices[selectedVoice];

  speechSynthesis.speak(utterance);
}

function stopVoice() {
  speechSynthesis.cancel();
}
