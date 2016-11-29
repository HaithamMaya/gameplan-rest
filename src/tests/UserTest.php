<?php
require __DIR__ . "/../vendor/autoload.php";
/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/28/16
 * Time: 6:45 PM
 */
use PHPUnit\Framework\TestCase;

class UserTest extends TestCase
{
    public function test_construct() {
        $row = array('id' => 1,
            'first' => 'Cash',
            'last' => 'Compton',
            'email' => 'cash@cashc.me',
            'joined' => '2015-01-15 23:50:26',
            'role' => 'S'
        );
        $user = new Felis\User($row);
        $this->assertEquals(12, $user->getId());
        $this->assertEquals('dude@ranch.com', $user->getEmail());
        $this->assertEquals('123-456-7890', $user->getPhone());
        $this->assertEquals('Some Address', $user->getAddress());
        $this->assertEquals('Some Notes', $user->getNotes());
        $this->assertEquals(strtotime('2015-01-15 23:50:26'),
            $user->getJoined());
        $this->assertEquals('S', $user->getRole());
    }

}