<?php
  $passwordHash = "96327d5521a52aff95ad8066420f715fdd0d2561";

  function getHouseContent() {
    $_POST['passwd'] = "";
    $homepage = file_get_contents('houseContent.txt');
    echo $homepage;
    exit("");
  }
  
  function wrongPass() {
    $_POST['passwd'] = "";
    echo "WRONG PASSWORD RETARD - 0x02";
    exit("");
  }
  
  if ( $_POST['passwd']) {
    $inPass = sha1($_POST['passwd']);
    if ($inPass == $passwordHash) {
      getHouseContent();
    }
  }
  wrongPass();
?>