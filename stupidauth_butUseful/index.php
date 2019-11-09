
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dartmouth House</title>
    <style>
      /* Space out content a bit */
      body {
        padding-top: 20px;
        padding-bottom: 20px;
        background: url(https://s3.amazonaws.com/erisimages/bkgTrees.jpg);
        background-repeat: repeat;
        background-attachment: fixed;
        padding-left:5px;
        padding-right:5px;
        font-family:arial,sans-serif;
      }

      /* Everything but the jumbotron gets side spacing for mobile first views */
      .header,
      .marketing,
      .footer {
          padding-right: 5px;
          padding-left: 5px;
      }
      .mainDiv {
        margin:0px auto;
        background:white;
        padding:10px;
        font-size:14pt;
      }
      b {
        color:red;
      }
      #clicky {
        border:1px solid #222;
        box-shadow: 1px 1px 5px #000;
        text-align:center;
        padding:3px;
        margin:5px auto;
        width:90px;
        cursor:pointer;
      }
      #clicky:hover {
        background-color:blue;
        color:white;
      }
      #contentContainer {
       padding:5px;
       margin:5px;
        
      }
      #passContainer {
        border:1px solid #222;
        box-shadow: 1px 1px 5px #000;
        text-align:center;
        padding:5px;
        
      }
      
    </style>
</head>
<body>
  <div class="mainDiv">
    <h3 style="color:red;">Welcome to the MHSL Dartmouth House Website</h3>
    <div id="contentContainer">
    
    </div>
    <div id="passContainer">
      Password: <input id="inputpwd" value=""/><br /><div id="clicky">SUBMIT</div>
    </div>
    <div><br />
    <div style="width:150px;margin:0px auto;text-align:center;">
      <br /><br />
      <span style="color:#4286f4;font-weight:bold;">DONATE TO THE DARTMOUTH HOUSE</span><br /><br />
      <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
        <input type="hidden" name="cmd" value="_s-xclick" />
        <input type="hidden" name="hosted_button_id" value="8JWU3HVKM6EKW" />
        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
        <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
      </form>
    </div>     
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script type="text/javascript">
    $(document).ready(function () {
        $('#inputpwd').keypress(function(event){
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if(keycode == '13'){
                clickEnter();
            }
        });
        $('#clicky').click(function () {
            clickEnter();
        });
        clickEnter = function () {
          $.ajax({
            type: "POST",
            url: "pushContent.php",
            data: { "passwd": $('#inputpwd').val() },
            success: function (data) {
              $("#passContainer").append(data);
              if (data.indexOf("0x02") != -1) {
                //alert("SERENITY WEBSITE: SUCK MY DIGITAL DICK... " + data);
                $("#reloadButton").show();
              } else {
                $("#reloadButton").hide();
                $("#passContainer").hide();
                $("#contentContainer").html(data);
                $("#contentContainer").show();
              }
            }
          });
        };
        
        

    });
    </script>
    

  </div>
       
    
</body>
</html>