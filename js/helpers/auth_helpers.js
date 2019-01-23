import alerts from '../components/alerts.js';
import router from './router.js';
import constants from '../constants.js';

const { alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;

function setAuth(userData) {
  // Function that stores the authentication details of a user i.e
  // authentication token and username from a userData object
  const userDetails = userData.user;
  const { id, createdOn, ...userProfile } = userDetails;
  localStorage.setItem('ireporter_auth', userData.token);
  localStorage.setItem('ireporter_username', userData.user.username);
  if (userData.user.isAdmin) {
    localStorage.setItem('ireporter_admin', userData.user.isAdmin);
  }
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

function getAuthAdmin() {
  // Function to return the authenticated user's id from localStorage
  return localStorage.getItem('ireporter_admin');
}

function isAdmin() {
  // Function to return Boolean value based on if current user is an admin
  const admin = getAuthAdmin();
  if (admin) {
    return true;
  }
  return false;
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

function checkAuthorization() {
  // Function to redirect if user is not authorized to view current page
  createAlert('loading...', alertIds.loading);
  if (isAuth()) {
    createAlert('Page successfully loaded', alertIds.success);
    return;
  }
  createAlert('You are not signed in. Please sign in to view this page',
    alertIds.error);
  newUrl(uiUrlFilepaths.LOGIN);
}

function removeAuth() {
  // Function to remove current user authentication details from browser i.e
  // remove authentication token, username and user id from current localStorage
  localStorage.removeItem('ireporter_auth');
  localStorage.removeItem('ireporter_username');
  localStorage.removeItem('ireporter_admin');
  localStorage.removeItem('ireporter_id');
  localStorage.removeItem('ireporter_profile');
}

const authHelpers = {
  setAuth,
  getAuthToken,
  getAuthUsername,
  getAuthId,
  isAdmin,
  getAuthProfile,
  isAuth,
  checkAuthorization,
  removeAuth,
};

export default authHelpers;
