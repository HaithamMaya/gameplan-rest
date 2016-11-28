<?php
/**
 * Created by PhpStorm.
 * User: cashc
 * Date: 11/27/16
 * Time: 10:39 AM
 */

namespace Gameplan;


class User
{
    /**
     * Constructor
     * @param $row Row from the Users table in the database
     */
    public function __construct($row) {
        $this->id = $row['id'];
        $this->email = $row['email'];
        $this->name = $row['first']." ".$row['last'];
        $this->created = strtotime($row['created']);
        $this->role = $row['role'];
    }

    public function getJson(){
        $data['id'] = $this->id;
        $data['name'] = $this->name;
        $data['email'] = $this->email;
        $data['created'] = $this->created;
        $data['role'] = $this->role;
        $json = json_encode($data, JSON_PRETTY_PRINT);
        return $json;
    }

    /**
     * @return mixed
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * @param mixed $id
     */
    public function setId($id)
    {
        $this->id = $id;
    }

    /**
     * @return mixed
     */
    public function getEmail()
    {
        return $this->email;
    }

    /**
     * @param mixed $email
     */
    public function setEmail($email)
    {
        $this->email = $email;
    }

    /**
     * @return mixed
     */
    public function getName()
    {
        return $this->name;
    }

    /**
     * @param mixed $name
     */
    public function setName($name)
    {
        $this->name = $name;
    }

    /**
     * @return mixed
     */
    public function getCreated()
    {
        return $this->created;
    }

    /**
     * @param mixed $created
     */
    public function setCreated($created)
    {
        $this->created = $created;
    }

    /**
     * @return mixed
     */
    public function getRole()
    {
        return $this->role;
    }

    /**
     * @param mixed $role
     */
    public function setRole($role)
    {
        $this->role = $role;
    }


    const ADMIN = "A";
    const STAFF = "S";
    const CLIENT = "C";
    const SESSION_NAME = 'user';

    private $id;		///< The internal ID for the user
    private $email;		///< Email address
    private $name; 		///< Name as last, first
    private $created;	///< When user was added
    private $role;		///< User role
}