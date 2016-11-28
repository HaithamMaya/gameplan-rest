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

$inifile = "../config.ini";

$config['displayErrorDetails'] = true;
$config['addContentLengthHeader'] = false;

$ini = parse_ini_file($inifile);

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
    $name = (is_null($user) ? "World" : $user->getName());
    $response->getBody()->write("Hello, $name\n" . $user->getJson());

    return $response;
});

$app->get('/', function(Request $request, Response $response) {
    $response->getBody()->write(phpinfo());
    return $response;
});

$app->run();