const $ = require('jquery');

if(document.getElementById('resume') !== null) {
  $(() => {
    PDFObject.embed('/static/gen/resume.pdf', '#resume');
  });
}
