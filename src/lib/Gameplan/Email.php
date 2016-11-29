<?php
/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/28/16
 * Time: 9:42 PM
 */

namespace Gameplan;


class Email {
    public function mail($to, $subject, $message, $headers) {
        mail($to, $subject, $message, $headers);
    }
}