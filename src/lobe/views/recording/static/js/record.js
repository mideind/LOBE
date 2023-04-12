"use strict";
window.onbeforeunload = function () {
  return "Are you sure?";
};

// ----------------- Globals -------------------
let mediaRecorder;
let audioCtx;
let micSurfer;
let wavesurfer;
let stream;
let meter;

var tokenIndex = 0; // At what utterance are we now?
var numTokens = tokens.length;
const recordingDelay = 100; // delay in ms before recording starts

//transcription
const streamResultElem = document.querySelector("#transcriptionElement");
const finalTranscriptionElem = document.querySelector(
  "#finalTranscriptionElement"
);
const transcriptionListItem = document.querySelector("li#transcriptionLi");

//token stuff
const tokenText = document.querySelector("#tokenText");
const tokenIDSpan = document.querySelector("#tokenID");
const tokenHref = document.querySelector("#tokenHref");
const tokenfileIDSpan = document.querySelector("#tokenFileID");
const tokenProgress = document.querySelector("#tokenProgress");
const currentIndexSpan = document.querySelector("#currentIndexSpan");
const totalIndexSpan = document.querySelector("#totalIndexSpan");
const tokenCard = document.querySelector("#tokenCard");
const videoCard = document.querySelector("#videoCard");

//recording
const recordButtonText = document.querySelector("#recordButtonText");
const recordingCard = document.querySelector("#recordingCard");
const micCard = document.querySelector("#micCard");

//analyze
const analyzeListElement = document.querySelector("li#analyzeLi");
const analyzeMsgElement = document.querySelector("span#analyzeMsg");
const analyzeIcn = document.querySelector("#analyzeIcn");

//buttons
const recordButton = document.querySelector("button#record");
const nextButton = document.querySelector("button#next");
const prevButton = document.querySelector("button#prev");
const deleteButton = document.querySelector("button#delete");
const playButton = document.querySelector("button#play");
const downloadButton = document.querySelector("button#download");
const finishButton = document.querySelector("button#send");
const finishButtonIcon = $("#finishButtonIcon");
const cutButton = document.querySelector("button#cut");
const cutButtonIcon = document.querySelector("#cutButtonIcon");
const cutButtonText = document.querySelector("#cutButtonText");

//other
const downloadRecordFName = document.querySelector("code#downloadRecordFName");

//meter
var meterCanvas = document.querySelector("#meter");
var canvasContext = meterCanvas.getContext("2d");
var rafID = null;

// Audio configuration
// We only support mono audio, not video
// For more information about the constraints, see:
// https://developer.mozilla.org/en-US/docs/Web/API/MediaTrackConstraints
const mediaConstraints = {
  audio: {
    sampleRate: 48000,  // Not supported in Firefox
    sampleSize: 16,  // Not supported in Firefox
    channelCount: 1,
    echoCancellation: true,
    autoGainControl: true, // not supported on Safari, desktop and mobile
    noiseSuppression: true, // not supported on Safari, desktop and mobile
    latency: 0,
  },
};
// RecorderRTC configuration
const mediaRecorderConfig = {
  type: "audio",
  mimeType: "audio/wav",
  recorderType: StereoAudioRecorder,
  sampleRate: mediaConstraints.audio.sampleRate,
  bufferSize: 4096,
  numberOfAudioChannels: mediaConstraints.audio.channelCount,
  disableLogs: true,
};
// For more information about the supported constraints, see:
// https://developer.mozilla.org/en-US/docs/Web/API/MediaTrackSupportedConstraints
const supportedConstraints = navigator.mediaDevices.getSupportedConstraints();
console.log("Supported constraints: ", supportedConstraints);

// ------------- register listeners ------------
nextButton.addEventListener("click", nextAction);
prevButton.addEventListener("click", prevAction);
recordButton.addEventListener("click", recordAction);
playButton.addEventListener("click", playAction);
deleteButton.addEventListener("click", deleteAction);
skipButton.addEventListener("click", skipAction);
downloadButton.addEventListener("click", downloadAction);
finishButton.addEventListener("click", finishAction);
cutButton.addEventListener("click", cutAction);
$(window).keyup(function (e) {
  if (
    e.key === " " ||
    e.key === "Spacebar" ||
    e.keyCode === 38 ||
    e.keyCode === 87
  ) {
    // spacebar, arrow-up or "w"
    e.preventDefault();
    recordAction();
  } else if (e.keyCode === 37 || e.keyCode === 65) {
    // arrow-left or "a"
    prevAction();
  } else if ((e.keyCode === 39 || e.keyCode === 68) && !nextButton.disabled) {
    // arrow-right or "d"
    nextAction();
  } else if (e.keyCode === 40 || e.keyCode === 83) {
    // arrow-down or "s"
    playAction();
  }
});

// ---------------- Actions --------------------
async function nextAction() {
  // Increment the sentence index and update the UI
  if (!await areRecording() && !arePlaying()) {
    if (tokenIndex < numTokens - 1) {
      if (wavesurfer) {
        wavesurfer.destroy();
      }
      tokenIndex += 1;
      await updateUI();
    }
  }
}

async function prevAction() {
  // Decrement the sentence index and update the UI
  if (! await areRecording() && !arePlaying()) {
    if (tokenIndex > 0) {
      if (wavesurfer) {
        wavesurfer.destroy();
      }
      tokenIndex -= 1;
      await updateUI();
    }
  }
}

async function recordAction() {
  const delay = (ms) => new Promise((res) => setTimeout(res, ms));

  if (! await areRecording()) {
    if ("recording" in tokens[tokenIndex]) {
      deleteAction();
    }
    await startRecording();
    tokenCard.style.borderWidth = "2px";
    tokenCard.classList.add("border-success");
    skipButton.disabled = true;
    nextButton.disabled = true;
    prevButton.disabled = true;
    recordButton.disabled = false;
    recordButtonText.innerHTML = "Stoppa";
  } else {
    await stopRecording();
    tokenCard.classList.remove("border-success");
    tokenCard.style.borderWidth = "1px";
    recordButtonText.innerHTML = "Byrja";
    skipButton.disabled = false;
    nextButton.disabled = false;
    prevButton.disabled = false;
  }

  async function startRecording() {
    if (!!wavesurfer) {
      wavesurfer.destroy();
    }
    try {
      stream = await navigator.mediaDevices.getUserMedia(mediaConstraints);
    } catch (e) {
      console.log(e);
      if (e instanceof OverconstrainedError) {
        promptError(
          `Villa kom upp í Media Constraints. Of hátt gildi á ${e.constraint}`,
          e.message,
          e.stack
        );
      }
    }
    audioCtx = new AudioContext(stream);
    mediaRecorder = new RecordRTCPromisesHandler(stream, mediaRecorderConfig);
    // Start recording
    mediaRecorder.startRecording();
    if (conf.visualize_mic) {
      meter = createMeter(audioCtx, stream);
      micSurfer = createMicSurfer(audioCtx, "#micWaveform");
      micSurfer.microphone.start();
      meterDrawLoop();
      setMicUI();
    }
  }

  async function stopRecording() {
    // read information about the audio track - we send this to the server
    let audioTrack = stream.getAudioTracks()[0];
    // See: https://developer.mozilla.org/en-US/docs/Web/API/MediaTrackSettings
    let audioSettings = audioTrack.getSettings();

    await mediaRecorder.stopRecording();
    let blob = await mediaRecorder.getBlob();
    tokens[tokenIndex].recording = {
      blob: blob,
      fname: `${new Date().toISOString()}.wav`,
      url: URL.createObjectURL(blob),
      settings: {
        sampleRate: audioSettings.sampleRate || mediaConstraints.audio.sampleRate, // not in audioSettings in Firefox
        sampleSize: audioSettings.sampleSize || mediaConstraints.audio.sampleSize, // not in audioSettings in Firefox
        channelCount: mediaConstraints.audio.channelCount, // never in audioSettings
        latency: audioSettings.latency || mediaConstraints.audio.latency, // only is Safari
        autoGainControl: audioSettings.autoGainControl || false,
        echoCancellation: audioSettings.echoCancellation,
        noiseSuppression: audioSettings.noiseSuppression || false,
      },
    };
    console.log("Recording stored (not sent):");
    console.log(tokens[tokenIndex].recording);
    
    if (conf.visualize_mic) {
      meter.shutdown();
      if (!!micSurfer) {
        micSurfer.destroy();
      }
      setMicUI();
    }

    // cleanup
    audioCtx.close();
    //stop mediadevice access
    stream.getTracks().forEach((track) => track.stop());
    // reset mediaRecorder
    await mediaRecorder.reset();
    await mediaRecorder.destroy();
    mediaRecorder = null;


    await setRecordingUI();
    setFinishButtonUI();
  }
}

function deleteAction() {
  delete tokens[tokenIndex].recording;
  updateUI();
}

function skipAction() {
  // mark as skipped
  if ("skipped" in tokens[tokenIndex]) {
    // reverse from marking as skipped
    delete tokens[tokenIndex].skipped;
    updateUI(tokenIndex);
  } else {
    tokens[tokenIndex].skipped = true;
    // then go to next
    if ("recording" in tokens[tokenIndex]) {
      delete tokens[tokenIndex].recording;
    }
    nextAction();
  }
}

function playAction() {
  // Play the recording for the sentence at the current index.

  if (arePlaying()) {
    wavesurfer.pause();
  } else {
    if (Object.keys(wavesurfer.regions) && Object.keys(wavesurfer.regions.list).length > 0) {
      wavesurfer.regions.list[Object.keys(wavesurfer.regions.list)[0]].play();
    } else {
      wavesurfer.play();
    }
  }
}

function downloadAction() {
  const a = document.createElement("a");
  a.style.display = "none";
  a.href = tokens[tokenIndex].recording.url;
  a.download = tokens[tokenIndex].recording.fname;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

function finishAction() {
  finishButtonIcon
    .removeClass("fa-arrow-right")
    .addClass("fa-spinner")
    .addClass("fa-spin");
  var xhr = new XMLHttpRequest();
  xhr.onload = function (e) {
    if (this.readyState === XMLHttpRequest.DONE) {
      finishButtonIcon.removeClass("fa-spinner").removeClass("fa-spin");
      if (xhr.status == "200") {
        // if we finish we go straight to the session
        var session_url = xhr.responseText;
        finishButtonIcon.addClass("fa-check");

        window.onbeforeunload = null;
        window.location = session_url;
      } else {
        finishButtonIcon.addClass("fa-times");
        finishButton.classList.add("btn-danger");
        promptError(
          "Villa koma upp við að senda upptökur",
          xhr.responseText,
          ""
        );
      }
    }
    finishButton.disabled = true;
  };
  var fd = new FormData();
  var recordings = {};
  var skipped = [];
  fd.append("user_id", user_id);
  fd.append("manager_id", manager_id);
  fd.append("collection_id", collection_id);
  for (var i = 0; i < numTokens; i++) {
    if ("recording" in tokens[i]) {
      recordings[tokens[i].id] = tokens[i].recording;
      if ("analysis" in tokens[i]) {
        recordings[tokens[i].id].analysis = tokens[i].analysis;
      }
      if ("cut" in tokens[i]) {
        recordings[tokens[i].id].cut = {
          start: tokens[i].cut.start,
          end: tokens[i].cut.end,
        };
      }
      fd.append(
        "file_" + tokens[i].id,
        tokens[i].recording.blob,
        tokens[i].recording.fname
      );
    } else if (tokens[i].skipped) {
      // append as skipped
      skipped.push(tokens[i]["id"]);
    }
  }
  fd.append("recordings", JSON.stringify(recordings));
  fd.append("skipped", JSON.stringify(skipped));
  xhr.open("POST", postRecordingRoute, true);
  xhr.send(fd);
}

function cutAction() {
  if (Object.keys(wavesurfer.regions.list).length > 0) {
    if ("cut" in tokens[tokenIndex]) {
      delete tokens[tokenIndex].cut;
      wavesurfer.clearRegions();
    } else {
      var region =
        wavesurfer.regions.list[Object.keys(wavesurfer.regions.list)[0]];
      tokens[tokenIndex].cut = region;
    }
  }
  setCutUI();
}

// ---------------- UI configuration --------------------
async function updateUI() {
  setTokenUI();
  setProgressUI(tokenIndex + 1);

  setSkipButtonUI();
  setNextButtonUI();
  setFinishButtonUI();
  setAnalysisUI();
  await setRecordingUI();
  await setMicUI();
  setCutUI();
}

function setProgressUI(i) {
  var ratio = (i / numTokens) * 100;
  tokenProgress.style.width = `${ratio.toString()}%`;
  currentIndexSpan.innerHTML = i;
}

function setCutUI(newRegion = false) {
  if (newRegion || (wavesurfer && areRegions())) {
    cutButton.disabled = false;
    if ("cut" in tokens[tokenIndex]) {
      cutButtonIcon.classList.remove("text-success");
      cutButtonIcon.classList.add("text-danger");
      cutButtonText.innerHTML = "Afklippa";
    } else {
      cutButtonIcon.classList.remove("text-danger");
      cutButtonIcon.classList.add("text-success");
      cutButtonText.innerHTML = "Klippa";
    }
  } else {
    cutButtonIcon.classList.remove("text-danger");
    cutButtonIcon.classList.add("text-success");
    cutButtonText.innerHTML = "Klippa";
    cutButton.disabled = true;
  }
}

function setTokenUI() {
  tokenText.innerHTML = tokens[tokenIndex]["text"];
  tokenfileIDSpan.innerHTML = tokens[tokenIndex]["file_id"];
  tokenHref.href = tokens[tokenIndex]["url"];
}

function setSkipButtonUI() {
  if (tokens[tokenIndex].skipped) {
    skipButton.classList.remove("text-danger", "btn-secondary");
    skipButton.classList.add("btn-danger");
    // also disable the recording button
    recordButton.disabled = true;
  } else {
    skipButton.classList.remove("btn-danger");
    skipButton.classList.add("text-danger", "btn-secondary");
    recordButton.disabled = false;
  }
}

function setNextButtonUI() {
  if (!("recording" in tokens[tokenIndex])) {
    nextButton.disabled = true;
  } else {
    nextButton.disabled = false;
  }
}

function setFinishButtonUI() {
  // Only allow if at least one marked token or one recording
  var numRecordings = 0;
  for (var i = 0; i < numTokens; i++) {
    if ("recording" in tokens[i]) {
      numRecordings += 1;
      finishButton.disabled = false;
      return true;
    }
  }
  if (numRecordings === numTokens) {
    finishButton.disabled = false;
  } else {
    finishButton.disabled = true;
  }
}

async function setRecordingUI() {
  //if it has a recording
  if ("recording" in tokens[tokenIndex]) {
    if (typeof wavesurfer === "object") {
      wavesurfer.destroy();
    }
    wavesurfer = createWaveSurfer(
      "#waveform",
      conf.has_video,
      playButtonIcon,
      nextButton,
      prevButton,
      recordButton,
      skipButton,
      deleteButton
    );
    await wavesurfer.loadBlob(tokens[tokenIndex].recording.blob);
    if ("cut" in tokens[tokenIndex]) {
      wavesurfer.addRegion({
        ...tokens[tokenIndex].cut,
        ...{ color: "rgba(243, 156, 18, 0.1)" },
      });
    }
    downloadRecordFName.innerHTML = tokens[tokenIndex].recording.fname;
    recordingCard.style.display = "block";
  } else {
    recordingCard.style.display = "none";
  }
}


function setAnalysisUI() {
  if ("recording" in tokens[tokenIndex] && !conf.analyze_sound) {
    setAnalyzeElement(
      "Slökkt er á gæðastjórnun",
      "warning",
      "fa-question-circle"
    );
  } else if (
    "recording" in tokens[tokenIndex] &&
    "analysis" in tokens[tokenIndex]
  ) {
    switch (tokens[tokenIndex].analysis) {
      case "ok":
        setAnalyzeElement("Upptaka er góð", "success", "fa-thumbs-up");
        break;
      case "high":
        setAnalyzeElement("Upptaka of há", "danger", "fa-thumbs-down");
        break;
      case "low":
        setAnalyzeElement("Upptaka of lág", "danger", "fa-thumbs-down");
        break;
      case "error":
        setAnalyzeElement("Villa kom upp", "danger", "fa-times");
        break;
    }
  } else {
    analyzeListElement.style.display = "none";
  }

  function setAnalyzeElement(text, type, icon) {
    analyzeListElement.style.display = "block";
    analyzeMsgElement.textContent = text;
    analyzeMsgElement.classList.remove(
      "text-success",
      "text-danger",
      "text-warning"
    );
    analyzeMsgElement.classList.add(`text-${type}`);
    analyzeIcn.classList.remove(
      "fa-thumbs-up",
      "fa-thumbs-down",
      "fa-times",
      "fa-question",
      "text-success",
      "text-danger",
      "text-warning"
    );
    analyzeIcn.classList.add(icon, `text-${type}`);
  }
}

async function setMicUI() {
  if (await areRecording() && conf.visualize_mic) {
    micCard.style.display = "block";
  } else {
    micCard.style.display = "none";
    if (micSurfer) {
      micSurfer.destroy();
    }
  }
}

function setLiveUI(type) {
  switch (type) {
    case "wait":
      tokenCard.style.borderWidth = "2px";
      tokenCard.classList.remove("border-success");
      tokenCard.classList.add("border-warning");
      skipButton.disabled = true;
      nextButton.disabled = true;
      prevButton.disabled = true;
      recordButton.disabled = true;
      recordButtonText.innerHTML = "...";
  }
}

// ----------------- Other -----------------
async function areRecording() {
  if (mediaRecorder) {
    return await mediaRecorder.getState() === "recording";
  }
  return false;
}

function arePlaying() {
  if (wavesurfer) {
    return wavesurfer.isPlaying();
  }
  return false;
}

function areRegions() {
  return (
    typeof wavesurfer === "object" &&
    Object.keys(wavesurfer.regions) &&
    Object.keys(wavesurfer.regions.list).length > 0
  );
}

// --------------------- Initialize UI --------------------------
totalIndexSpan.innerHTML = numTokens;
updateUI();
