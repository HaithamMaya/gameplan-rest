<?php
/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/28/16
 * Time: 7:24 PM
 */

namespace Gameplan;


class Table
{
    /**
     * Constructor
     * @param $db The pdo object
     */
    public function __construct($db, $name)
    {
        $this->db = $db;
        $this->tableName = $name;
    }

    /** Diagnostic routine that substitutes into an SQL statement
     * @param $query The queuy with : or ? parameters
     * @param $params The arguments to substitute (what you pass to execute)
     * @return string SQL statement with substituted values
     */
    public function sub_sql($query, $params) {
        $keys = array();
        $values = array();

        // build a regular expression for each parameter
        foreach ($params as $key => $value) {
            if (is_string($key)) {
                $keys[] = '/:' . $key . '/';
            } else {
                $keys[] = '/[?]/';
            }

            if (is_numeric($value)) {
                $values[] = intval($value);
            } else {
                $values[] = '"' . $value . '"';
            }
        }

        $query = preg_replace($keys, $values, $query, 1, $count);
        return $query;
    }

    protected $db;          ///< The PDO object
    protected $tableName;   ///< The table name to use
}