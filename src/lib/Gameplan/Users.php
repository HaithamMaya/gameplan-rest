<?php
/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/27/16
 * Time: 10:41 AM
 */

namespace Gameplan;


class Users extends Table
{
    /**
     * Constructor
     * @param $db The PDO object
     */
    public function __construct($db) {
        parent::__construct($db, "users");
    }

    /**
     * Get a user based on the id
     * @param $id ID of the user
     * @returns User object if successful, null otherwise.
     */
    public function get($id) {
        $sql =<<<SQL
SELECT * from $this->tableName
where id=?
SQL;
        $statement = $this->db->prepare($sql);
        $statement->execute(array($id));
        if($statement->rowCount() === 0) {
            return null;
        }
        return new User($statement->fetch(\PDO::FETCH_ASSOC));
    }

    /**
     * Create a new user.
     * @param User $user The new user data
     * @param Email $mailer An Email object to use
     * @return null on success or error message if failure
     */
    public function add(User $user) {
        // Ensure we have no duplicate email address
        if($this->exists($user->getEmail())) {
            return "Email address already exists.";
        }

        // Add a record to the user table
        $sql = <<<SQL
INSERT INTO $this->tableName VALUES
(DEFAULT, ?, ?, DEFAULT, ?, ?, ?, ?, DEFAULT, DEFAULT, DEFAULT, DEFAULT);
SQL;

        $statement = $this->db->prepare($sql);
        $statement->execute(array(
            $user->getFirst(), $user->getLast(), $user->getEmail(), $user->getRole(),
            (int)$user->getSchoolid(), (int)$user->getAddressid()));
        $id = $this->db->lastInsertId('users_id_seq');

        // Create a validator and add to the validator table
        $validators = new Validators($this->db);
        $validator = $validators->newValidator($id);

        $name = $user->getFirst() . ' ' . $user->getLast();
        $to = array($user->getEmail(), $name);

        $mailer = new Email();
        $mailer->welcome($name, $validator);
        $ret = $mailer->send($to);

        return $ret;
    }

    /**
     * Determine if a user exists in the system.
     * @param $email An email address.
     * @returns true if $email is an existing email address
     */
    public function exists($email) {
        $sql =<<<SQL
SELECT * from $this->tableName
where email=?
SQL;
        $statement = $this->db->prepare($sql);

        $statement->execute(array($email));
        if($statement->rowCount() === 0) {
            return false;
        }
        else{
            return true;
        }
    }

    /**
     * Test for a valid login.
     * @param $email User email
     * @param $password Password credential
     * @returns User object if successful, null otherwise.
     */
    public function login($email, $password) {
        $sql =<<<SQL
SELECT * from $this->tableName
where email=?
SQL;
        $statement = $this->db->prepare($sql);

        $statement->execute(array($email));
        if($statement->rowCount() === 0) {
            return null;
        }

        $row = $statement->fetch(\PDO::FETCH_ASSOC);

        // Get the encrypted password and salt from the record
        $hash = $row['password'];
        $salt = $row['salt'];
        $pepper = $row['created'];

        // Ensure it is correct
        if($hash !== hash("sha256", $password . $salt . $pepper)) {
            return null;
        }
        if($hash)

        return new User($row);
    }

    /**
     * Set the password for a user
     * @param $id The ID for the user
     * @param $password New password to set
     */
    public function setPassword($id, $password) {
        $joined = strtotime(date());
        $salt = $this->randomSalt();
        $passwd = hash("sha256", $password . $salt . $joined);

        $sql = <<<SQL
UPDATE $this->tableName
SET hash=?, salt=?, joined=?
where id=?
SQL;
        $statement = $this->db->prepare($sql);
        $ret = $statement->execute(array($passwd, $salt, $id));

        return $ret;
    }

    /**
     * Generate a random salt string of characters for password salting
     * @param $len Length to generate, default is 16
     * @returns Salt string
     */
    public static function randomSalt($len = 16) {
        $chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789`~!@#$%^&*()-=_+';
        $l = strlen($chars) - 1;
        $str = '';
        for ($i = 0; $i < $len; ++$i) {
            $str .= $chars[rand(0, $l)];
        }
        return $str;
    }

    public function recover(User $user){
        // Create a validator and add to the validator table
        $validators = new Validators($this->db);
        $validator = $validators->newValidator($user->getId());

        $name = $user->getFirst() . ' ' . $user->getLast();
        $to = array($user->getEmail(), $name);

        $mailer = new Email();
        $mailer->recover($name, $validator);
        $ret = $mailer->send($to);

        return $ret;
    }
}