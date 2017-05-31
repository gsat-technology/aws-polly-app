content = """
<html>
  <head>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">

    <style>
    #main-div {
      width: 600px;
      margin: 0 auto;
    }

    button, label {
      margin-top: 5px;
    }

    #voice-sel {
      width: 200px;
    }

    #translation-sel {
      width: 200px;
    }

    .side-by-side {
      margin: auto;
      margin-top: 20px;
    }

    .float-left {
      float: left;
      margin-right: 10px;
    }

    .sub-div {
      clear: left;
      padding-top: 10px;
    }

    </style>

  </head>
  <body>
    <div id="main-div" class="form-group">
      <label for="pwd">Password:</label>
      <input type="password" class="form-control" id="pwd">
      <label for="comment">Text to convert to speech</label>
      <textarea id="text-in" class="form-control" rows="5" cols="13" id="comment"></textarea>

      <div class="side-by-side">
        <label class="float-left" for="voice-sel">Voice</label>
        <select class="form-control float-left" id="voice-sel">
          <option value="Nicole">Nicole (Australian)</option>
          <option value="Russell">Russell (Australian)</option>
          <option value="Russell">Mathieu (French)</option>
          <option value="Hans">Hans (German)</option>
          <option value="Dora">Dora (Icelandic)</option>
          <option value="Dora">Filiz (Turkish)</option>
          <option value="Dora">Mizuki (Japanese)</option>
        </select>
        <label class="float-left" for="translation-sel">Translation</label>
        <select class="form-control float-left" id="translation-sel">
          <option value="none">none</option>
          <option value="en-de">German</option>
          <option value="en-fr">French</option>
          <option value="en-is">Icelandic</option>
          <option value="en-ja">Japanese</option>
          <option value="en-tr">Turkish</option>
        </select>
        <div class="sub-div">
          <button id="sub" type="submit" class="btn btn-primary">Submit</button>
        </div>
      </div>
    </div>

    <script>

      $('#sub').click(function() {

        payload = {}

        var text = $('#text-in').val();
        payload.text = text;

        var pwd = $('#pwd').val();
        payload.password = pwd;

        var voice = $('#voice-sel').find(":selected").val();
        payload.voice = voice;

        var translation = $('#translation-sel').find(":selected").val();

        if (translation != 'none') {
          payload.translation = translation;
        }

        $.ajax({
          type: "POST",
          url: window.location.origin + '/polly',
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(payload),
          success: function(data) {

            new Audio(data.location).play();
          }
        });
      })

    </script>
  </body>
</html>

"""
