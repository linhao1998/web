var exampleFASTA =
  ">tr|A0A024QZ08|A0A024QZ08_HUMAN Intraflagellar" +
  " transport 20 homolog (Chlamydomonas), isoform CRA_c OS=Homo" +
  " sapiens OX=9606 GN=IFT20 PE=4 SV=1\nMAKDILGEAGLHFDELNKLRVLDPE" +
  "VTQQTIELKEECKDFVDKIGQFQKIVGGLIELVDQ\nLAKEAENEKMKAIGARNLLKSIAKQ" +
  "REAQQQQLQALIAEKKMQLERYRVEYEALCKVEAE\nQNEFIDQFIFQK";

var patt = /(?=.*[A-Z])^[A-Z\s]+$/;
var valSuc = false;
var b = []

function loadExample() {
  var fastaSeqStr = document.getElementById("sequence").value;
  // var model = document.getElementById("model").value;
  if (fastaSeqStr != exampleFASTA) {
    document.getElementById("sequence").value = exampleFASTA;
  }
  // if (model == "Activity" || model == "PPI" || model == "Regulation") {
  //   document.getElementById("site").setAttribute("placeholder", "Y:107,111 S:81 T:27,30");
  // }
  // else if (model == "Activity(Y)" || model == "PPI(Y)" || model == "Regulation(Y)") {
  //   document.getElementById("site").setAttribute("placeholder", "Y:107,111");
  // }
  // else {
  //   document.getElementById("site").setAttribute("placeholder", "S:81 T:27,30");
  // }
}

function validateForm() {
  var seqArr = document.getElementById("sequence").value.split(/\n/);
  label = seqArr[0];
  delete seqArr[0];
  var seqStr = seqArr.join("");
  var site = document.getElementById("site").value;
  if (label[0] == ">" && patt.test(seqStr)) {
    seqStr = seqStr.replace(/\s+/g, "");
    if (b.indexOf(parseInt(site)) != -1) {
      b = [];
      document.getElementById("load").style.display = "inline-block";
    } else {
      alert(
        "Invalid the phosphorylation site!\n" +
        "Please enter the correct phosphorylation site.\n" +
        "Site information provides correct site information."
      );
      document.getElementById("site").value = "";
      return false;
    }
  } else {
    alert(
      "Invalid FASTA format!\nPlease paste sequences with the correct FASTA format."
    );
    document.getElementById("site").value = "";
    return false;
  }
}

function seqSite() {
  var seqArr = document.getElementById("sequence").value.split(/\n/);
  delete seqArr[0];
  var seqStr = seqArr.join("");
  seqStr = seqStr.replace(/\s+/g, "");
  var model = document.getElementById("model").value;
  var a = [];
  SiteIndexStr = "Please enter the phosphorylation site to be predicted:\n";
  if (model == "Activity" || model == "PPI" || model == "Regulation") {
    var index = seqStr.indexOf('Y');
    b = []
    while (index !== -1) {
      a.push(index + 1);
      b.push(index + 1);
      index = seqStr.indexOf('Y', index + 1);
    }
    SiteIndexStr += "Y:" + a.join(", ") + "\n";
    a = [];
    index = seqStr.indexOf('S');
    while (index !== -1) {
      a.push(index + 1);
      b.push(index + 1);
      index = seqStr.indexOf('S', index + 1);
    }
    SiteIndexStr += "S:" + a.join(", ") + "\n";
    a = [];
    index = seqStr.indexOf('T');
    while (index !== -1) {
      a.push(index + 1);
      b.push(index + 1);
      index = seqStr.indexOf('T', index + 1);
    }
    SiteIndexStr += "T:" + a.join(", ");
    a = [];
  }
  else if (model == "Activity(Y)" || model == "PPI(Y)" || model == "Regulation(Y)") {
    var index = seqStr.indexOf('Y');
    b = [];
    while (index !== -1) {
      a.push(index + 1);
      b.push(index + 1);
      index = seqStr.indexOf('Y', index + 1);
    }
    SiteIndexStr += "Y:" + a.join(", ");
    a = [];
  }
  else {
    var index = seqStr.indexOf('S');
    b = [];
    while (index !== -1) {
      a.push(index + 1);
      b.push(index + 1);
      index = seqStr.indexOf('S', index + 1);
    }
    SiteIndexStr += "S:" + a.join(", ") + "\n";
    a = [];
    var index = seqStr.indexOf('T');
    while (index !== -1) {
      a.push(index + 1);
      b.push(index + 1);
      index = seqStr.indexOf('T', index + 1);
    }
    SiteIndexStr += "T:" + a.join(", ");
    a = [];
  }
  a = null
  // document
  //   .getElementById("site")
  //   .setAttribute("placeholder", SiteIndexStr);
  alert(SiteIndexStr);
}

function startPredict() {
  var seqArr = document.getElementById("sequence").value.split(/\n/);
  delete seqArr[0];
  var seqStr = seqArr.join("");
  seqStr = seqStr.replace(/\s+/g, "");
  var site = document.getElementById("site").value;
  seqHtml = seqStr.replace(
    seqStr[site - 1],
    '<b style="color:red">' + seqStr[site - 1] + '</b>'
  );
  document.getElementById("seq").innerHTML = seqHtml;
}
