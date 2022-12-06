var exampleFASTA =
  ">tr|A0A024QZ08|A0A024QZ08_HUMAN Intraflagellar" +
  " transport 20 homolog (Chlamydomonas), isoform CRA_c OS=Homo" +
  " sapiens OX=9606 GN=IFT20 PE=4 SV=1\nMAKDILGEAGLHFDELNKLRVLDPE" +
  "VTQQTIELKEECKDFVDKIGQFQKIVGGLIELVDQ\nLAKEAENEKMKAIGARNLLKSIAKQ" +
  "REAQQQQLQALIAEKKMQLERYRVEYEALCKVEAE\nQNEFIDQFIFQK";

var patt = /(?=.*[A-Z])^[A-Z\s]+$/;

function loadExample() {
  var fastaSeqStr = $("#inputseq").val();
  if (fastaSeqStr != exampleFASTA) {
    $("#inputseq").val(exampleFASTA);
  }
}

function validateForm() {
  var seqArr = $("#inputseq").val().split(/\n/);
  label = seqArr[0];
  delete seqArr[0];
  var seqStr = seqArr.join("");
  if (label[0] == ">" && patt.test(seqStr)) {
    return true;
  } else {
    $(".modal-title").text("Invalid FASTA format");
    $(".modal-body").text("Please paste sequences with the " +
      "correct FASTA format! The first line " +
      "must be started with > and only alphabet, " +
      "*, -, space, and line breaks " +
      "are accepted in the sequence.");
    $("#myModal").modal("show");
    return false;
  }
}

function getAccSeq() {
  var seqArr = $("#inputseq").val().split(/\n/);
  delete seqArr[0];
  var seqStr = seqArr.join("");
  seqStr = seqStr.replace(/\s+/g, "");
  return seqStr
}

function fetchresult(data, siteScore) {
  // get result from server
  // let result = await new Promise((resolve, reject) => $.ajax({..., success: resolve, error: reject}));
  // postprocessing ...
  // return ...

  // fake result:
  let result = {}; // map[number]{weight: number}
  let sequence = Array.from(data);
  for (var index in siteScore) {
    result[index] = {
      weight: siteScore[index],
    }
  }

  return new Promise((resolve) =>
    resolve({
      sequence,
      result,
    })
  );
}

function linear_interpolation(left, right, proportion) {
  return left.map((l, i) => (right[i] - l) * proportion + l);
}

function update_range(value) {
  /*** tested on firefox only ***/
  $("#tag").text(value.toFixed(3));
  $("style#rangestyle").html(`
        .form-range::-moz-range-track {
          background: rgb(255, 246, 0);
          background:linear-gradient(90deg, rgba(255,255,0,1) 0%, rgba(255,219,76,1) ${value * 100
    }%, rgba(255,0,0,1) 100%);
        }
        .form-range::-webkit-slider-runnable-track {
          background: rgb(255, 246, 0);
          background:linear-gradient(90deg, rgba(255,255,0,1) 0%, rgba(255,219,76,1) ${value * 100
    }%, rgba(255,0,0,1) 100%);
        }
        #tag {
          left: calc( ${value * 100}% - 2em );
        }`);
}

async function show_seq_result(siteScore) {
  // get form
  let data = getAccSeq()
  // console.log(data);
  // get result
  let { sequence, result } = await fetchresult(data, siteScore);
  console.log(result);
  let seqmsg = $("#inputseq").val().split(/\n/)[0]

  // show result
  const show_result = () => {
    let threshold = Number.parseFloat($("#range").val());
    update_range(threshold);
    $("#sequence").html(
      sequence.map((v, i) => {
        if (result[i] && result[i].weight >= threshold) {
          let w = result[i].weight;
          let [r, g, b] = linear_interpolation(
            [255, 219, 76],
            [255, 0, 0],
            (w - threshold) / (1 - threshold)
          );
          return `<div style="background-color:rgb(${r}, ${g}, ${b})">${v}</div>`;
        } else {
          return `<div>${v}</div>`;
        }
      })
    );
    $("#seqmsg").text(seqmsg);
    $("#ticks").html(
      sequence.map((v, i) => {
        if ((i + 1) % 10 == 0) {
          return `<div><div>|</div><div>${i + 1}</div></div>`;
        } else {
          return `<div></div>`;
        }
      })
    );
  };

  $("#save").click(function () {
    var fileResult = "";
    for (index in siteScore) {
      var position = parseInt(index) + 1;
      fileResult += position + "\t" + data[index] + "\t" + siteScore[index] + "\n";
    }
    console.log(fileResult)
    var content = seqmsg + "\nprediction model:  " + $("#model").val() + "\nPosition\tResidue\tScores\n" + fileResult;
    var blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    var anchor = document.createElement("a");
    anchor.download = "Prediction_result.txt";
    anchor.href = window.URL.createObjectURL(blob);
    anchor.target = "_blank";
    anchor.style.display = "none"; // just to be safe! 
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
  })

  $("#result").show();
  show_result();

  // update view when range changes
  let captured = false;
  $("#range")
    .off()
    .mousedown(() => (captured = true))
    .mousemove(() => {
      if (captured) {
        let threshold = Number.parseFloat($("#range").val());
        update_range(threshold);
      }
    })
    .mouseup(() => {
      captured = false;
      show_result();
    });
}

function validataFile() {
  var seqArr = $("#inputseq").val().split(/\n/);
  delete seqArr[0];
  var seqStr = seqArr.join("");
  if (seqStr.indexOf(">") != -1) {
    return false;
  } else {
    return true;
  }
};


function bottom() {
  $('html,body').animate({ scrollTop: $('#resultbottom').offset().top }, 500);
}

// main
$(() => {

  $("#openfile").click(function () {
    $("#textinput").hide();
    $("#fileinput").show();
    $("#result").hide();
  });

  $("#back").click(function () {
    $("#fileinput").hide();
    $("#textinput").show();
    $("#uploadmsg").text(
      "Click to upload (only support the FASTA format).");
    $("#openfileinput").val("");
    $("#inputseq").val("");
    $("#result").hide();
  });

  $("#openfileimg").click(function () {
    $("#openfileinput").click();
  });

  $("#openfileinput").change(async function (e) {
    var fileName = e.currentTarget.files[0].name;
    if (fileName.split(".").pop() == "fasta") {
      var file = this.files[0];
      var fr = new FileReader();
      fr.readAsText(file, "UTF-8");
      fr.onload = function (e) {   //读取完文件之后会回到这里
        var inputseq = e.target.result;
        $("#inputseq").val(inputseq);
        $("#uploadmsg").html(
          `${fileName} has been uploaded.<br>Click the <b>Start prediction</b> button to submit the job.`
        );
      };
    } else {
      $(".modal-title").text("Invalid FASTA file");
      $(".modal-body").text("Please upload sequences with the " +
        "correct FASTA format! The first line " +
        "must be started with > and only alphabet, " +
        "*, -, space, and line breaks " +
        "are accepted in the sequence.");
      $("#myModal").modal("show");
    }
  });

  $("#loadExample").click(function () {
    loadExample();
  });

  $("#submit").click(function () {
    if (validateForm()) {
      console.log('AjaxUpload');
      $("#loading").show();
      $("#result").hide();
      bottom();
      $.ajax({
        url: "startPredict",
        type: "Post",
        data: {
          "inputseq": $("#inputseq").val(),
          "model": $("#model").val(),
          "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").attr("value")
        },
        success: function (res) {
          // alert("success!");
          console.log(res)
          $("#loading").hide();
          show_seq_result(res);
          bottom();
        },
        error: function (res) {
          alert("fail!");
          console.log(res);
        }
      });
      return false;
    }
  });

  $("#submit1").click(function () {
    if (validataFile()) {
      $("#submit").click();
    } else {
      $(".modal-title").text("");
      $(".modal-body").text(
        "Please upload a smaller file " +
        "containing only one protein sequence.");
      $("#myModal").modal("show");
    }
  })
});