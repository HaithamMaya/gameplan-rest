<?php
/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/27/16
 * Time: 10:41 AM
 */

namespace Gameplan;


class Users
{
    public function __construct($db)
    {
        $this->db = $db;
    }

    /**
     * Get a user based on the id
     * @param $id ID of the user
     * @returns User object if successful, null otherwise.
     */
    public function get($id) {
        $sql =<<<SQL
SELECT * from Users
where id=?
SQL;

        $statement = $this->db->prepare($sql);

        $statement->execute(array($id));
        if($statement->rowCount() === 0) {
            return null;
        }

        return new User($statement->fetch(\PDO::FETCH_ASSOC));
    }

    protected $db;
}