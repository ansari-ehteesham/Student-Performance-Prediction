const fileInput = document.getElementById('file');
const fileNameDisplay = document.getElementById('file-name');
const modeUpload      = document.getElementById('mode-upload');
const modeTrain       = document.getElementById('mode-train');
const csvSection      = document.getElementById('csv-uploader');
const trainSection    = document.getElementById('normal-training');
const uploadBtn       = document.getElementsByClassName('upload-btn');
const startTrainBtn   = document.getElementById('start-train-btn');

modeUpload.addEventListener('click', () => {
  csvSection.style.display   = 'block';
  trainSection.style.display = 'none';
});
modeTrain.addEventListener('click', () => {
  csvSection.style.display   = 'none';
  trainSection.style.display = 'block';
});

fileInput.addEventListener('change', function () {
    const file = fileInput.files[0]; // Get the first selected file
    if (file) {
      fileNameDisplay.textContent = `Selected file: ${file.name}`;
      document.getElementById('upload-btn').disabled = false;
    } else {
      fileNameDisplay.textContent = 'No file selected';
    }
  });
