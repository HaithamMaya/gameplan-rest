<?php
/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/28/16
 * Time: 7:23 PM
 */

namespace Gameplan;


class Validators extends Table
{
    /**
     * Constructor
     * @param $db The PDO object
     */
    public function __construct($db) {
        parent::__construct($db, "validator");
    }

    /**
     * Create a new validator and add it to the table.
     * @param $userid User this validator is for.
     * @return string new validator.
     */
    public function newValidator($id) {
        $validator = $this->createValidator();

        // Write to the table
        $sql = <<<SQL
INSERT INTO $this->tableName VALUES
(?, ?, DEFAULT);
SQL;
        $statement = $this->db->prepare($sql);
        try {
            if($statement->execute(array($id, $validator)) === false) {
                return null;
            }
        } catch(\PDOException $e) {
            return null;
        }

        return $validator;
    }

    /**
     * @brief Generate a random validator string of characters
     * @param $len Length to generate, default is 32
     * @returns string
     */
    private function createValidator($len = 32) {
        $chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        $l = strlen($chars) - 1;
        $str = '';
        for ($i = 0; $i < $len; ++$i) {
            $str .= $chars[rand(0, $l)];
        }
        return $str;
    }
    /**
     * Determine if a validator is valid. If it is,
     * get the user ID for that validator. Then destroy any
     * validator records for that user ID. Return the
     * user ID.
     * @param $validator Validator to look up
     * @return User ID or null if not found.
     */
    public function getOnce($validator) {
        $sql = <<<SQL
SELECT userid FROM $this->tableName WHERE validator=?
SQL;
        $statement = $this->db->prepare($sql);

        $statement->execute(array($validator));
        if($statement->rowCount() === 0) {
            return null;
        }

        $row = $statement->fetch(\PDO::FETCH_ASSOC);
        $id = $row['userid'];

        $sql = <<<SQL
delete from $this->tableName
where userid=?
SQL;

        $stmt = $this->db->prepare($sql);
        $ret = $stmt->execute(array($id));

        if(!$ret){
            return null;
        }else{
            return $id;
        }
    }

    public function get($validator) {
        $sql = <<<SQL
SELECT id FROM $this->tableName WHERE validator=?
SQL;
        $statement = $this->db->prepare($sql);

        $statement->execute(array($validator));
        if($statement->rowCount() === 0) {
            return false;
        }

        $row = $statement->fetch(\PDO::FETCH_ASSOC);
        $id = $row['id'];
        return $id;
    }

}