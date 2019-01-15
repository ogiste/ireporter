
class User {
    // User class defining properties of a user object and class methods
    // User properties:
    //     fname: First Name (String)
    //     lname: Second Name (String)
    //     othername: Other Name (String)
    //     username: Username (String)
    //     email: Email (String)
    //     phone: Phone (String)
    //     isAdmin: is Administrator (Boolean)
    //     createdOn: Created On (Datetime)

    constructor(user_data) {
        // constructor to initialize user details
        this.fname = user_data.fname;
        this.lname = user_data.lname;
        this.othername = user_data.othername;
        this.username = user_data.username;
        this.email = user_data.email;
        this.phone = user_data.phone;
        this.isAdmin = user_data.isAdmin;
        this.createdOn = user_data.createdOn;
    }

}

login(username, password){
    // Function used to sign in user based on username and password
    postLoginAuth();
}
