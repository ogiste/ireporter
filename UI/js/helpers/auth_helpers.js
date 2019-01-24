function setAuth(userData) {
  // Function that stores the authentication details of a user i.e
  // authentication token and username from a userData object
  const userDetails = userData.user;
  const { id, createdOn, ...userProfile } = userDetails;
  localStorage.setItem('ireporter_auth', userData.token);
  localStorage.setItem('ireporter_username', userData.user.username);
  localStorage.setItem('ireporter_id', userData.user.id);
  localStorage.setItem('ireporter_profile', JSON.stringify(userProfile));
}

function getAuthToken() {
  // Function to return the authentication token for current user from
  // localStorage
  return localStorage.getItem('ireporter_auth');
}

function getAuthUsername() {
  // Function to return the authenticated user's username from localStorage
  return localStorage.getItem('ireporter_username');
}

function getAuthId() {
  // Function to return the authenticated user's id from localStorage
  return localStorage.getItem('ireporter_id');
}

function getAuthProfile() {
  // Function to return json object with user profile details
  let userProfile = localStorage.getItem('ireporter_profile');
  userProfile = JSON.parse(userProfile);
  return userProfile;
}

function isAuth() {
  // Return Boolean value based on if authentication token is available for
  // current user
  const authToken = getAuthToken();
  if (authToken) {
    return true;
  }
  return false;
}

function removeAuth() {
  // Function to remove current user authentication details from browser i.e
  // remove authentication token, username and user id from current localStorage
  localStorage.removeItem('ireporter_auth');
  localStorage.removeItem('ireporter_username');
  localStorage.removeItem('ireporter_id');
  localStorage.removeItem('ireporter_profile');
}

const authHelpers = {
  setAuth,
  getAuthToken,
  getAuthUsername,
  getAuthId,
  getAuthProfile,
  isAuth,
  removeAuth,
};

export default authHelpers;
