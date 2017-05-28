content = """
<html>
  <head>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">

    <style>
    #main-div {
      width: 500px;
      margin: 0 auto;
    }

    button, label {
      margin-top: 5px;
    }

    #voice-sel {
      width: 200px;
    }

    </style>

  </head>
  <body>
    <div id="main-div" class="form-group">
      <label for="pwd">Password:</label>
      <input type="password" class="form-control" id="pwd">
      <label for="comment">Text to convert to speech</label>
      <textarea id="text-in" class="form-control" rows="5" cols="13" id="comment"></textarea>

      <label for="sel1">Voice</label>
      <select class="form-control" id="voice-sel">
        <option value="Nicole">Nicole (Australian)</option>
        <option value="Russel">Russel (Australian)</option>
        <option value="Raveena">Raveena (Indian)</option>
        <option value="Hans">Hans (German)</option>
        <option value="Dora">Dora (Icelandic)</option>
      </select>

      <button id="sub" type="submit" class="btn btn-primary">Submit</button>

    </div>
    <script>

      $('#sub').click(function() {
        console.log('submitting');

        var text = $('#text-in').val();
        console.log('text: ' + text);

        var pwd = $('#pwd').val();
        console.log('password: ' + pwd);

        var voice = $('#voice-sel').find(":selected").val();
        console.log('voice: ' + voice);

        $.ajax({
          type: "POST",
          url: window.location.origin + '/polly',
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify({
            password: pwd,
            text: text,
            voice: voice
          }),
          success: function(data) {
            console.log('success');
            console.log(data);
            new Audio(data.location).play();
          }
        });
      })

    </script>
  </body>
</html>

"""
