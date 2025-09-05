<?php
if($_SERVER["REQUEST_METHOD"]== "POST"){
    $nome = $_POST["nome"];
    $email = $_POST["email"];
    $senha = password_hash($_POST["senha"], PASSWORD_DEFAULT);

    echo "<p style ='color: green;'Usuário $nome Cadastrado com sucesso!</p>";
}
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro</title>
</head>
<style>
    body {
        font-family: Arial;
        background: #f8f8f8;
        padding: 30px;
    }
    form {
        background: white;
        padding: 20px;
        width: 300px;
        border-radius: 8px;
        box-shadow: 0 0 10px #ccc;

    }
</style>
<body>
    
</body>
</html>