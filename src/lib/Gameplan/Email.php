<?php
/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/28/16
 * Time: 9:42 PM
 */


namespace Gameplan;


class Email {
    /**
     * Email constructor.
     */
    public function __construct()
    {
        $ini = parse_ini_file("../emailConfig.ini");

        $this->mailer = new \PHPMailer;
        $this->mailer->isSMTP();
        $this->mailer->SMTPDebug = 0;
        $this->mailer->Debugoutput = 'html';
        $this->mailer->Host = 'mail.privateemail.com';
        $this->mailer->Port = 587;
        $this->mailer->SMTPSecure = 'tls';
        $this->mailer->SMTPAuth = true;
        $this->mailer->Username = $ini['user'];
        $this->mailer->Password = $ini['pass'];
        $this->mailer->setFrom($ini['user'], $ini['name']);
        $this->site = $ini['site'];
    }

    public function addAttachment($attachment){
        $this->mailer->addAttachment($attachment);
    }

    public function send($to){
        $this->mailer->addAddress($to[0], $to[1]);

        //send the message, check for errors
        if (!$this->mailer->send()) {
            return "Mailer Error: " . $this->mailer->ErrorInfo;
        } else {
            return "Message sent!";
        }
    }

    public function recover($name, $validator){
        $subject = 'Recover Stoked Password';
        $link = $this->site. '/recover-' .$validator;
        $msg = <<<MSG
<html>
<p>Greetings, $name</p>

<p>Recover your password by visiting the following link:</p>

<p><a href="$link">Stoked.io</a></p>
</html>
MSG;
        $this->mailer->msgHTML($msg);
        $this->mailer->Subject = $subject;
    }

    public function welcome($name, $validator){
        $subject = 'Get Stoked!';
        $link = $this->site. '/validator-' .$validator;
        $msg = <<<MSG
<html>
<p>Greetings, $name,</p>

<p>Welcome to Stoked. In order to complete your registration,
please create a username and password by visiting the following link:</p>

<p><a href="$link">Stoked.io</a></p>
</html>
MSG;
        $this->mailer->msgHTML($msg);
        $this->mailer->Subject = $subject;
    }

    protected $mailer;
    protected $site;
}