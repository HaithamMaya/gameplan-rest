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
     * @param $row array from the Users table in the database
     */
    public function __construct($row) {
        $this->id = $row['id'];
        $this->first = $row['first'];
        $this->last = $row['last'];
        $this->username = $row['username'];
        $this->email = $row['email'];
        $this->role = $row['role'];
        $this->schoolid = $row['schoolid'];
        $this->addressid = $row['addressid'];
        $this->created = $row['created'];
        $this->joined = $row['joined'];
    }

    public function getJson(){
        $data['id'] = $this->id;
        $data['first'] = $this->first;
        $data['last'] = $this->last;
        $data['username'] = $this->username;
        $data['email'] = $this->email;
        $data['role'] = $this->role;
        $data['schoolid'] = $this->schoolid;
        $data['addressid'] = $this->addressid;
        $data['created'] = $this->created;
        $data['joined'] = $this->joined;

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
    public function getFirst()
    {
        return $this->first;
    }

    /**
     * @param mixed $first
     */
    public function setFirst($first)
    {
        $this->first = $first;
    }

    /**
     * @return mixed
     */
    public function getLast()
    {
        return $this->last;
    }

    /**
     * @param mixed $last
     */
    public function setLast($last)
    {
        $this->last = $last;
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

    /**
     * @return mixed
     */
    public function getSchoolid()
    {
        return $this->schoolid;
    }

    /**
     * @param mixed $schoolid
     */
    public function setSchoolid($schoolid)
    {
        $this->schoolid = $schoolid;
    }

    /**
     * @return mixed
     */
    public function getAddressid()
    {
        return $this->addressid;
    }

    /**
     * @param mixed $addressid
     */
    public function setAddressid($addressid)
    {
        $this->addressid = $addressid;
    }

    /**
     * @return mixed
     */
    public function getJoined()
    {
        return $this->joined;
    }

    /**
     * @param mixed $joined
     */
    public function setJoined($joined)
    {
        $this->joined = $joined;
    }

    /**
     * @return mixed
     */
    public function getUsername()
    {
        return $this->username;
    }

    /**
     * @param mixed $username
     */
    public function setUsername($username)
    {
        $this->username = $username;
    }


    const ADMIN = "A";
    const STAFF = "S";
    const CLIENT = "C";
    const SESSION_NAME = 'user';

    private $id;		///< The internal ID for the user
    private $first; 	///< First name
    private $last;   	///< Last name
    private $email;		///< Email address
    private $username;  ///< Username
    private $role;		///< User role
    private $schoolid;  ///< ID for School
    private $addressid; ///< ID for Address
    private $created;	///< When user was created in DB
    private $joined;	///< When user activated account

}