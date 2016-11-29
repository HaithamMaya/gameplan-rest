<?php

/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/26/16
 * Time: 11:52 PM
 */
use \Psr\Http\Message\ServerRequestInterface as Request;
use \Psr\Http\Message\ResponseInterface as Response;

require __DIR__ . "/../vendor/autoload.php";

$config['displayErrorDetails'] = true;
$config['addContentLengthHeader'] = false;

$ini = parse_ini_file("../dbConfig.ini");

$config['db']['host']   = $ini['host'];
$config['db']['port']   = $ini['port'];
$config['db']['user']   = $ini['user'];
$config['db']['pass']   = $ini['pass'];
$config['db']['dbname'] = $ini['dbname'];

$app = new \Slim\App(["settings" => $config]);

$container = $app->getContainer();

$container['logger'] = function($c) {
    $log = new \Monolog\Logger('my_logger');
    $file_handler = new \Monolog\Handler\StreamHandler("../logs/app.log");
    $log->pushHandler($file_handler);
    return $log;
};

$container['db'] = function ($c) {
    $db = $c['settings']['db'];
    try{
        $pdo = new PDO("pgsql:host=" . $db['host'] .
            ";port=" . $db['port'] .
            ";dbname=" . $db['dbname'],
            $db['user'],
            $db['pass']);
    } catch(PDOException $e){
        die("ERROR $e");
    }

    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    return $pdo;
};

$app->get('/user-{id}', function (Request $request, Response $response) {
    $id = $request->getAttribute('id');
    $users = new \Gameplan\Users($this->db);
    $user = $users->get($id);
    if(is_null($user)){
        $response->getBody()->write("Invalid User ID");
    } else{
        $this->logger->addInfo($user->getFirst());
        $response->getBody()->write("Hello, ".$user->getFirst()."\n" . $user->getJson());
    }

    return $response;
});

$app->get('/validate-{v}', function(Request $request, Response $response){
    $validator = $request->getAttribute('v');
    $validators = new \Gameplan\Validators($this->db);
});

$app->post('/validate-{}', function(Request $request, Response $response) {
    $data = $request->getParsedBody();
    $pass1 = filter_var($data['pass1'], FILTER_SANITIZE_STRING);
    $pass2 = filter_var($data['pass2'], FILTER_SANITIZE_STRING);

});

/*$app->get('/user/new', function(Request $request, Response $response){

});*/

$app->post('/user/new', function(Request $request, Response $response){
    $data = $request->getParsedBody();
    $row = array(
        'first' => filter_var($data['first'], FILTER_SANITIZE_STRING),
        'last' => filter_var($data['last'], FILTER_SANITIZE_STRING),
        'email' => filter_var($data['email'], FILTER_SANITIZE_STRING),
        'role' => filter_var($data['role'], FILTER_SANITIZE_STRING),
        'schoolid' => filter_var($data['schoolid'], FILTER_SANITIZE_STRING),
        'addressid' => filter_var($data['addressid'], FILTER_SANITIZE_STRING));

    $user = new \Gameplan\User($row);
    $this->logger->addInfo("Adding user: ".$user->getJson());
    $users = new \Gameplan\Users($this->db);
    $mailer = new \Gameplan\Email();
    $ret = $users->add($user, $mailer);
    $response->getBody()->write($ret);
});

$app->get('/info', function(Request $request, Response $response) {
    $response->getBody()->write(phpinfo());
    return $response;
});



$app->run();